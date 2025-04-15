# Copyright 2025 Red Hat, Inc.
# Copyright 2012 New Dream Network, LLC (DreamHost)
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
import uuid

from oslo_log import log
from paste import deploy
import pecan

from aetos import hooks
from aetos import middleware
from aetos import service

LOG = log.getLogger(__name__)


# NOTE(sileht): pastedeploy uses ConfigParser to handle
# global_conf, since python 3 ConfigParser doesn't
# allow storing object as config value, only strings are
# permit, so to be able to pass an object created before paste load
# the app, we store them into a global var. But the each loaded app
# store it's configuration in unique key to be concurrency safe.
global APPCONFIGS
APPCONFIGS = {}


def setup_app(root, conf):
    app_hooks = [hooks.ConfigHook(conf),
                 hooks.TranslationHook()]
    return pecan.make_app(
        root,
        hooks=app_hooks,
        wrap_app=middleware.ParsableErrorMiddleware,
        guess_content_type_from_ext=False
    )


def load_app(conf):
    global APPCONFIGS

    # Build the WSGI app
    cfg_path = conf.paste_config
    if not os.path.isabs(cfg_path):
        cfg_path = conf.find_file(cfg_path)

    if cfg_path is None or not os.path.exists(cfg_path):
        LOG.debug("No api-paste configuration file found! Using default.")
        cfg_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "api-paste.ini"))

    config = dict(conf=conf)
    configkey = str(uuid.uuid4())
    APPCONFIGS[configkey] = config

    LOG.info("WSGI config used: %s", cfg_path)
    return deploy.loadapp("config:" + cfg_path,
                          name="aetos+" + (
                              conf.auth_mode
                              if conf.auth_mode else "noauth"
                          ),
                          global_conf={'configkey': configkey})


def app_factory(global_config, **local_conf):
    global APPCONFIGS
    appconfig = APPCONFIGS.get(global_config.get('configkey'))
    return setup_app(root=local_conf.get('root'), **appconfig)


def build_wsgi_app(argv=None):
    conf = service.prepare_service(argv=argv)
    conf.log_opt_values(LOG, log.DEBUG)
    return load_app(conf)
