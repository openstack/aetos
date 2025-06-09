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
        label_name = 'job'

        result = self.get_json(f'/label/{label_name}/values', {},
                               headers=self.reader_auth_headers,
                               status=self.expected_status_code)

        self.assertEqual(self.expected_status_code, result.status_code)
        self.assertEqual(self.expected_fault_string,
                         result.json['error_message']['faultstring'])

    def test_labels(self):
        result = self.get_json('/labels', {},
                               headers=self.reader_auth_headers,
                               status=self.expected_status_code)

        self.assertEqual(self.expected_status_code, result.status_code)
        self.assertEqual(self.expected_fault_string,
                         result.json['error_message']['faultstring'])

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
        match = 'ceilometer_image_size'
        params = {'match[]': match}

        result = self.get_json('/series', **params,
                               headers=self.reader_auth_headers,
                               status=self.expected_status_code)

        self.assertEqual(self.expected_status_code, result.status_code)
        # NOTE(jwysogla): the series doesn't use wsme, so the
        # error message is slightly differently formatted, but the same
        # status code is still returned and the meaning of the error message
        # is also the same. But this is the reason why we're using assertIn
        # instead of assertEqual here.
        self.assertIn(self.expected_fault_string, result.json['error_message'])

    def test_status(self):
        result = self.get_json('/status/runtimeinfo', {},
                               headers=self.reader_auth_headers,
                               status=self.expected_status_code)

        self.assertEqual(self.expected_status_code, result.status_code)
        self.assertEqual(self.expected_fault_string,
                         result.json['error_message']['faultstring'])

    def test_targets(self):
        params = {'state': 'running'}
        result = self.get_json('/targets', **params,
                               headers=self.reader_auth_headers,
                               status=self.expected_status_code)

        self.assertEqual(self.expected_status_code, result.status_code)
        self.assertEqual(self.expected_fault_string,
                         result.json['error_message']['faultstring'])


class TestCoreEndpointsAsUser(base.TestCase):
    def test_label(self):
        expected_status_code = 200
        returned_from_prometheus = {
            "status": "success",
            "data": [
                "prometheus",
                "sg-core"
                ]
            }

        label_name = 'job'
        expected_match = f"{{project='{self.project_id}'}}"
        expected_params = {'match[]': expected_match}

        with (
            mock.patch.object(prometheus_client.PrometheusAPIClient, '_get',
                              return_value=returned_from_prometheus
                              ) as get_mock,
            mock.patch.object(rbac.PromQLRbac, 'append_rbac_labels',
                              return_value=expected_match) as rbac_mock
            ):
            result = self.get_json(f'/label/{label_name}/values', {},
                                   headers=self.reader_auth_headers,
                                   status=expected_status_code)

        self.assertEqual(returned_from_prometheus, result.json)
        self.assertEqual(expected_status_code, result.status_code)
        get_mock.assert_called_once_with(
            f'label/{label_name}/values', expected_params
        )
        rbac_mock.assert_called_once_with('')

    def test_labels(self):
        expected_status_code = 200
        returned_from_prometheus = {
            "status": "success",
            "data": [
                "__name__",
                "alarm",
                "branch",
                "volume"
                ]
            }

        expected_match = f"{{project='{self.project_id}'}}"
        expected_params = {'match[]': expected_match}

        with (
            mock.patch.object(prometheus_client.PrometheusAPIClient, '_get',
                              return_value=returned_from_prometheus
                              ) as get_mock,
            mock.patch.object(rbac.PromQLRbac, 'append_rbac_labels',
                              return_value=expected_match) as rbac_mock
            ):
            result = self.get_json('/labels', {},
                                   headers=self.reader_auth_headers,
                                   status=expected_status_code)

        self.assertEqual(returned_from_prometheus, result.json)
        self.assertEqual(expected_status_code, result.status_code)
        get_mock.assert_called_once_with(
            'labels', expected_params
        )
        rbac_mock.assert_called_once_with('')

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
            f'ceilometer_image_size{{project={self.project_id}}}'
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
        expected_status_code = 200
        returned_from_prometheus = {
            "status": "success",
            "data": [
                {
                    "__name__": "ceilometer_image_size",
                    "counter": "image.size",
                    "image": "18f639e4-3d0c-447c-a81f-d00db66e63f3",
                    "instance": "localhost:3000",
                    "job": "sg-core",
                    "project": "7b8e1f013ad240fabe4ff2a4f44345fd",
                    "publisher": "localhost.localdomain",
                    "resource": "18f639e4-3d0c-447c-a81f-d00db66e63f3",
                    "resource_name": "tempest-scenario-img--2041421357",
                    "type": "size",
                    "unit": "B"
                    }
                ]
            }

        matches = ['ceilometer_image_size', '{resource="volume.size"}']
        modified_matches = [
            f'ceilometer_image_size{{project={self.project_id}}}',
            f'{{project={self.project_id}, resource="volume.size"}}'
        ]
        params = {'match[]': matches}
        modified_params = {'match[]': modified_matches}

        with (
            mock.patch.object(prometheus_client.PrometheusAPIClient, '_get',
                              return_value=returned_from_prometheus
                              ) as get_mock,
            mock.patch.object(rbac.PromQLRbac, 'modify_query',
                              side_effect=lambda x:
                              modified_matches[matches.index(x)]
                              ) as rbac_mock
            ):
            result = self.get_json('/series', **params,
                                   headers=self.reader_auth_headers,
                                   status=expected_status_code)

        self.assertEqual(returned_from_prometheus, result.json)
        self.assertEqual(expected_status_code, result.status_code)
        get_mock.assert_called_once_with('series', modified_params)
        for match in matches:
            rbac_mock.assert_any_call(match)

    def test_status(self):
        expected_status_code = 403
        expected_fault_string = "RBAC Authorization Failed"

        result = self.get_json('/status/runtimeinfo', {},
                               headers=self.reader_auth_headers,
                               status=expected_status_code)

        self.assertEqual(expected_status_code, result.status_code)
        self.assertEqual(expected_fault_string,
                         result.json['error_message']['faultstring'])

    def test_targets(self):
        expected_status_code = 403
        expected_fault_string = "RBAC Authorization Failed"
        params = {'state': 'running'}

        result = self.get_json('/targets', **params,
                               headers=self.reader_auth_headers,
                               status=expected_status_code)

        self.assertEqual(expected_status_code, result.status_code)
        self.assertEqual(expected_fault_string,
                         result.json['error_message']['faultstring'])


class TestCoreEndpointsAsAdmin(base.TestCase):
    def test_label(self):
        expected_status_code = 200
        returned_from_prometheus = {
            "status": "success",
            "data": [
                "prometheus",
                "sg-core"
                ]
            }

        label_name = 'job'

        with mock.patch.object(prometheus_client.PrometheusAPIClient, '_get',
                               return_value=returned_from_prometheus
                               ) as get_mock:
            result = self.get_json(f'/label/{label_name}/values', {},
                                   headers=self.admin_auth_headers,
                                   status=expected_status_code)

        self.assertEqual(returned_from_prometheus, result.json)
        self.assertEqual(expected_status_code, result.status_code)
        get_mock.assert_called_once_with(f'label/{label_name}/values', None)

    def test_labels(self):
        expected_status_code = 200
        returned_from_prometheus = {
            "status": "success",
            "data": [
                "__name__",
                "alarm",
                "branch",
                "volume"
                ]
            }

        with mock.patch.object(prometheus_client.PrometheusAPIClient, '_get',
                               return_value=returned_from_prometheus
                               ) as get_mock:
            result = self.get_json('/labels', {},
                                   headers=self.admin_auth_headers,
                                   status=expected_status_code)

        self.assertEqual(returned_from_prometheus, result.json)
        self.assertEqual(expected_status_code, result.status_code)
        get_mock.assert_called_once_with('labels', None)

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
        expected_status_code = 200
        returned_from_prometheus = {
            "status": "success",
            "data": [
                {
                    "__name__": "ceilometer_image_size",
                    "counter": "image.size",
                    "image": "18f639e4-3d0c-447c-a81f-d00db66e63f3",
                    "instance": "localhost:3000",
                    "job": "sg-core",
                    "project": "7b8e1f013ad240fabe4ff2a4f44345fd",
                    "publisher": "localhost.localdomain",
                    "resource": "18f639e4-3d0c-447c-a81f-d00db66e63f3",
                    "resource_name": "tempest-scenario-img--2041421357",
                    "type": "size",
                    "unit": "B"
                    }
                ]
            }

        matches = ['ceilometer_image_size', '{resource="volume.size"}']
        params = {'match[]': matches}

        with (
            mock.patch.object(prometheus_client.PrometheusAPIClient, '_get',
                              return_value=returned_from_prometheus
                              ) as get_mock,
            mock.patch.object(rbac.PromQLRbac, 'modify_query'
                              ) as rbac_mock
            ):
            result = self.get_json('/series', **params,
                                   headers=self.admin_auth_headers,
                                   status=expected_status_code)

        self.assertEqual(returned_from_prometheus, result.json)
        self.assertEqual(expected_status_code, result.status_code)
        get_mock.assert_called_once_with('series', params)
        rbac_mock.assert_not_called()

    def test_status(self):
        expected_status_code = 200
        returned_from_prometheus = {
            "status": "success",
            "data": {
                "startTime": "2025-05-26T15:32:23.890553181Z",
                "CWD": "/prometheus",
                "reloadConfigSuccess": True,
                "lastConfigTime": "2025-05-26T15:32:24Z",
                "corruptionCount": 0,
                "goroutineCount": 34,
                "GOMAXPROCS": 4,
                "GOMEMLIMIT": 9223372036854775807,
                "GOGC": "75",
                "GODEBUG": "",
                "storageRetention": "15d"
                }
            }

        with mock.patch.object(prometheus_client.PrometheusAPIClient, '_get',
                               return_value=returned_from_prometheus
                               ) as get_mock:
            result = self.get_json('/status/runtimeinfo', {},
                                   headers=self.admin_auth_headers,
                                   status=expected_status_code)

        self.assertEqual(returned_from_prometheus, result.json)
        self.assertEqual(expected_status_code, result.status_code)
        get_mock.assert_called_once_with('status/runtimeinfo', None)

    def test_targets(self):
        expected_status_code = 200
        returned_from_prometheus = {
            "status": "success",
            "data": {
                "activeTargets": [
                    {
                        "discoveredLabels": {
                            "__address__": "localhost:9090",
                            "__metrics_path__": "/metrics",
                            "__scheme__": "http",
                            "__scrape_interval__": "15s",
                            "__scrape_timeout__": "10s",
                            "job": "prometheus"
                            },
                        "labels": {
                            "instance": "localhost:9090",
                            "job": "prometheus"
                            },
                        "scrapePool": "prometheus",
                        "scrapeUrl": "http://localhost:9090/metrics",
                        "globalUrl": "http://localhost.locald:9090/metrics",
                        "lastError": "",
                        "lastScrape": "2025-06-06T13:16:11.554579236Z",
                        "lastScrapeDuration": 0.006158981,
                        "health": "up",
                        "scrapeInterval": "15s",
                        "scrapeTimeout": "10s"
                        }
                    ],
                "droppedTargets": [],
                "droppedTargetCounts": None
                }
            }
        params = {'state': 'running'}

        with mock.patch.object(prometheus_client.PrometheusAPIClient, '_get',
                               return_value=returned_from_prometheus
                               ) as get_mock:
            result = self.get_json('/targets', **params,
                                   headers=self.admin_auth_headers,
                                   status=expected_status_code)

        self.assertEqual(returned_from_prometheus, result.json)
        self.assertEqual(expected_status_code, result.status_code)
        get_mock.assert_called_once_with('targets', params)


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
