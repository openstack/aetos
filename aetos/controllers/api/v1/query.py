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
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from aetos.controllers.api.v1 import base

LOG = log.getLogger(__name__)


class QueryController(base.Base):
    @wsme_pecan.wsexpose(wtypes.text, wtypes.text)
    def get(self, query):
        """Query endpoint"""
        # TODO(jwysogla):
        # - policy handling
        # - query modification
        modified_query = query

        LOG.debug("Unmodified query: %s", query)
        LOG.debug("Query sent to prometheus: %s", modified_query)

        result = self.prometheus_client._get("query",
                                             {"query": modified_query})

        LOG.debug("Data received from prometheus: %s", str(result))
        return result
