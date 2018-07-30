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
import copy
import testtools
from testtools import matchers

from cyborgclient.tests.unit import utils
from cyborgclient.v1 import deployables


DEPLOYABLE1 = {
    "instance_uuid": "", "assignable": True,
    "vendor": "test_vendor1",
    "parent_uuid": "1859ef92-90c9-462e-ba78-3fd8295aa390",
    "links": [
        {"href": "http://127.0.0.1:6666/v1/deployables/fake_uuid",
         "rel": "self"
         },
        {"href": "http://127.0.0.1:6666/deployables/fake_uuid",
         "rel": "bookmark"}],
    "updated_at": "2018-07-27T13:07:14+00:00",
    "interface_type": "pci",
    "uuid": "1859ef92-90c9-462e-ba78-3fd8295aa390",
    "name": "test_name1", "host": "host_test1",
    "version": "1", "board": "test_board1",
    "address": "test_addr1", "created_at": None,
    "type": "pf", "availability": "1",
    "root_uuid": "1859ef92-90c9-462e-ba78-3fd8295aa390"
}
DEPLOYABLE2 = {
    "instance_uuid": None, "assignable": False,
    "vendor": "test_vendor2",
    "parent_uuid": "5a7dfaf9-7f4e-42d0-bfac-b2f464110d9f",
    "links": [
        {"href": "http://127.0.0.1:6666/v1/deployables/fake_uuid",
         "rel": "self"},
        {"href": "http://127.0.0.1:6666/deployables/fake_uuid",
         "rel": "bookmark"}],
    "updated_at": "2018-07-27T19:51:18+00:00",
    "interface_type": "mdev",
    "uuid": "5a7dfaf9-7f4e-42d0-bfac-b2f464110d9f",
    "name": "test_name2", "host": "host_test2", "version": "2",
    "board": "test_board2", "address": "test_addr2",
    "created_at": None, "type": "vf", "availability": "1",
    "root_uuid": "5a7dfaf9-7f4e-42d0-bfac-b2f464110d9f"
}
ALLOC_DEPLOYABLE1 = {
    "instance_uuid": None, "assignable": False,
    "vendor": "test_vendor2",
    "parent_uuid": "5a7dfaf9-7f4e-42d0-bfac-b2f464110d9f",
    "links": [
        {"href": "http://127.0.0.1:6666/v1/deployables/fake_uuid",
         "rel": "self"},
        {"href": "http://127.0.0.1:6666/deployables/fake_uuid",
         "rel": "bookmark"}],
    "updated_at": "2018-07-27T19:51:18+00:00",
    "interface_type": "mdev",
    "uuid": "5a7dfaf9-7f4e-42d0-bfac-b2f464110d9f",
    "name": "test_name2", "host": "host_test2", "version": "2",
    "board": "test_board2", "address": "test_addr2",
    "created_at": None, "type": "vf", "availability": "1",
    "root_uuid": "5a7dfaf9-7f4e-42d0-bfac-b2f464110d9f"
}
fake_responses = {
    '/v1/accelerators/deployables':
    {
        'GET': (
            {},
            {'deployables': [DEPLOYABLE1, DEPLOYABLE2]},
        )
    },
    '/v1/accelerators/deployables/%s' % ALLOC_DEPLOYABLE1["uuid"]:
    {
        'PATCH': (
            {"instance_uuid": "fake_instance_uuid"},
            ALLOC_DEPLOYABLE1,
        ),
    },
    '/v1/accelerators/deployables?filters.field=limit&filters.value=2':
    {
        'GET': (
            {},
            {'deployables': [DEPLOYABLE1, DEPLOYABLE2]},
        )
    },
    '/v1/accelerators/deployables?filters.field=marker&filters.value=%s' %
    DEPLOYABLE1['uuid']:
    {
        'GET': (
            {},
            {'deployables': [DEPLOYABLE1, DEPLOYABLE2]},
        )
    }
}


class DeployableManagerTest(testtools.TestCase):

    def setUp(self):
        super(DeployableManagerTest, self).setUp()
        self.api = utils.FakeAPI(fake_responses)
        self.mgr = deployables.DeployableManager(self.api)

    def test_deployables_list(self):
        deployables = self.mgr.list()
        expect = [
            ('GET', '/v1/accelerators/deployables', {}, None),
        ]
        self.assertEqual(expect, self.api.calls)
        self.assertThat(deployables, matchers.HasLength(2))

    def _test_deployables_list_with_filters(self, limit=None, marker=None,
                                            sort_key=None, sort_dir=None,
                                            expect=[], **add_filters):
        deployables_filter = self.mgr.list(limit=limit, marker=marker,
                                           sort_key=sort_key,
                                           sort_dir=sort_dir, **add_filters)
        self.assertEqual(expect, self.api.calls)
        self.assertThat(deployables_filter, matchers.HasLength(2))

    def test_deployables_list_with_limit(self):
        expect = [
            ('GET', '/v1/accelerators/deployables?filters.field='
                    'limit&filters.value=2', {}, None),
        ]
        self._test_deployables_list_with_filters(
            limit=2,
            expect=expect)

    def test_deployables_list_with_marker(self):
        expect = [
            ('GET', '/v1/accelerators/deployables?filters.field=marker&'
                    'filters.value=%s' % DEPLOYABLE1['uuid'],
             {}, None),
        ]
        self._test_deployables_list_with_filters(
            marker=DEPLOYABLE1['uuid'],
            expect=expect)

    def test_deployables_allocation(self):
        dep_for_alloc = copy.deepcopy(ALLOC_DEPLOYABLE1)
        self.mgr.allocation(dep_for_alloc["uuid"], "fake_instance_uuid")
        expect = [
            ('PATCH', '/v1/accelerators/deployables/%s' %
             dep_for_alloc["uuid"],
             {}, [{'op': 'replace',
                   'path': '/instance_uuid',
                   'value': 'fake_instance_uuid'}])
        ]
        self.assertEqual(expect, self.api.calls)

    def test_deployables_deallocation(self):
        dep_for_dealloc = copy.deepcopy(ALLOC_DEPLOYABLE1)
        self.mgr.deallocation(dep_for_dealloc["uuid"])
        expect = [
            ('PATCH', '/v1/accelerators/deployables/%s' %
             dep_for_dealloc["uuid"],
             {}, [{'op': 'replace',
                   'path': '/instance_uuid',
                   'value': None}])
        ]
        self.assertEqual(expect, self.api.calls)
