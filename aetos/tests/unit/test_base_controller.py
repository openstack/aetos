#
# Copyright 2025 Red Hat, Inc
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

from unittest import mock

from oslo_config import fixture as fixture_config

from aetos.controllers.api.v1 import base
from aetos.tests import base as test_base


class TestBaseController(test_base.TestCase):

    def setUp(self):
        super().setUp()
        self.controller = base.Base()
        self.conf = self.useFixture(fixture_config.Config()).conf
        self.conf.register_opts(base.PROMETHEUS_OPTS, group='prometheus')

    def test_create_prometheus_client_without_tls(self):
        """Test prometheus client creation without TLS"""
        with mock.patch(
            'observabilityclient.prometheus_client.PrometheusAPIClient'
        ) as mock_client:
            self.controller.create_prometheus_client(self.conf)

            mock_client.assert_called_once_with('localhost:9090')
            mock_client.return_value.set_ca_cert.assert_not_called()
            mock_client.return_value.set_client_cert.assert_not_called()

    def test_create_prometheus_client_with_tls_custom_ca(self):
        """Test prometheus client creation with TLS with custom CA"""
        self.conf.set_override('ca_file', 'cafile', group='prometheus')
        self.conf.set_override('use_tls', True, group='prometheus')

        with mock.patch(
            'observabilityclient.prometheus_client.PrometheusAPIClient'
        ) as mock_client:
            self.controller.create_prometheus_client(self.conf)

            mock_client.assert_called_once_with('localhost:9090')
            mock_client.return_value.set_ca_cert.assert_called_once_with(
                'cafile')
            mock_client.return_value.set_client_cert.assert_not_called()

    def test_create_prometheus_client_with_tls_default_ca(self):
        """Test prometheus client creation with TLS with default CA"""
        self.conf.set_override('use_tls', True, group='prometheus')

        with mock.patch(
            'observabilityclient.prometheus_client.PrometheusAPIClient'
        ) as mock_client:
            self.controller.create_prometheus_client(self.conf)

            mock_client.assert_called_once_with('localhost:9090')
            mock_client.return_value.set_ca_cert.assert_called_once_with(True)
            mock_client.return_value.set_client_cert.assert_not_called()

    def test_create_prometheus_client_without_tls_with_ca(self):
        """Test prometheus client creation without TLS but with CA"""
        self.conf.set_override('ca_file', 'cafile', group='prometheus')
        with mock.patch(
            'observabilityclient.prometheus_client.PrometheusAPIClient'
        ) as mock_client:
            self.controller.create_prometheus_client(self.conf)

            mock_client.assert_called_once_with('localhost:9090')
            mock_client.return_value.set_ca_cert.assert_not_called()
            mock_client.return_value.set_client_cert.assert_not_called()

    def test_create_prometheus_client_with_tls_with_cert_and_key(self):
        """Test prometheus client creation with TLS with cert/key file"""
        self.conf.set_override('use_tls', True, group='prometheus')
        self.conf.set_override('cert_file', 'certfile', group='prometheus')
        self.conf.set_override('key_file', 'keyfile', group='prometheus')

        with mock.patch(
            'observabilityclient.prometheus_client.PrometheusAPIClient'
        ) as mock_client:
            self.controller.create_prometheus_client(self.conf)

            mock_client.assert_called_once_with('localhost:9090')
            mock_client.return_value.set_ca_cert.assert_called_once_with(True)
            mock_client.return_value.set_client_cert.assert_called_once_with(
                'certfile', 'keyfile')

    def test_create_prometheus_client_without_tls_with_cert_and_key(self):
        """Test prometheus client creation without TLS with cert/key file"""
        self.conf.set_override('cert_file', 'certfile', group='prometheus')
        self.conf.set_override('key_file', 'keyfile', group='prometheus')

        with mock.patch(
            'observabilityclient.prometheus_client.PrometheusAPIClient'
        ) as mock_client:
            self.controller.create_prometheus_client(self.conf)

            mock_client.assert_called_once_with('localhost:9090')
            mock_client.return_value.set_ca_cert.assert_not_called()
            mock_client.return_value.set_client_cert.assert_not_called()

    def test_create_prometheus_client_with_tls_with_cert_only(self):
        """Test prometheus client creation with TLS with only cert file"""
        self.conf.set_override('use_tls', True, group='prometheus')
        self.conf.set_override('key_file', 'keyfile', group='prometheus')

        with mock.patch(
            'observabilityclient.prometheus_client.PrometheusAPIClient'
        ) as mock_client:
            self.controller.create_prometheus_client(self.conf)

            mock_client.assert_called_once_with('localhost:9090')
            mock_client.return_value.set_ca_cert.assert_called_once_with(True)
            mock_client.return_value.set_client_cert.assert_not_called()

    def test_create_prometheus_client_with_tls_with_key_only(self):
        """Test prometheus client creation with TLS with only ket file"""
        self.conf.set_override('use_tls', True, group='prometheus')
        self.conf.set_override('key_file', 'keyfile', group='prometheus')

        with mock.patch(
            'observabilityclient.prometheus_client.PrometheusAPIClient'
        ) as mock_client:
            self.controller.create_prometheus_client(self.conf)

            mock_client.assert_called_once_with('localhost:9090')
            mock_client.return_value.set_ca_cert.assert_called_once_with(True)
            mock_client.return_value.set_client_cert.assert_not_called()
