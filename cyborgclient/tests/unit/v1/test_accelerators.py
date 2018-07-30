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
import testtools
from testtools import matchers

from cyborgclient.tests.unit import utils
from cyborgclient.v1 import accelerators

ACCELERATOR1 = {"user_id": "3a4b753552964978af7f76ce9fecf7d0",
                "description": "test", "links":
                [{"href": "http://127.0.0.1:6666/v1/accelerators/fake_uuid",
                          "rel": "self"},
                 {"href": "http://127.0.0.1:6666/accelerators/fake_uuid",
                  "rel": "bookmark"}],
                "acc_capability": "test",
                "created_at": "2018-07-20T07:45:04+00:00",
                "vendor_id": "test", "updated_at": None,
                "acc_type": None, "name": "test-cyborg-create",
                "product_id": "test", "device_type": "test", "remotable": 1,
                "project_id": None,
                "uuid": "4cc55aab-dac6-486f-ad14-284c8e554589"}

ACCELERATOR2 = {"user_id": "3a4b753552964978af7f76ce9fecf7d0",
                "description": "test", "links":
                [{"href": "http://127.0.0.1:6666/v1/accelerators/fake_uuid",
                  "rel": "self"},
                 {"href": "http://127.0.0.1:6666/accelerators/fake_uuid",
                  "rel": "bookmark"}],
                "acc_capability": "test",
                "created_at": "2018-07-20T08:11:14+00:00",
                "vendor_id": "test", "updated_at": None,
                "acc_type": None, "name": "test-cyborg-create",
                "product_id": "test", "device_type": "test", "remotable": 1,
                "project_id": None,
                "uuid": "a444397a-deba-4c94-984f-ce35fbcdec42"}

fake_responses = {
    '/v1/accelerators':
    {
        'GET': (
            {},
            {'accelerators': [ACCELERATOR1, ACCELERATOR2]},
        )
    }
}


class AcceleratorManagerTest(testtools.TestCase):

    def setUp(self):
        super(AcceleratorManagerTest, self).setUp()
        self.api = utils.FakeAPI(fake_responses)
        self.mgr = accelerators.AcceleratorManager(self.api)

    def test_accelerators_list(self):
        accelerators = self.mgr.list()
        expect = [
            ('GET', '/v1/accelerators', {}, None),
        ]
        self.assertEqual(expect, self.api.calls)
        self.assertThat(accelerators, matchers.HasLength(2))
