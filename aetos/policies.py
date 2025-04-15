# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from oslo_config import cfg
from oslo_policy import policy

RULE_CONTEXT_IS_ADMIN = 'rule:context_is_admin'
RULE_ADMIN_OR_OWNER = 'rule:context_is_admin or project_id:%(project_id)s'
UNPROTECTED = ''

# Constants that represent common personas.
PROJECT_ADMIN = 'role:admin and project_id:%(project_id)s'
PROJECT_MEMBER = 'role:member and project_id:%(project_id)s'
PROJECT_READER = 'role:reader and project_id:%(project_id)s'

rules = [
    policy.RuleDefault(
        name="segregation",
        check_str=RULE_CONTEXT_IS_ADMIN),

    # TODO(jwysogla): Add policies. Below is an example
    # taken from Aodh

    # policy.DocumentedRuleDefault(
    #    name="telemetry:get_alarm",
    #    check_str=PROJECT_READER,
    #    scope_types=['project'],
    #    description='Get an alarm.',
    #    operations=[
    #        {
    #            'path': '/v2/alarms/{alarm_id}',
    #            'method': 'GET'
    #        }
    #    ],
    #    deprecated_rule=deprecated_get_alarm
    #
    # ),
]


def list_rules():
    return rules


def init(conf):
    enforcer = policy.Enforcer(conf, default_rule="default")
    enforcer.register_defaults(list_rules())
    return enforcer


def get_enforcer():
    # This method is used by oslopolicy CLI scripts in order to generate policy
    # files from overrides on disk and defaults in code.
    cfg.CONF([], project='aetos')
    return init(cfg.CONF)
