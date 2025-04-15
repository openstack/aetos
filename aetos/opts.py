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

from keystoneauth1 import loading
from oslo_config import cfg

import aetos.controllers.api.v1.base
import aetos.keystone_client
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
         itertools.chain(OPTS,
                         aetos.controllers.api.v1.base.OPTS)),
        ('service_credentials', aetos.keystone_client.OPTS),
    ]


def list_keystoneauth_opts():
    # NOTE(sileht): the configuration file contains only the options
    # for the password plugin that handles keystone v2 and v3 API
    # with discovery. But other options are possible.
    return [('service_credentials', (
            loading.get_auth_common_conf_options() +
            loading.get_auth_plugin_conf_options('password')))]
