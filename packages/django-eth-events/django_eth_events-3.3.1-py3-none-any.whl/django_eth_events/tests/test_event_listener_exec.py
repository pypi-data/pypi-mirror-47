# -*- coding: utf-8 -*-
from json import dumps, loads

from django.test import TestCase
from eth_tester import EthereumTester
from web3.providers.eth_tester import EthereumTesterProvider

from ..event_listener import EventListener
from ..factories import DaemonFactory
from ..models import Block, Daemon
from ..utils import remove_0x_head
from ..web3_service import Web3Service
from .utils import (CentralizedOracle, centralized_oracle_abi,
                    centralized_oracle_bytecode)


class TestDaemonExec(TestCase):
    def setUp(self):
        self.provider = EthereumTesterProvider(EthereumTester())
        self.web3 = Web3Service(provider=self.provider).web3
        self.web3.eth.defaultAccount = self.web3.eth.coinbase

        # Mock web3
        self.daemon = DaemonFactory()
        self.tx_data = {'from': self.web3.eth.accounts[0],
                        'gas': 1000000}

        # create oracles
        centralized_contract_factory = self.web3.eth.contract(abi=centralized_oracle_abi,
                                                              bytecode=centralized_oracle_bytecode)
        tx_hash = centralized_contract_factory.constructor().transact()
        self.centralized_oracle_factory_address = self.web3.eth.getTransactionReceipt(tx_hash).get('contractAddress')
        self.centralized_oracle_factory = self.web3.eth.contract(self.centralized_oracle_factory_address,
                                                                 abi=centralized_oracle_abi)

        self.contracts = [
            {
                'NAME': 'Centralized Oracle Factory',
                'EVENT_ABI': centralized_oracle_abi,
                'EVENT_DATA_RECEIVER': 'django_eth_events.tests.utils.CentralizedOraclesReceiver',
                'ADDRESSES': [self.centralized_oracle_factory_address[2::]]
            }
        ]
        EventListener.instance = None
        self.listener_under_test = EventListener(contract_map=self.contracts,
                                                 provider=self.provider)
        CentralizedOracle().reset()
        self.assertEqual(CentralizedOracle().length(), 0)
        self.assertEqual(1, self.web3.eth.blockNumber)

    def tearDown(self):
        self.provider.ethereum_tester.reset_to_genesis()
        self.assertEqual(0, self.web3.eth.blockNumber)

    def test_create_centralized_oracle(self):
        self.assertEqual(CentralizedOracle().length(), 0)
        self.assertEqual(0, Daemon.get_solo().block_number)
        self.assertEqual(0, Block.objects.all().count())

        # Create centralized oracle
        tx_hash = self.centralized_oracle_factory.functions.createCentralizedOracle(
            b'QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG').transact(self.tx_data)
        self.assertIsNotNone(tx_hash)
        self.listener_under_test.execute()
        self.assertEqual(CentralizedOracle().length(), 1)
        self.assertEqual(2, Daemon.get_solo().block_number)

        # Check backup
        self.assertEqual(2, Block.objects.all().count())
        block = Block.objects.get(block_number=2)
        self.assertEqual(1, len(loads(block.decoded_logs)))

    def test_reorg_centralized_oracle(self):
        # initial transaction, to set reorg init
        accounts = self.web3.eth.accounts
        self.web3.eth.sendTransaction({'from': accounts[0], 'to': accounts[1], 'value': 5000000})
        self.assertEqual(0, Block.objects.all().count())
        self.assertEqual(CentralizedOracle().length(), 0)
        self.assertEqual(2, self.web3.eth.blockNumber)

        # Create centralized oracle
        tx_hash = self.centralized_oracle_factory.functions.createCentralizedOracle(
            b'QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG').transact(self.tx_data)
        self.assertIsNotNone(tx_hash)
        self.listener_under_test.execute()
        self.assertEqual(CentralizedOracle().length(), 1)
        self.assertEqual(3, Daemon.get_solo().block_number)
        self.assertEqual(3, Block.objects.all().count())
        self.assertEqual(3, self.web3.eth.blockNumber)

        # Reset blockchain (simulates reorg)
        self.tearDown()

        self.web3.eth.sendTransaction({'from': accounts[0], 'to': accounts[1], 'value': 1000000})
        self.web3.eth.sendTransaction({'from': accounts[0], 'to': accounts[1], 'value': 1000000})
        self.web3.eth.sendTransaction({'from': accounts[0], 'to': accounts[1], 'value': 1000000})
        self.assertEqual(3, self.web3.eth.blockNumber)

        # Force block_hash change (cannot recreate a real reorg with python testrpc)
        # TODO Check if it can be done with eth-tester
        block_hash = remove_0x_head(self.web3.eth.getBlock(1)['hash'])
        Block.objects.filter(block_number=1).update(block_hash=block_hash)

        self.listener_under_test.execute()
        self.assertEqual(CentralizedOracle().length(), 0)
        self.assertEqual(3, Daemon.get_solo().block_number)
        self.assertEqual(3, Block.objects.all().count())

    def test_atomic_transaction(self):
        contracts = [
            {
                'NAME': 'Centralized Oracle Factory',
                'EVENT_ABI': centralized_oracle_abi,
                'EVENT_DATA_RECEIVER': 'django_eth_events.tests.utils.ErroredCentralizedOraclesReceiver',
                'ADDRESSES': [self.centralized_oracle_factory_address[2::]]
            }
        ]
        atomic_listener = EventListener(contract_map=contracts, provider=self.provider)

        self.assertEqual(0, Block.objects.all().count())
        self.assertEqual(0, CentralizedOracle().length())
        self.assertEqual(0, Daemon.get_solo().block_number)
        # Create centralized oracle
        tx_hash = self.centralized_oracle_factory.functions.createCentralizedOracle(
            b'QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG').transact(self.tx_data)

        with self.assertRaises(Exception):
            # raising an exception would make the atomic transaction to fail
            atomic_listener.execute()

        # Test transaction atomic worked and updates where committed just for the first block
        self.assertEqual(0, CentralizedOracle().length())
        self.assertEqual(1, Daemon.get_solo().block_number)
        self.assertEqual(2, self.web3.eth.blockNumber)

        # Reset daemon
        daemon = Daemon.get_solo()
        daemon.block_number = 0
        daemon.save()

        # Execute the listener correctly, this will save new blocks
        self.listener_under_test.execute()
        self.assertEqual(1, CentralizedOracle().length())
        self.assertEqual(2, Daemon.get_solo().block_number)
        self.assertEqual(2, Block.objects.all().count())
        self.assertEqual(2, self.web3.eth.blockNumber)

        # Reset blockchain (simulates reorg)
        self.tearDown()

        block = Block.objects.filter(block_number__gt=1).order_by('-block_number').first()
        logs = loads(block.decoded_logs)
        logs[0]['event_receiver'] = 'django_eth_events.tests.utils.ErroredCentralizedOraclesReceiver'
        block.decoded_logs = dumps(logs)
        block.save()

        accounts = self.web3.eth.accounts
        self.web3.eth.sendTransaction({'from': accounts[0], 'to': accounts[1], 'value': 1000000})
        self.web3.eth.sendTransaction({'from': accounts[0], 'to': accounts[1], 'value': 1000000})
        self.web3.eth.sendTransaction({'from': accounts[0], 'to': accounts[1], 'value': 1000000})
        tx_hash = self.centralized_oracle_factory.functions.createCentralizedOracle(
            b'QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG').transact(self.tx_data)

        self.assertEqual(1, CentralizedOracle().length())
        self.assertEqual(2, Daemon.get_solo().block_number)
        self.assertEqual(2, Block.objects.all().count())
        self.assertEqual(4, self.web3.eth.blockNumber)

        block_hash1 = remove_0x_head(self.web3.eth.getBlock(1)['hash'])
        Block.objects.filter(block_number=1).update(block_hash=block_hash1)

        with self.assertRaises(Exception):
            atomic_listener.execute()
        # Test atomic rollback worked
        self.assertEqual(1, CentralizedOracle().length())
        self.assertEqual(2, Daemon.get_solo().block_number)
        self.assertEqual(2, Block.objects.all().count())
        self.assertEqual(4, self.web3.eth.blockNumber)
