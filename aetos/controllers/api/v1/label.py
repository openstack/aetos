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

from observabilityclient import rbac as obsc_rbac
from oslo_log import log
import pecan
from webob import exc
from wsme.exc import ClientSideError
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from aetos.controllers.api.v1 import base
from aetos import rbac

LOG = log.getLogger(__name__)


class LabelController(base.Base):
    @wsme_pecan.wsexpose(wtypes.text, wtypes.text, wtypes.text)
    def get(self, name, values):
        """Label endpoint"""
        target = {"project_id": pecan.request.headers.get('X-Project-Id')}
        try:
            rbac.enforce('label:all_projects', pecan.request.headers,
                         pecan.request.enforcer, target)
            privileged = True
            LOG.debug(
                "Received a high privilege request for the label endpoint"
            )
        except exc.HTTPForbidden:
            rbac.enforce('label', pecan.request.headers,
                         pecan.request.enforcer, target)
            privileged = False
            LOG.debug(
                "Received a low privilege request for the label endpoint"
            )

        if values != "values":
            raise ClientSideError("page not found", 404)

        self.create_prometheus_client(pecan.request.cfg)

        LOG.debug("Label name: %s", name)
        if privileged:
            result = self.prometheus_get(f"label/{name}/values")
        else:
            promQLRbac = obsc_rbac.PromQLRbac(
                self.prometheus_client,
                target['project_id']
            )
            result = self.prometheus_get(
                f"label/{name}/values",
                {"match[]": promQLRbac.append_rbac_labels('')}
            )
        LOG.debug("Data received from prometheus: %s", str(result))
        return result
