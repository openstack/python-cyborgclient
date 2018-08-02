#
# Copyright 2013 OpenStack LLC.
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

from cyborgclient.common import utils
from cyborgclient.tests.unit import utils as test_utils


class CommonFiltersTest(test_utils.BaseTestCase):
    def test_limit(self):
        result = utils.common_filters(limit=42)
        self.assertEqual(['filters.field=limit', 'filters.value=42'], result)

    def test_limit_0(self):
        result = utils.common_filters(limit=0)
        self.assertEqual(['filters.field=limit', 'filters.value=0'], result)

    def test_limit_negative_number(self):
        result = utils.common_filters(limit=-2)
        self.assertEqual(['filters.field=limit', 'filters.value=-2'], result)

    def test_other(self):
        for key in ('marker', 'sort_key', 'sort_dir'):
            result = utils.common_filters(**{key: 'test'})
            self.assertEqual(['filters.field=%s' % key, 'filters.value=test'],
                             result)
