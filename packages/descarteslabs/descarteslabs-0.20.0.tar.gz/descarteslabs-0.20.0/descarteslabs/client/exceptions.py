# Copyright 2018-2019 Descartes Labs.
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


class ClientError(Exception):
    """ Base class """

    pass


class AuthError(ClientError):
    pass


class OauthError(AuthError):
    pass


class ServerError(Exception):
    status = 500


class BadRequestError(ClientError):
    status = 400


class NotFoundError(ClientError):
    status = 404


class ConflictError(ClientError):
    status = 409


class RateLimitError(ClientError):
    status = 429

    def __init__(self, message, retry_after=None):
        super(RateLimitError, self).__init__(message)
        self.retry_after = retry_after


class RetryWithError(ClientError):
    status = 449


class GatewayTimeoutError(ServerError):
    status = 504
