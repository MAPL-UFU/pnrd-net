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

import json


class ApiBadRequest(Exception):
    def __init__(self, message):
        self.status_code = 400
        self.message = 'Bad Request: ' + message
        super().__init__(message)


class ApiInternalError(Exception):
    def __init__(self, message):
        self.status_code = 500
        self.message = 'Internal Error: ' + message
        super().__init__(message)


class ApiNotFound(Exception):
    def __init__(self, message):
        self.status_code = 404
        self.message = 'Not Found: ' + message
        super().__init__(message)


class ApiUnauthorized(Exception):
    def __init__(self, message):
        self.status_code = 401
        self.message = 'Unauthorized: ' + message
        super().__init__(message)
