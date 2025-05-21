# Copyright 2010-2011 OpenStack Foundation
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
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

from unittest import mock
import webtest
import wsme

from oslo_config import fixture as fixture_config

from aetos import app
from aetos import service
from aetos.tests import base


def quiet_expected_exception():
    # NOTE(jwysogla): WSME will output a traceback to stdout whenever an
    # exception resulting in 5** http status code is raised. There are a
    # few tests, which expect various 5** statuses. Use this to get rid of
    # the unnecesssary tracebacks in the test output.
    r = dict(faultcode=500,
             faultstring='faultstring',
             debuginfo=None)
    return mock.patch.object(wsme.api, 'format_exception',
                             return_value=r)


class TestCase(base.TestCase):

    """Test case base class for all functional tests."""
    PATH_PREFIX = '/api/v1'

    def setUp(self):
        super().setUp()
        self.admin_auth_headers = {'X-User-Id': 'admin_user',
                                   'X-Project-Id': 'project1',
                                   'X-Roles': 'admin'}

        self.reader_auth_headers = {'X-User-Id': 'reader_user',
                                    'X-Project-Id': 'project1',
                                    'X-Roles': 'reader'}

        conf = service.prepare_service(argv=[], config_files=[])
        self.CONF = self.useFixture(fixture_config.Config(conf)).conf
        self.CONF.set_override('auth_mode', None, group=None)

        self.app = webtest.TestApp(app.load_app(self.CONF))

    def tearDown(self):
        super().tearDown()

    def post_json(self, path, params, expect_errors=False, headers=None,
                  method="post", extra_environ=None, status=None):
        """Sends simulated HTTP POST request to Pecan test app.

        :param path: url path of target service
        :param params: content for wsgi.input of request
        :param expect_errors: boolean value whether an error is expected based
                              on request
        :param headers: A dictionary of headers to send along with the request
        :param method: Request method type. Appropriate method function call
                       should be used rather than passing attribute in.
        :param extra_environ: A dictionary of environ variables to send along
                              with the request
        :param status: Expected status code of response
        """
        full_path = self.PATH_PREFIX + path
        response = getattr(self.app, "%s_json" % method)(
            str(full_path),
            params=params,
            headers=headers,
            status=status,
            extra_environ=extra_environ,
            expect_errors=expect_errors
        )
        return response

    def get_json(self, path, expect_errors=False, headers=None,
                 extra_environ=None, status=None, **params):
        """Sends simulated HTTP GET request to Pecan test app.

        :param path: url path of target service
        :param expect_errors: boolean value whether an error is expected based
                              on request
        :param headers: A dictionary of headers to send along with the request
        :param extra_environ: A dictionary of environ variables to send along
                              with the request
        :param status: Expected status code of response
        :param params: content for wsgi.input of request
        """
        full_path = self.PATH_PREFIX + path
        response = self.app.get(full_path,
                                params=params,
                                headers=headers,
                                extra_environ=extra_environ,
                                expect_errors=expect_errors,
                                status=status)
        if not expect_errors:
            response = response.json
        return response


class ErrorResponse():
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        return {"status": "error", "error": "test_error"}
