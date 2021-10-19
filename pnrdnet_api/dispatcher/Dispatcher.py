import time
from typing import Tuple
import requests
import yaml
import base64
import cbor
from sawtooth_sdk.protobuf import client_batch_submit_pb2
from sawtooth_sdk.protobuf import validator_pb2
from sawtooth_sdk.protobuf import batch_pb2

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import secp256k1

from pnrdnet_addressing.addresser import NAMESPACE, get_owner_address, get_record_address
from pnrdnet_api.decoding import deserialize_data

from .transaction_creation import make_create_owner_transaction
from .transaction_creation import make_create_record_transaction
from .transaction_creation import make_transfer_record_transaction
from .transaction_creation import make_update_record_transaction
from pnrdnet_api.utils.errors import ApiBadRequest, ApiInternalError
from pnrdnet_api.config import DEFAULT_URL_SAWTOOH_REST_API


class Dispatcher(object):
    def __init__(self, sawtooth_rest_api_url=DEFAULT_URL_SAWTOOH_REST_API):
        self.sawtooth_rest_api_url = sawtooth_rest_api_url
        self._context = create_context('secp256k1')
        self._crypto_factory = CryptoFactory(self._context)
        self._batch_signer = self._crypto_factory.new_signer(
            self._context.new_random_private_key())

    def open_validator_connection(self):
        self._connection.open()

    def close_validator_connection(self):
        self._connection.close()

    def get_new_key_pair(self):
        private_key = self._context.new_random_private_key()
        public_key = self._context.get_public_key(private_key)
        return public_key.as_hex(), private_key.as_hex()

    def _get_status(self, batch_id, wait):
        try:
            result = self._send_request(
                f'batch_statuses?id={batch_id}&wait={wait}')
            return yaml.safe_load(result)['data'][0]['status']
        except BaseException as err:
            raise ApiBadRequest(err) from err

    def _send_request(self, suffix, data=None, name=None, http_verb='POST'):
        url = f"{self.sawtooth_rest_api_url}/{suffix}"
        headers = {
            'Content-Type': 'application/octet-stream'
        }
        try:
            if data is not None and http_verb == 'POST':
                result = requests.post(url, headers=headers, data=data)
            else:
                result = requests.get(url, headers=headers)

            if result.status_code == 404:
                raise ApiBadRequest("No such key: {}".format(name))

            if not result.ok:
                raise ApiBadRequest("Error {}: {}".format(
                    result.status_code, result.reason))

        except requests.ConnectionError as err:
            raise ApiBadRequest(
                'Failed to connect to REST API: {}'.format(err)) from err

        except BaseException as err:
            raise ApiBadRequest(err) from err

        return result.text

    def _get_blockchain_data_net(self, address, result):
        encoded_entries = yaml.safe_load(result)["data"]
        deserialize_data_batch = []
        for n in encoded_entries:
            decode_data = base64.b64decode(n["data"])
            data_type, resources = deserialize_data(n["address"], decode_data)
            deserialize_data_batch.append(
                {"type": data_type, "resources": resources})
        return deserialize_data_batch

    def _get_blockchain_data(self, address, result):
        encoded_entries = yaml.safe_load(result)["data"]
        decode_data = [
            base64.b64decode(entry["data"])
            for entry in encoded_entries
        ]
        deserialized_data = []
        for entry in decode_data:
            data_type, resources = deserialize_data(address, entry)
            deserialized_data.append(resources)
        return deserialized_data

    def _transaction_signer(self, private_key):
        return self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

    def get_owner_data(self, public_key):
        owner_address = get_owner_address(public_key)
        result = self._send_request(
            f"state?address={owner_address}")

        try:
            deserialized_data = self._get_blockchain_data(
                owner_address, result)
            return (deserialized_data, owner_address)
        except BaseException as e:
            print(e)
            return None

    def get_record_data(self, record_id):
        record_address = get_record_address(record_id)
        result = self._send_request(
            f"state?address={record_address}")
        try:
            deserialized_data = self._get_blockchain_data(
                record_address, result)
            return (deserialized_data, record_address)
        except BaseException as e:
            print(e)
            return None

    def get_network_data(self):
        namespace_address = NAMESPACE

        result = self._send_request(
            f"state?address={namespace_address}")
        try:

            deserialized_data = self._get_blockchain_data_net(
                namespace_address, result)
            return (deserialized_data, namespace_address)
        except BaseException as e:
            print(e)
            return None

    def send_create_owner_transaction(self,
                                      private_key,
                                      name,
                                      timestamp):
        transaction_signer = self._transaction_signer(private_key)
        batch = make_create_owner_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            name=name,
            timestamp=timestamp)

        response, status = self.post_batch(
            batch=batch, transaction_name="create_owner", wait=1)
        return response, status
        # self._send_and_wait_for_commit(batch)

    def send_create_record_transaction(self,
                                       private_key,
                                       reader_id,
                                       ant_id,
                                       situation,
                                       token,
                                       record_id,
                                       tag_id,
                                       timestamp):

        transaction_signer = self._transaction_signer(private_key)
        batch = make_create_record_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            reader_id=reader_id,
            ant_id=ant_id,
            situation=situation,
            token=token,
            record_id=record_id,
            tag_id=tag_id,
            timestamp=timestamp)
        response, status = self.post_batch(
            batch=batch, transaction_name="create_record", wait=1)
        return response, status

    def send_transfer_record_transaction(self,
                                         private_key,
                                         receiving_owner,
                                         record_id,
                                         timestamp):
        transaction_signer = self._transaction_signer(private_key)

        batch = make_transfer_record_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            receiving_owner=receiving_owner,
            record_id=record_id,
            timestamp=timestamp)

        response, status = self.post_batch(
            batch=batch, transaction_name="transfer_record", wait=1)
        return response, status

    def send_update_record_transaction(self,
                                       private_key,
                                       reader_id,
                                       ant_id,
                                       situation,
                                       token,
                                       record_id,
                                       timestamp):
        transaction_signer = self._transaction_signer(private_key)

        batch = make_update_record_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            reader_id=reader_id,
            ant_id=ant_id,
            situation=situation,
            token=token,
            record_id=record_id,
            timestamp=timestamp)

        response, status = self.post_batch(
            batch=batch, transaction_name="update_record", wait=1)
        return response, status

    def post_batch(self, batch,  transaction_name, wait=None) -> tuple[str, str]:
        batch_list = batch_pb2.BatchList(batches=[batch])
        batch_id = batch.header_signature
        if wait and wait > 0:
            wait_time = 0
            start_time = time.time()
            response = self._send_request(
                suffix="batches", data=batch_list.SerializeToString(), name=transaction_name)
            while wait_time < wait:
                status = self._get_status(
                    batch_id,
                    wait - int(wait_time),
                )
                wait_time = time.time() - start_time
                if status != 'PENDING':
                    return (response, status)

            return (response, "")

        rest = self._send_request(
            suffix="batches", data=batch_list.SerializeToString(), name=transaction_name,  http_verb="POST")
        return (rest, "")

    def _send_and_wait_for_commit(self, batch):
        # Send transaction to validator
        submit_request = client_batch_submit_pb2.ClientBatchSubmitRequest(
            batches=[batch])
        self._connection.send(
            validator_pb2.Message.CLIENT_BATCH_SUBMIT_REQUEST,
            submit_request.SerializeToString())

        # Send status request to validator
        batch_id = batch.header_signature
        status_request = client_batch_submit_pb2.ClientBatchStatusRequest(
            batch_ids=[batch_id], wait=True)
        validator_response = self._connection.send(
            validator_pb2.Message.CLIENT_BATCH_STATUS_REQUEST,
            status_request.SerializeToString())

        # Parse response
        status_response = client_batch_submit_pb2.ClientBatchStatusResponse()
        status_response.ParseFromString(validator_response.content)
        status = status_response.batch_statuses[0].status
        if status == client_batch_submit_pb2.ClientBatchStatus.INVALID:
            error = status_response.batch_statuses[0].invalid_transactions[0]
            raise ApiBadRequest(error.message)
        elif status == client_batch_submit_pb2.ClientBatchStatus.PENDING:
            raise ApiInternalError('Transaction submitted but timed out')
        elif status == client_batch_submit_pb2.ClientBatchStatus.UNKNOWN:
            raise ApiInternalError('Something went wrong. Try again later')
