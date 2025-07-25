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
from oslo_utils import netutils


OPTS = [
    cfg.StrOpt(
        'prometheus_host',
        default="localhost",
        help="The host of Prometheus"),
    cfg.PortOpt(
        'prometheus_port',
        default=9090,
        help="The port of Prometheus"),
    # TODO(jwysogla): TLS Prometheus options
]


class ServerSideError(exc.ClientSideError):
    def __init__(self, error, status_code=500):
        super().__init__(error, status_code, 'Server')


class Base(rest.RestController):
    def create_prometheus_client(self, conf):
        # TODO(jwysogla): Handle TLS
        prometheus_host = netutils.escape_ipv6(conf.prometheus_host)
        prometheus_port = conf.prometheus_port
        url = f"{prometheus_host}:{prometheus_port}"
        self.prometheus_client = prometheus_client.PrometheusAPIClient(url)
        super(object, self).__init__()

    def process_matches(self, matches, privileged, project_id):
        # Ensure matches is always a list
        if not isinstance(matches, list):
            matches = [matches]

        # If user has high privileges, return matches as-is
        if privileged:
            return matches

        promQLRbac = obsc_rbac.PromQLRbac(self.prometheus_client, project_id)

        if matches == []:
            return promQLRbac.append_rbac_labels('')

        # Apply RBAC modification to each match
        modified_matches = []
        for match in matches:
            modified_matches.append(promQLRbac.modify_query(match))

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
