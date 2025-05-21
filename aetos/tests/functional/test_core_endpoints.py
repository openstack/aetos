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

"""
test_core_endpoints
----------------------------------

Tests for endpoints under /api/v1
"""

from unittest import mock

from observabilityclient import prometheus_client

from aetos.tests.functional import base


class TestCoreEndpointsAsUser(base.TestCase):
    def test_label(self):
        pass

    def test_labels(self):
        pass

    def test_query(self):
        pass

    def test_series(self):
        pass

    def test_status(self):
        pass

    def test_targets(self):
        pass


class TestCoreEndpointsAsAdmin(base.TestCase):
    def test_label(self):
        pass

    def test_labels(self):
        pass

    def test_query(self):
        pass

    def test_series(self):
        pass

    def test_status(self):
        pass

    def test_targets(self):
        pass


class CoreEndpointsErrorCommonTests():
    def test_label(self):
        with base.quiet_expected_exception():
            result = self.get_json('/label/name/values',
                                   headers=self.admin_auth_headers,
                                   status=self.expected_status_code,
                                   expect_errors=True)
        self.assertEqual(self.expected_status_code, result.status_code)

    def test_labels(self):
        with base.quiet_expected_exception():
            result = self.get_json('/labels',
                                   headers=self.admin_auth_headers,
                                   status=self.expected_status_code,
                                   expect_errors=True)

        self.assertEqual(self.expected_status_code, result.status_code)

    def test_query(self):
        with base.quiet_expected_exception():
            result = self.get_json('/query', query="some_query{l='lvalue'}",
                                   headers=self.admin_auth_headers,
                                   status=self.expected_status_code,
                                   expect_errors=True)

        self.assertEqual(self.expected_status_code, result.status_code)

    def test_series(self):
        args = {"match[]": ["metric_name1", "metric_name2"]}
        with base.quiet_expected_exception():
            result = self.get_json('/series', **args,
                                   headers=self.admin_auth_headers,
                                   status=self.expected_status_code,
                                   expect_errors=True)

        self.assertEqual(self.expected_status_code, result.status_code)

    def test_status(self):
        with base.quiet_expected_exception():
            result = self.get_json('/status/runtimeinfo',
                                   headers=self.admin_auth_headers,
                                   status=self.expected_status_code,
                                   expect_errors=True)

        self.assertEqual(self.expected_status_code, result.status_code)

    def test_targets(self):
        with base.quiet_expected_exception():
            result = self.get_json('/targets/somestate',
                                   headers=self.admin_auth_headers,
                                   status=self.expected_status_code,
                                   expect_errors=True)

        self.assertEqual(self.expected_status_code, result.status_code)


class TestCoreEndpointsServerSideError(
    base.TestCase,
    CoreEndpointsErrorCommonTests
):
    def setUp(self):
        super().setUp()
        self.expected_status_code = 508

        exception = prometheus_client.PrometheusAPIClientError(
            base.ErrorResponse(self.expected_status_code)
        )
        self.mock_get = mock.patch.object(
            prometheus_client.PrometheusAPIClient,
            '_get',
            side_effect=exception
        )
        self.mock_get.start()

    def tearDown(self):
        self.mock_get.stop()
        super().tearDown()


class TestCoreEndpointsClientSideError(
    base.TestCase,
    CoreEndpointsErrorCommonTests
):
    def setUp(self):
        super().setUp()
        self.expected_status_code = 418

        exception = prometheus_client.PrometheusAPIClientError(
            base.ErrorResponse(self.expected_status_code)
        )
        self.mock_get = mock.patch.object(
            prometheus_client.PrometheusAPIClient,
            '_get',
            side_effect=exception
        )
        self.mock_get.start()

    def tearDown(self):
        self.mock_get.stop()
        super().tearDown()


class TestCoreEndpointsUnexpectedStatusCodeError(
    base.TestCase,
    CoreEndpointsErrorCommonTests
):
    def setUp(self):
        super().setUp()
        self.expected_status_code = 501

        exception = prometheus_client.PrometheusAPIClientError(
            base.ErrorResponse(102)
        )
        self.mock_get = mock.patch.object(
            prometheus_client.PrometheusAPIClient,
            '_get',
            side_effect=exception
        )
        self.mock_get.start()

    def tearDown(self):
        self.mock_get.stop()
        super().tearDown()
