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
import pecan
from wsme import exc

from oslo_log import log

from aetos.controllers.api.v1 import base

LOG = log.getLogger(__name__)


class SeriesController(base.Base):
    # NOTE(jwysogla): the series/ endpoint expects a `match[]` argument,
    # which is making the use of wsexpose difficult, so a plain
    # pecan.expose is used instead, with handling of the arguments
    # as a dictionary inside the function.
    @pecan.expose(content_type='application/json')
    def get(self, **args):
        """Series endpoint"""
        # TODO(jwysogla):
        # - policy handling
        # - match modification
        # - handle unknown parameters
        self.create_prometheus_client(pecan.request.cfg)
        status_code = 200

        matches = args['match[]']
        modified_matches = matches

        LOG.debug("Unmodified matches received: %s", str(matches))
        LOG.debug("Matches sent to prometheus: %s", str(modified_matches))

        try:
            result = self.prometheus_get("series",
                                         {'match[]': modified_matches})
        except exc.ClientSideError as e:
            # NOTE(jwysogla): We need a special handling of the exceptions,
            # because we don't use wsexpose as with most of other endpoints.
            status_code = e.code
            result = e.msg
        LOG.debug("Data received from prometheus: %s", str(result))

        pecan.response.status = status_code
        return json.dumps(result)
