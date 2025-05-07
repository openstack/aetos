# Copyright 2010-2011 OpenStack Foundation
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pecan
from unittest import mock

from aetos.tests import base


class TestCase(base.TestCase):

    """Test case base class for all unit tests."""
    def setUp(self):
        self.mock_pecan_response = mock.patch.object(
            pecan, 'response', return_value=mock.Mock()
        )
        self.mock_pecan_request = mock.patch.object(
            pecan, 'request', return_value=mock.Mock()
        )
        self.mock_pecan_response.start()
        self.mock_pecan_request.start()

        pecan.request.body = ''
        pecan.request.cfg.prometheus_host = '127.0.0.1'
        super().setUp()

    def tearDown(self):
        self.mock_pecan_response.stop()
        self.mock_pecan_request.stop()
        super().tearDown()


class ErrorResponse():
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        return {"status": "error", "error": "test_error"}
