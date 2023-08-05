import binascii
from logging import getLogger

from eth_abi import decode_abi
from ethereum.utils import sha3
from hexbytes import HexBytes

from .singleton import Singleton
from .utils import normalize_address_without_0x, remove_0x_head

logger = getLogger(__name__)


class Decoder(Singleton):
    """
    This module allows to decode ethereum logs (hexadecimal) into readable dictionaries, by using
    Contract's ABIs
    """

    def __init__(self):
        self.methods = {}
        self.added_abis = {}
        self.events = set()

    def reset(self):
        self.methods.clear()
        self.added_abis.clear()
        self.events.clear()

    @staticmethod
    def get_method_id(item):
        if item.get('inputs'):
            # Generate methodID and link it with the abi
            method_header = "{}({})".format(item['name'],
                                            ','.join(map(lambda method_input: method_input['type'], item['inputs'])))
        else:
            method_header = "{}()".format(item['name'])

        return binascii.hexlify(sha3(method_header)).decode('ascii')

    def add_abi(self, abi) -> int:
        """
        Add ABI array into the decoder collection, in this step the method id is generated from:
        sha3(function_name + '(' + param_type1 + ... + param_typeN + ')')
        :param abi: Array of dictionaries
        :return: Items added
        :rtype: int
        """
        added = 0
        abi_sha3 = sha3(str(abi))
        # Check that abi was not processed before
        if abi_sha3 not in self.added_abis:
            for item in abi:
                if item.get('name'):
                    method_id = self.get_method_id(item)
                    self.methods[method_id] = item
                    added += 1
                if item.get('type') == 'event':
                    self.events.add(HexBytes(method_id).hex())
            self.added_abis[abi_sha3] = None
        return added

    def remove_abi(self, abi):
        """
        For testing purposes, we won't sometimes to remove the ABI methods from the decoder
        :param abi: Array of dictionaries
        :return: None
        """
        self.added_abis = {}
        for item in abi:
            if item.get('name'):
                method_id = self.get_method_id(item)
                if self.methods.get(method_id):
                    del self.methods[method_id]

    def decode_log(self, log):
        """
        Decodes an ethereum log and returns the recovered parameters along with the method from the abi that was used
        in decoding. Raises a LookupError if the log's topic is unknown,
        :param log: ethereum log
        :return: dictionary of decoded parameters, decoding method reference
        """
        method_id = remove_0x_head(log['topics'][0])

        if method_id not in self.methods:
            raise LookupError("Unknown log topic.")

        # method item has the event name, inputs and types
        method = self.methods[method_id]
        decoded_params = []
        data_i = 0
        topics_i = 1
        data_types = []

        # get param types from properties not indexed
        for param in method['inputs']:
            if not param['indexed']:
                data_types.append(param['type'])

        # decode_abi expect data in bytes format instead of str starting by 0x
        log_data_bytes = HexBytes(log['data'])
        decoded_data = decode_abi(data_types, log_data_bytes)

        for param in method['inputs']:
            decoded_p = {
                'name': param['name']
            }
            if param['indexed']:
                decoded_p['value'] = log['topics'][topics_i]
                topics_i += 1
            else:
                decoded_p['value'] = decoded_data[data_i]
                data_i += 1

            if '[]' in param['type']:
                if 'address' in param['type']:
                    decoded_p['value'] = [self.decode_address(address) for address in decoded_p['value']]
                else:
                    decoded_p['value'] = list(decoded_p['value'])
            elif 'address' == param['type']:
                decoded_p['value'] = self.decode_address(decoded_p['value'])

            decoded_params.append(decoded_p)

        decoded_event = {
            'params': decoded_params,
            'name': method['name'],
            'address': self.decode_address(log['address']),
            'transaction_hash': self.decode_transaction(log['transactionHash'])
        }

        return decoded_event

    @staticmethod
    def decode_address(address):
        if not address:
            raise ValueError

        if isinstance(address, bytes):
            address = address.hex()

        # Address length must be 40 (42 with 0x), but usually it's packed on 32 bits (length of 66 with 0x)
        if len(address) == 66:
            address = address[26:]

        return normalize_address_without_0x(address)

    @staticmethod
    def decode_transaction(tx_hash):
        if not tx_hash:
            raise ValueError

        if isinstance(tx_hash, bytes):
            tx_hash = tx_hash.hex()

        tx_hash = tx_hash.strip()  # Trim spaces
        if tx_hash.startswith('0x'):  # Remove 0x prefix
            tx_hash = tx_hash[2:]

        if len(tx_hash) < 64:
            raise ValueError

        return tx_hash

    def decode_logs(self, logs):
        """
        Processes and array of ethereum logs and returns an array of dictionaries of logs that could be decoded
        from the ABIs loaded. Logs that could not be decoded are omitted from the result.
        :param logs: array of ethereum logs
        :return: array of dictionaries
        """
        decoded = []
        for log in logs:
            try:
                decoded.append(self.decode_log(log))
            except LookupError:
                pass

        return decoded
