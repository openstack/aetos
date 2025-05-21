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
    def setUp(self):
        super().setUp()
        self.expected_status_code = 403
        self.expected_fault_string = "RBAC Authorization Failed"

    def test_snapshot(self):
        result = self.post_json('/admin/tsdb/snapshot', {},
                                headers=self.reader_auth_headers,
                                status=self.expected_status_code,
                                expect_errors=True)

        self.assertEqual(self.expected_status_code, result.status_code)
        self.assertEqual(self.expected_fault_string,
                         result.json['error_message']['faultstring'])

    def test_delete_series(self):
        params = {"match[]": ["metric_name1", "metric_name2"]}
        result = self.post_json('/admin/tsdb/delete_series', params,
                                headers=self.reader_auth_headers,
                                status=self.expected_status_code,
                                expect_errors=True)

        self.assertEqual(self.expected_status_code, result.status_code)
        # NOTE(jwysogla): the delete_series doesn't use wsme, so the
        # error message is slightly differently formatted, but the same
        # status code is still returned and the meaning of the error message
        # is also the same. But this is the reason why we're using assertIn
        # instead of assertEqual here.
        self.assertIn(self.expected_fault_string, result.json['error_message'])

    def test_clean_tombstones(self):
        result = self.post_json('/admin/tsdb/clean_tombstones', {},
                                headers=self.reader_auth_headers,
                                status=self.expected_status_code,
                                expect_errors=True)

        self.assertEqual(self.expected_status_code, result.status_code)
        self.assertEqual(self.expected_fault_string,
                         result.json['error_message']['faultstring'])


class TestAdminEndpointsAsAdmin(base.TestCase):
    def test_snapshot(self):
        expected_status_code = 200
        returned_from_prometheus = {
            "status": "success",
            "data": {
                "name": 'somefilename'
            }
        }

        with mock.patch.object(
            prometheus_client.PrometheusAPIClient,
            '_post',
            return_value=returned_from_prometheus
        ):
            result = self.post_json('/admin/tsdb/snapshot', {},
                                    headers=self.admin_auth_headers,
                                    status=expected_status_code)

        self.assertEqual(expected_status_code, result.status_code)
        self.assertEqual(returned_from_prometheus, result.json)

    def test_delete_series(self):
        expected_status_code = 204
        params = {"match[]": ["metric_name1", "metric_name2"]}
        with mock.patch.object(
            prometheus_client.PrometheusAPIClient,
            '_post',
            return_value={}
        ):
            result = self.post_json('/admin/tsdb/delete_series', params,
                                    headers=self.admin_auth_headers,
                                    status=expected_status_code)

        self.assertEqual(expected_status_code, result.status_code)

    def test_clean_tombstones(self):
        expected_status_code = 204
        with mock.patch.object(
            prometheus_client.PrometheusAPIClient,
            '_post',
            return_value={}
        ):
            result = self.post_json('/admin/tsdb/clean_tombstones', {},
                                    headers=self.admin_auth_headers,
                                    status=expected_status_code)

        self.assertEqual(expected_status_code, result.status_code)


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
