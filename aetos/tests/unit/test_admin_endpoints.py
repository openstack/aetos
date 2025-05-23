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

import pecan
from unittest import mock

from observabilityclient import prometheus_client

from aetos.controllers.api.v1.admin.tsdb import clean_tombstones
from aetos.controllers.api.v1.admin.tsdb import delete_series
from aetos.controllers.api.v1.admin.tsdb import snapshot
from aetos.tests.unit import base


class TestAdminEndpointsAsUser(base.TestCase):
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
        ctrl = delete_series.DeleteSeriesController()
        args = {"match[]": ["metric_name1", "metric_name2"]}
        result = ctrl.post(**args)

        self.assertEqual(self.expected_status_code, pecan.response.status)
        self.assertIn(str(self.expected_content), str(result))

    def test_snapshot(self):
        ctrl = snapshot.SnapshotController()
        result = ctrl.post()

        self.assertEqual(self.expected_status_code, pecan.response.status)
        self.assertIn(str(self.expected_content), str(result))

    def test_clean_tombstones(self):
        ctrl = clean_tombstones.CleanTombstonesController()
        result = ctrl.post()

        self.assertEqual(self.expected_status_code, pecan.response.status)
        self.assertIn(str(self.expected_content), str(result))


class TestAdminEndpointsServerSideError(
    base.TestCase,
    AdminEndpointsErrorCommonTests
):
    def setUp(self):
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

        self.expected_content = str(exception)
        super().setUp()

    def tearDown(self):
        self.mock_post.stop()
        super().tearDown()


class TestAdminEndpointsClientSideError(
    base.TestCase,
    AdminEndpointsErrorCommonTests
):
    def setUp(self):
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

        self.expected_content = str(exception)
        super().setUp()

    def tearDown(self):
        self.mock_post.stop()
        super().tearDown()


class TestAdminEndpointsUnexpectedStatusCodeError(
    base.TestCase,
    AdminEndpointsErrorCommonTests
):
    def setUp(self):
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

        self.expected_content = str(exception)
        super().setUp()

    def tearDown(self):
        self.mock_post.stop()
        super().tearDown()
