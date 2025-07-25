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

import warnings

from oslotest import base


class TestCase(base.BaseTestCase):

    """Test case base class for all unit tests."""

    def setUp(self):
        super().setUp()
        # FIXME(stephenfin): Determine if we need to replace use of best_match
        warnings.filterwarnings(
            'ignore',
            module='webob',
            message='The behavior of AcceptValidHeader.best_match is ',
            category=DeprecationWarning,
        )

        # FIXME(stephenfin): Determine if we need to replace use of best_match
        warnings.filterwarnings(
            'ignore',
            module='webob',
            message='The behavior of .best_match for the Accept classes is ',
            category=DeprecationWarning,
        )
