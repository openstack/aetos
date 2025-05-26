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
test_admin_endpoints
----------------------------------

Tests for endpoints under /api/v1/admin/tsdb
"""

from unittest import mock

from observabilityclient import prometheus_client

from aetos.tests.functional import base


class TestAdminEndpointsAsReader(base.TestCase):
    def test_snapshot(self):
        pass

    def test_delete_series(self):
        pass

    def test_clean_tombstones(self):
        pass


class TestAdminEndpointsAsAdmin(base.TestCase):
    def test_snapshot(self):
        pass

    def test_delete_series(self):
        pass

    def test_clean_tombstones(self):
        pass


class AdminEndpointsErrorCommonTests():
    def test_delete_series(self):
        params = {"match[]": ["metric_name1", "metric_name2"]}
        with base.quiet_expected_exception():
            result = self.post_json('/admin/tsdb/delete_series', params,
                                    headers=self.admin_auth_headers,
                                    status=self.expected_status_code,
                                    expect_errors=True)

        self.assertEqual(self.expected_status_code, result.status_code)

    def test_snapshot(self):
        with base.quiet_expected_exception():
            result = self.post_json('/admin/tsdb/snapshot', {},
                                    headers=self.admin_auth_headers,
                                    status=self.expected_status_code,
                                    expect_errors=True)

        self.assertEqual(self.expected_status_code, result.status_code)

    def test_clean_tombstones(self):
        with base.quiet_expected_exception():
            result = self.post_json('/admin/tsdb/clean_tombstones', {},
                                    headers=self.admin_auth_headers,
                                    status=self.expected_status_code,
                                    expect_errors=True)

        self.assertEqual(self.expected_status_code, result.status_code)


class TestAdminEndpointsServerSideError(
    base.TestCase,
    AdminEndpointsErrorCommonTests
):
    def setUp(self):
        super().setUp()
        self.expected_status_code = 508

        exception = prometheus_client.PrometheusAPIClientError(
            base.ErrorResponse(self.expected_status_code)
        )
        self.mock_post = mock.patch.object(
            prometheus_client.PrometheusAPIClient,
            '_post',
            side_effect=exception
        )
        self.mock_post.start()

    def tearDown(self):
        self.mock_post.stop()
        super().tearDown()


class TestAdminEndpointsClientSideError(
    base.TestCase,
    AdminEndpointsErrorCommonTests
):
    def setUp(self):
        super().setUp()
        self.expected_status_code = 418

        exception = prometheus_client.PrometheusAPIClientError(
            base.ErrorResponse(self.expected_status_code)
        )
        self.mock_post = mock.patch.object(
            prometheus_client.PrometheusAPIClient,
            '_post',
            side_effect=exception
        )
        self.mock_post.start()

    def tearDown(self):
        self.mock_post.stop()
        super().tearDown()


class TestAdminEndpointsUnexpectedStatusCodeError(
    base.TestCase,
    AdminEndpointsErrorCommonTests
):
    def setUp(self):
        super().setUp()
        self.expected_status_code = 501

        exception = prometheus_client.PrometheusAPIClientError(
            base.ErrorResponse(102)
        )
        self.mock_post = mock.patch.object(
            prometheus_client.PrometheusAPIClient,
            '_post',
            side_effect=exception
        )
        self.mock_post.start()

    def tearDown(self):
        self.mock_post.stop()
        super().tearDown()
