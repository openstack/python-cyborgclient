# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
import copy

from cyborgclient.osc.v2 import deployable as osc_deployable
from cyborgclient.tests.unit.osc.v2 import fakes as acc_fakes


class TestDeployable(acc_fakes.TestAccelerator):

    def setUp(self):
        super(TestDeployable, self).setUp()

        self.mock_acc_client = self.app.client_manager.accelerator
        self.mock_acc_client.reset_mock()


class TestDeployableList(TestDeployable):

    def setUp(self):
        super(TestDeployableList, self).setUp()

        self.mock_acc_client.deployables.return_value = [
            acc_fakes.FakeAcceleratorResource(
                None,
                copy.deepcopy(acc_fakes.DEPLOYABLE),
                loaded=True)
        ]

        self.cmd = osc_deployable.ListDeployable(self.app, None)

    def test_deployable_list(self):
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {}

        self.mock_acc_client.deployables.assert_called_with(**kwargs)

        collist = (
            'uuid',
            'name',
            'device_id'
        )
        self.assertEqual(collist, columns)

        datalist = [(
            acc_fakes.deployable_uuid,
            acc_fakes.deployable_name,
            acc_fakes.deployable_device_id,
        ), ]
        self.assertEqual(datalist, list(data))

    def test_deployable_list_long(self):
        arglist = ['--long']
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {}

        self.mock_acc_client.deployables.assert_called_with(**kwargs)

        collist = (
            'created_at',
            'updated_at',
            'uuid',
            'parent_id',
            'root_id',
            'name',
            'num_accelerators',
            'device_id'
        )
        self.assertEqual(collist, columns)

        datalist = [(
            acc_fakes.deployable_created_at,
            acc_fakes.deployable_updated_at,
            acc_fakes.deployable_uuid,
            acc_fakes.deployable_parent_id,
            acc_fakes.deployable_root_id,
            acc_fakes.deployable_name,
            acc_fakes.deployable_num_accelerators,
            acc_fakes.deployable_device_id,
        ), ]
        self.assertEqual(datalist, list(data))
