from pnrdnet_addressing import addresser

from pnrdnet_protobuf import owner_pb2
from pnrdnet_protobuf import record_pb2


class PnrdNetState(object):
    def __init__(self, context, timeout=2):
        self._context = context
        self._timeout = timeout

    def get_owner(self, public_key):
        """Gets the owner associated with the public_key

        Args:
            public_key (str): The public key of the agent

        Returns:
            owner_pb2.Owner: Agent with the provided public_key
        """
        address = addresser.get_owner_address(public_key)
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container = owner_pb2.OwnerContainer()
            container.ParseFromString(state_entries[0].data)
            for owner in container.entries:
                if owner.public_key == public_key:
                    return owner

        return None

    def set_owner(self, public_key, name, timestamp):
        """Creates a new owner in state

        Args:
            public_key (str): The public key of the agent
            name (str): The human-readable name of the agent
            timestamp (int): Unix UTC timestamp of when the agent was created
        """
        address = addresser.get_owner_address(public_key)
        owner = owner_pb2.Owner(
            public_key=public_key, name=name, timestamp=timestamp)
        container = owner_pb2.OwnerContainer()
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container.ParseFromString(state_entries[0].data)

        container.entries.extend([owner])
        data = container.SerializeToString()

        updated_state = {}
        updated_state[address] = data
        self._context.set_state(updated_state, timeout=self._timeout)

    def get_record(self, record_id):
        """Gets the record associated with the record_id

        Args:
            record_id (str): The id of the record

        Returns:
            record_pb2.Record: Record with the provided record_id
        """
        address = addresser.get_record_address(record_id)
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container = record_pb2.RecordContainer()
            container.ParseFromString(state_entries[0].data)
            for record in container.entries:
                if record.record_id == record_id:
                    return record

        return None

    def set_record(self,
                   public_key,
                   reader_id,
                   ant_id,
                   situation,
                   token,
                   record_id,
                   tag_id,
                   timestamp):
        """Creates a new record in state

        Args:
            public_key (str): The public key of the agent creating the record
            latitude (int): Initial latitude of the record
            longitude (int): Initial latitude of the record
            record_id (str): Unique ID of the record
            timestamp (int): Unix UTC timestamp of when the agent was created
        """
        address = addresser.get_record_address(record_id)
        owner = record_pb2.Record.Owner(
            owner_id=public_key,
            timestamp=timestamp)
        history = record_pb2.Record.History(
            reader_id=reader_id,
            ant_id=ant_id,
            situation=situation,
            token=token,
            timestamp=timestamp)
        record = record_pb2.Record(
            record_id=record_id,
            tag_id=tag_id,
            owners=[owner],
            histories=[history])
        container = record_pb2.RecordContainer()
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container.ParseFromString(state_entries[0].data)
        container.entries.extend([record])
        data = container.SerializeToString()

        updated_state = {}
        updated_state[address] = data
        self._context.set_state(updated_state, timeout=self._timeout)

    def transfer_record(self, receiving_owner, record_id, timestamp):
        owner = record_pb2.Record.Owner(
            owner_id=receiving_owner,
            timestamp=timestamp)
        address = addresser.get_record_address(record_id)
        container = record_pb2.RecordContainer()
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container.ParseFromString(state_entries[0].data)
            for record in container.entries:
                if record.record_id == record_id:
                    record.owners.extend([owner])
        data = container.SerializeToString()
        updated_state = {}
        updated_state[address] = data
        self._context.set_state(updated_state, timeout=self._timeout)

    def update_record(self,
                      reader_id,
                      ant_id,
                      situation,
                      token,
                      tag_id,
                      record_id,
                      timestamp):
        history = record_pb2.Record.History(
            reader_id=reader_id,
            ant_id=ant_id,
            situation=situation,
            token=token,
            timestamp=timestamp)
        address = addresser.get_record_address(record_id)
        container = record_pb2.RecordContainer()
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container.ParseFromString(state_entries[0].data)
            for record in container.entries:
                if record.record_id == record_id:
                    record.histories.extend([history])
        data = container.SerializeToString()
        updated_state = {}
        updated_state[address] = data
        self._context.set_state(updated_state, timeout=self._timeout)
