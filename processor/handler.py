
import datetime
import time

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from pnrdnet_addressing import addresser
from pnrdnet_protobuf import payload_pb2

from processor.payload import PnrdNetPayload
from processor.state import PnrdNetState


SYNC_TOLERANCE = 60 * 5


class PnrdNetHandler(TransactionHandler):

    @property
    def family_name(self):
        return addresser.FAMILY_NAME

    @property
    def family_versions(self):
        return [addresser.FAMILY_VERSION]

    @property
    def namespaces(self):
        return [addresser.NAMESPACE]

    def apply(self, transaction, context):
        header = transaction.header
        payload = PnrdNetPayload(transaction.payload)
        state = PnrdNetState(context)

        _validate_timestamp(payload.timestamp)

        if payload.action == payload_pb2.SimpleSupplyPayload.CREATE_OWNER:
            _create_owner(
                state=state,
                public_key=header.signer_public_key,
                payload=payload)
        elif payload.action == payload_pb2.SimpleSupplyPayload.CREATE_RECORD:
            _create_record(
                state=state,
                public_key=header.signer_public_key,
                payload=payload)
        elif payload.action == payload_pb2.SimpleSupplyPayload.TRANSFER_RECORD:
            _transfer_record(
                state=state,
                public_key=header.signer_public_key,
                payload=payload)
        elif payload.action == payload_pb2.SimpleSupplyPayload.UPDATE_RECORD:
            _update_record(
                state=state,
                public_key=header.signer_public_key,
                payload=payload)
        else:
            raise InvalidTransaction('Unhandled action')


def _create_owner(state, public_key, payload):
    if state.get_owner(public_key):
        raise InvalidTransaction('Owner with the public key {} already '
                                 'exists'.format(public_key))
    state.set_owner(
        public_key=public_key,
        name=payload.data.name,
        timestamp=payload.timestamp)


def _create_record(state, public_key, payload):
    if state.get_owner(public_key) is None:
        raise InvalidTransaction('Owner with the public key {} does '
                                 'not exist'.format(public_key))

    if payload.data.record_id == '':
        raise InvalidTransaction('No record ID provided')

    if state.get_record(payload.data.record_id):
        raise InvalidTransaction('Identifier {} belongs to an existing '
                                 'record'.format(payload.data.record_id))

    _validate_tag(payload.data.tag_id)

    state.set_record(
        public_key=public_key,
        record_id=payload.data.record_id,
        tag_id=payload.data.tag_id,
        reader_id=payload.data.reader_id,
        ant_id=payload.data.ant_id,
        situation=payload.data.situation,
        token=payload.data.token,
        timestamp=payload.timestamp)


def _transfer_record(state, public_key, payload):
    if state.get_owner(payload.data.receiving_owner) is None:
        raise InvalidTransaction(
            'Owner with the public key {} does '
            'not exist'.format(payload.data.receiving_owner))

    record = state.get_record(payload.data.record_id)
    if record is None:
        raise InvalidTransaction('Record with the record id {} does not '
                                 'exist'.format(payload.data.record_id))

    if not _validate_record_owner(signer_public_key=public_key,
                                  record=record):
        raise InvalidTransaction(
            'Transaction signer is not the owner of the record')

    state.transfer_record(
        receiving_agent=payload.data.receiving_agent,
        record_id=payload.data.record_id,
        timestamp=payload.timestamp)


def _update_record(state, public_key, payload):
    record = state.get_record(payload.data.record_id)
    if record is None:
        raise InvalidTransaction('Record with the record id {} does not '
                                 'exist'.format(payload.data.record_id))

    if not _validate_record_owner(signer_public_key=public_key,
                                  record=record):
        raise InvalidTransaction(
            'Transaction signer is not the owner of the record')

    state.update_record(
        record_id=payload.data.record_id,
        reader_id=payload.data.reader_id,
        ant_id=payload.data.ant_id,
        situation=payload.data.situation,
        token=payload.data.token,
        timestamp=payload.timestamp)


def _validate_record_owner(signer_public_key, record):
    """Validates that the public key of the signer is the latest (i.e.
    current) owner of the record
    """
    latest_owner = max(record.owners, key=lambda obj: obj.timestamp).agent_id
    return latest_owner == signer_public_key


def _validate_tag(tag_id):
    if tag_id is None or tag_id == '':
        raise InvalidTransaction('Incorrect TAG')


def _validate_timestamp(timestamp):
    """Validates that the client submitted timestamp for a transaction is not
    greater than current time, within a tolerance defined by SYNC_TOLERANCE

    NOTE: Timestamp validation can be challenging since the machines that are
    submitting and validating transactions may have different system times
    """
    dts = datetime.datetime.utcnow()
    current_time = round(time.mktime(dts.timetuple()) + dts.microsecond/1e6)
    if (timestamp - current_time) > SYNC_TOLERANCE:
        raise InvalidTransaction(
            'Timestamp must be less than local time.'
            ' Expected {0} in ({1}-{2}, {1}+{2})'.format(
                timestamp, current_time, SYNC_TOLERANCE))
