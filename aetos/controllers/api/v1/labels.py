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

from oslo_log import log
import pecan
from webob import exc
from wsme import exc as wsme_exc

from aetos.controllers.api.v1 import base
from aetos import rbac

LOG = log.getLogger(__name__)


class LabelsController(base.Base):
    @pecan.expose(content_type='application/json')
    def get(self, *args, **kwargs):
        """Labels endpoint"""
        target = {"project_id": pecan.request.headers.get('X-Project-Id')}
        try:
            rbac.enforce('labels:all_projects', pecan.request.headers,
                         pecan.request.enforcer, target)
            privileged = True
            LOG.debug(
                "Received a high privilege request for the labels endpoint"
            )
        except exc.HTTPForbidden:
            rbac.enforce('labels', pecan.request.headers,
                         pecan.request.enforcer, target)
            privileged = False
            LOG.debug(
                "Received a low privilege request for the labels endpoint"
            )

        status_code = 200

        if len(args) != 0:
            pecan.response.status = 404
            return json.dumps("page not found")

        matches = kwargs.get('match[]', [])

        self.create_prometheus_client(pecan.request.cfg)

        processed_matches = self.process_matches(
            matches, privileged, target['project_id'], pecan.request.cfg
        )

        LOG.debug("Matches sent to prometheus: %s", str(processed_matches))
        try:
            result = self.prometheus_get(
                "labels", {"match[]": processed_matches}
            )
        except wsme_exc.ClientSideError as e:
            status_code = e.code
            result = e.msg

        LOG.debug("Data received from prometheus: %s", str(result))

        pecan.response.status = status_code
        return json.dumps(result)
