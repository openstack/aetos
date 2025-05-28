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

from observabilityclient import prometheus_client
from observabilityclient import rbac
import os
from unittest import mock
import webtest

from aetos import app
from aetos.tests.functional import base


class TestCoreEndpointsForbidden(base.TestCase):
    def setUp(self):
        super().setUp()
        self.expected_status_code = 403
        self.expected_fault_string = "RBAC Authorization Failed"

        pf = os.path.abspath('aetos/tests/functional/policy.yaml-test')
        self.CONF.set_override('policy_file', pf, group='oslo_policy')
        self.CONF.set_override('auth_mode', None, group=None)
        self.app = webtest.TestApp(app.load_app(self.CONF))

    def test_label(self):
        pass

    def test_labels(self):
        pass

    def test_query(self):
        query_string = 'ceilometer_image_size'
        params = {'query': query_string}

        result = self.get_json('/query', **params,
                               headers=self.reader_auth_headers,
                               status=self.expected_status_code)

        self.assertEqual(self.expected_status_code, result.status_code)
        self.assertEqual(self.expected_fault_string,
                         result.json['error_message']['faultstring'])

    def test_series(self):
        pass

    def test_status(self):
        pass

    def test_targets(self):
        pass


class TestCoreEndpointsAsUser(base.TestCase):
    def test_label(self):
        pass

    def test_labels(self):
        pass

    def test_query(self):
        expected_status_code = 200
        returned_from_prometheus = {
            "status": "success",
            "data": {
                "resultType": "vector",
                "result": [
                    {
                        "metric": {
                            "__name__": "ceilometer_image_size",
                            "counter": "image.size",
                            "image": "828ab616-8904-48fb-a4bb-d037473cee7d",
                            "instance": "localhost:3000",
                            "job": "sg-core",
                            "project": "2dd8edd6c8c24f49bf04670534f6b357",
                            "publisher": "localhost.localdomain",
                            "resource": "828ab616-8904-48fb-a4bb-d037473cee7d",
                            "resource_name": "cirros-0.6.2-x86_64-disk",
                            "type": "size",
                            "unit": "B"
                            },
                        "value": [
                            1748273657.273,
                            "21430272"
                            ]
                        }
                    ]
                }
            }

        query_string = 'ceilometer_image_size'
        modified_query_string = \
            f'ceilometer_image_size{{project_id={self.project_id}}}'
        params = {'query': query_string}
        modified_params = {'query': modified_query_string}

        with (
            mock.patch.object(prometheus_client.PrometheusAPIClient, '_get',
                              return_value=returned_from_prometheus
                              ) as get_mock,
            mock.patch.object(rbac.PromQLRbac, 'modify_query',
                              return_value=modified_query_string) as rbac_mock
            ):
            result = self.get_json('/query', **params,
                                   headers=self.reader_auth_headers,
                                   status=expected_status_code)

        self.assertEqual(returned_from_prometheus, result.json)
        self.assertEqual(expected_status_code, result.status_code)
        get_mock.assert_called_once_with('query', modified_params)
        rbac_mock.assert_called_once_with(query_string)

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
        expected_status_code = 200
        returned_from_prometheus = {
            "status": "success",
            "data": {
                "resultType": "vector",
                "result": [
                    {
                        "metric": {
                            "__name__": "ceilometer_image_size",
                            "counter": "image.size",
                            "image": "828ab616-8904-48fb-a4bb-d037473cee7d",
                            "instance": "localhost:3000",
                            "job": "sg-core",
                            "project": "2dd8edd6c8c24f49bf04670534f6b357",
                            "publisher": "localhost.localdomain",
                            "resource": "828ab616-8904-48fb-a4bb-d037473cee7d",
                            "resource_name": "cirros-0.6.2-x86_64-disk",
                            "type": "size",
                            "unit": "B"
                            },
                        "value": [
                            1748273657.273,
                            "21430272"
                            ]
                        }
                    ]
                }
            }

        query_string = 'ceilometer_image_size'
        params = {'query': query_string}

        with (
            mock.patch.object(prometheus_client.PrometheusAPIClient, '_get',
                              return_value=returned_from_prometheus
                              ) as get_mock,
            mock.patch.object(rbac.PromQLRbac, 'modify_query') as rbac_mock
            ):
            result = self.get_json('/query', **params,
                                   headers=self.admin_auth_headers,
                                   status=expected_status_code)

        self.assertEqual(returned_from_prometheus, result.json)
        self.assertEqual(expected_status_code, result.status_code)
        get_mock.assert_called_once_with('query', params)
        rbac_mock.assert_not_called()

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
