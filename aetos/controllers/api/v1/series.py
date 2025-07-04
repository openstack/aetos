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

import json
from observabilityclient import rbac as obsc_rbac
from oslo_log import log
import pecan
from webob import exc
from wsme import exc as wsme_exc

from aetos.controllers.api.v1 import base
from aetos import rbac

LOG = log.getLogger(__name__)


class SeriesController(base.Base):
    # NOTE(jwysogla): the series/ endpoint expects a `match[]` argument,
    # which is making the use of wsexpose difficult, so a plain
    # pecan.expose is used instead, with handling of the arguments
    # as a dictionary inside the function.
    @pecan.expose(content_type='application/json')
    def get(self, *args, **kwargs):
        """Series endpoint"""
        target = {"project_id": pecan.request.headers.get('X-Project-Id')}
        try:
            rbac.enforce('series:all_projects', pecan.request.headers,
                         pecan.request.enforcer, target)
            privileged = True
            LOG.debug(
                "Received a high privilege request for the series endpoint"
            )
        except exc.HTTPForbidden:
            rbac.enforce('series', pecan.request.headers,
                         pecan.request.enforcer, target)
            privileged = False
            LOG.debug(
                "Received a low privilege request for the series endpoint"
            )

        self.create_prometheus_client(pecan.request.cfg)
        status_code = 200

        if len(args) != 0:
            pecan.response.status = 404
            return json.dumps("page not found")

        matches = kwargs.get('match[]', [])
        if not isinstance(matches, list):
            matches = [matches]
        LOG.debug("Unmodified matches received: %s", str(matches))

        modified_matches = matches
        if not privileged:
            promQLRbac = obsc_rbac.PromQLRbac(
                self.prometheus_client,
                target['project_id']
            )
            modified_matches = []
            for match in matches:
                modified_matches.append(promQLRbac.modify_query(match))

        LOG.debug("Matches sent to prometheus: %s", str(modified_matches))

        try:
            result = self.prometheus_get("series",
                                         {'match[]': modified_matches})
        except wsme_exc.ClientSideError as e:
            # NOTE(jwysogla): We need a special handling of the exceptions,
            # because we don't use wsexpose as with most of other endpoints.
            status_code = e.code
            result = e.msg
        LOG.debug("Data received from prometheus: %s", str(result))

        pecan.response.status = status_code
        return json.dumps(result)
