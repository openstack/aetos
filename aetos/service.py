#
# Copyright 2013-2025 Red Hat, Inc
# Copyright 2012-2015 eNovance <licensing@enovance.com>
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
import os

from keystoneauth1 import loading as ka_loading
from oslo_config import cfg
from oslo_db import options as db_options
import oslo_i18n
from oslo_log import log
from oslo_policy import opts as policy_opts

from aetos.conf import defaults
from aetos import keystone_client
from aetos import version


def prepare_service(argv=None, config_files=None):
    conf = cfg.ConfigOpts()
    oslo_i18n.enable_lazy()
    log.register_options(conf)
    log_levels = (
        conf.default_log_levels +
        [
            'futurist=INFO',
            'keystoneclient=INFO',
            'oslo_db.sqlalchemy=WARN',
            'cotyledon=INFO'
        ]
    )
    log.set_defaults(default_log_levels=log_levels)
    defaults.set_cors_middleware_defaults()
    db_options.set_defaults(conf)
    policy_opts.set_defaults(conf, policy_file=os.path.abspath(
        os.path.join(os.path.dirname(__file__), "api", "policy.yaml")))
    from aetos import opts
    # Register our own Aetos options
    for group, options in opts.list_opts():
        conf.register_opts(list(options),
                           group=None if group == "DEFAULT" else group)
    keystone_client.register_keystoneauth_opts(conf)

    conf(argv, project='aetos', validate_default_values=True,
         default_config_files=config_files,
         version=version.version_info.version_string())

    ka_loading.load_auth_from_conf_options(conf, "service_credentials")
    log.setup(conf, 'aetos')

    return conf
