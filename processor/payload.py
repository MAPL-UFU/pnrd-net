# Copyright 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

from sawtooth_sdk.processor.exceptions import InvalidTransaction

from pnrdnet_protobuf import payload_pb2


class PnrdNetPayload(object):

    def __init__(self, payload):
        self._transaction = payload_pb2.PnrdPayload()
        self._transaction.ParseFromString(payload)

    @property
    def action(self):
        return self._transaction.action

    @property
    def data(self):
        if self._transaction.HasField('create_owner') and \
            self._transaction.action == \
                payload_pb2.PnrdPayload.CREATE_OWNER:
            return self._transaction.create_owner

        if self._transaction.HasField('create_record') and \
            self._transaction.action == \
                payload_pb2.PnrdPayload.CREATE_RECORD:
            return self._transaction.create_record

        if self._transaction.HasField('transfer_record') and \
            self._transaction.action == \
                payload_pb2.PnrdPayload.TRANSFER_RECORD:
            return self._transaction.transfer_record

        if self._transaction.HasField('update_record') and \
            self._transaction.action == \
                payload_pb2.PnrdPayload.UPDATE_RECORD:
            return self._transaction.update_record

        raise InvalidTransaction('Action does not match payload data')

    @property
    def timestamp(self):
        return self._transaction.timestamp
