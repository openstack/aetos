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

from aetos.controllers.api.v1 import base

LOG = log.getLogger(__name__)


class DeleteController(base.Base):
    # NOTE(jwysogla): the delete/ endpoint expects a `match[]` argument,
    # which is making the use of wsexpose difficult, so a plain
    # pecan.expose is used instead, with handling of the arguments
    # as a dictionary inside the function.
    @pecan.expose(content_type='application/json')
    def post(self, **args):
        """Delete endpoint"""
        # TODO(jwysogla):
        # - policy handling
        # - handle unknown, missing and optional parameters
        # - handle unsuccessful calls to prometheus
        self.create_prometheus_client(pecan.request.cfg)
        matches = args.get('match[]', [])
        start = args.get('start', None)
        end = args.get('end', None)
        self.prometheus_client.delete(matches, start, end)
