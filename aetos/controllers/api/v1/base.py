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

from pecan import rest
from wsme import exc

from observabilityclient import prometheus_client
from observabilityclient import rbac as obsc_rbac
from oslo_config import cfg
from oslo_log import log
from oslo_utils import netutils

LOG = log.getLogger(__name__)


PROMETHEUS_OPTS = [
    cfg.StrOpt(
        'host',
        default="localhost",
        help="The host of Prometheus"),
    cfg.PortOpt(
        'port',
        default=9090,
        help="The port of Prometheus"),
    cfg.StrOpt(
        'cert_file',
        help="Path to a client cert for establishing TLS connections to "
             "Prometheus."
        ),
    cfg.StrOpt(
        'key_file',
        help="Path to a client key for establishing TLS connections to "
             "Prometheus."
        ),
    cfg.StrOpt(
        'ca_file',
        help="Path to a CA cert for establishing TLS connections to "
             "Prometheus. This is optional, if this isn't set, then "
             "default system CA certificates will be used."
        ),
    cfg.BoolOpt(
        'use_tls',
        default=False,
        help="Whether TLS should be used when connecting to Prometheus."
        ),
    cfg.StrOpt(
        'project_label_name',
        default="project",
        help="Label name used to store project IDs in Prometheus. "
             "This will be used for distinguishing between projects "
             "for multi-tenancy reasons."
        )
]


class ServerSideError(exc.ClientSideError):
    def __init__(self, error, status_code=500):
        super().__init__(error, status_code, 'Server')


class Base(rest.RestController):
    def create_prometheus_client(self, conf):
        host = netutils.escape_ipv6(conf.prometheus.host)
        port = conf.prometheus.port
        cert_file = conf.prometheus.cert_file
        key_file = conf.prometheus.key_file
        ca_file = conf.prometheus.ca_file
        use_tls = conf.prometheus.use_tls

        if (ca_file or key_file or cert_file) and not use_tls:
            LOG.warning("CA/Cert/Key file specified but TLS disabled - "
                        "Ca/Cert/Key file will be ignored")

        url = f"{host}:{port}"
        self.prometheus_client = prometheus_client.PrometheusAPIClient(url)

        if use_tls:
            if ca_file:
                LOG.debug("TLS for Prometheus connection enabled with CA "
                          "file: %s", ca_file)
                self.prometheus_client.set_ca_cert(ca_file)
            else:
                LOG.debug("TLS for Prometheus connection enabled with system "
                          "default CA certificates")
                self.prometheus_client.set_ca_cert(True)

            if cert_file and key_file:
                self.prometheus_client.set_client_cert(cert_file, key_file)
            elif cert_file or key_file:
                LOG.warning("Only one of cert_file and key_file is set. "
                            "Set the two options or both are ignored.")

        super(object, self).__init__()

    def process_matches(self, matches, privileged, project_id, conf):
        # Ensure matches is always a list
        if not isinstance(matches, list):
            matches = [matches]

        # If user has high privileges, return matches as-is
        if privileged:
            return matches

        promQLRbac = obsc_rbac.PromQLRbac(
            self.prometheus_client, project_id,
            conf.prometheus.project_label_name)

        if matches == []:
            return promQLRbac.append_rbac_labels('')

        # Apply RBAC modification to each match
        metric_names = self.prometheus_client.label_values("__name__")
        modified_matches = []
        for match in matches:
            modified_matches.append(
                promQLRbac.modify_query(match, metric_names=metric_names))

        return modified_matches

    @staticmethod
    def _get_correct_exception(e):
        if e.resp.status_code // 100 == 4:
            return exc.ClientSideError(str(e), e.resp.status_code)
        elif e.resp.status_code // 100 == 5:
            return ServerSideError(str(e), e.resp.status_code)
        else:
            return ServerSideError(
                (f'Aetos received an unexpected status code from '
                 f'prometheus: "{e}"'),
                501
            )

    def prometheus_get(self, endpoint, params=None):
        try:
            return self.prometheus_client._get(endpoint, params)
        except prometheus_client.PrometheusAPIClientError as e:
            if e.resp.status_code != 204:
                # NOTE(jwysogla): Prometheus can return empty responses, which
                # is expected, so ignore the 204 status code and reraise on
                # all others.
                raise Base._get_correct_exception(e)

    def prometheus_post(self, endpoint, params=None):
        try:
            return self.prometheus_client._post(endpoint, params)
        except prometheus_client.PrometheusAPIClientError as e:
            if e.resp.status_code != 204:
                # NOTE(jwysogla): Prometheus can return empty responses, which
                # is expected, so ignore the 204 status code and reraise on
                # all others.
                raise Base._get_correct_exception(e)
