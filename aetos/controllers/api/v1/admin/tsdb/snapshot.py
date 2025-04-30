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

from oslo_log import log
import pecan
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from aetos.controllers.api.v1 import base

LOG = log.getLogger(__name__)


class SnapshotController(base.Base):
    @wsme_pecan.wsexpose(wtypes.text)
    def post(self):
        """Snapshot endpoint"""
        # TODO(jwysogla)
        # - check policies. This should be accessible to admin only.
        # - handle unsuccessful requests
        self.create_prometheus_client(pecan.request.cfg)
        result = self.prometheus_client._post("admin/tsdb/snapshot")
        LOG.debug("Data received from prometheus: %s", str(result))
        return result
