#
# Copyright 2025 Red Hat, Inc
# Copyright 2014-2015 eNovance
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
import itertools

from oslo_config import cfg

import aetos.controllers.api.v1.base
import aetos.service


OPTS = [
    cfg.StrOpt(
        'paste_config',
        default='api-paste.ini',
        help="Configuration file for WSGI definition of API."),
    cfg.StrOpt(
        'auth_mode',
        default="keystone",
        help="Authentication mode to use. Unset to disable authentication"),
]


def list_opts():
    return [
        ('DEFAULT',
         itertools.chain(OPTS)),
        ('prometheus',
         itertools.chain(aetos.controllers.api.v1.base.PROMETHEUS_OPTS)),
    ]
