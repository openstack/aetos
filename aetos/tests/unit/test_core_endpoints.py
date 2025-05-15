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

import pecan
from unittest import mock

from observabilityclient import prometheus_client

from aetos.controllers.api.v1 import label
from aetos.controllers.api.v1 import labels
from aetos.controllers.api.v1 import query
from aetos.controllers.api.v1 import series
from aetos.controllers.api.v1 import status
from aetos.controllers.api.v1 import targets
from aetos.tests.unit import base


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
        ctrl = label.LabelController()
        result = ctrl.get("name", "values")

        self.assertEqual(self.expected_status_code, pecan.response.status)
        self.assertIn(str(self.expected_content), str(result))

    def test_labels(self):
        ctrl = labels.LabelsController()
        result = ctrl.get()

        self.assertEqual(self.expected_status_code, pecan.response.status)
        self.assertIn(str(self.expected_content), str(result))

    def test_query(self):
        ctrl = query.QueryController()
        result = ctrl.get("some_query{label='label_value'}")

        self.assertEqual(self.expected_status_code, pecan.response.status)
        self.assertIn(str(self.expected_content), str(result))

    def test_series(self):
        ctrl = series.SeriesController()
        args = {"match[]": ["metric_name1", "metric_name2"]}
        result = ctrl.get(**args)

        self.assertEqual(self.expected_status_code, pecan.response.status)
        self.assertIn(str(self.expected_content), str(result))

    def test_status(self):
        ctrl = status.StatusController()
        result = ctrl.get("runtimeinfo")

        self.assertEqual(self.expected_status_code, pecan.response.status)
        self.assertIn(str(self.expected_content), str(result))

    def test_targets(self):
        ctrl = targets.TargetsController()
        result = ctrl.get("somestate")

        self.assertEqual(self.expected_status_code, pecan.response.status)
        self.assertIn(str(self.expected_content), str(result))


class TestCoreEndpointsServerSideError(
    base.TestCase,
    CoreEndpointsErrorCommonTests
):
    def setUp(self):
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

        self.expected_content = str(exception)
        super().setUp()

    def tearDown(self):
        self.mock_get.stop()
        super().tearDown()


class TestCoreEndpointsClientSideError(
    base.TestCase,
    CoreEndpointsErrorCommonTests
):
    def setUp(self):
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

        self.expected_content = str(exception)
        super().setUp()

    def tearDown(self):
        self.mock_get.stop()
        super().tearDown()


class TestCoreEndpointsUnexpectedStatusCodeError(
    base.TestCase,
    CoreEndpointsErrorCommonTests
):
    def setUp(self):
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

        self.expected_content = str(exception)
        super().setUp()

    def tearDown(self):
        self.mock_get.stop()
        super().tearDown()
