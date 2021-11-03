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

from cyborgclient import exceptions as exc
from cyborgclient.osc.v2 import device_profile as osc_device_profile
from cyborgclient.tests.unit.osc.v2 import fakes as acc_fakes


class TestDeviceProfile(acc_fakes.TestAccelerator):

    def setUp(self):
        super(TestDeviceProfile, self).setUp()

        self.mock_acc_client = self.app.client_manager.accelerator
        self.mock_acc_client.reset_mock()


class TestDeviceProfileList(TestDeviceProfile):

    def setUp(self):
        super(TestDeviceProfileList, self).setUp()

        self.mock_acc_client.device_profiles.return_value = [
            acc_fakes.FakeAcceleratorResource(
                None,
                copy.deepcopy(acc_fakes.DEVICE_PROFILE),
                loaded=True)
        ]

        self.cmd = osc_device_profile.ListDeviceProfile(self.app, None)

    def test_device_profile_list(self):
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {}

        self.mock_acc_client.device_profiles.assert_called_with(**kwargs)

        collist = (
            'uuid',
            'name',
            'groups',
            'description'
        )
        self.assertEqual(collist, columns)

        datalist = [(
            acc_fakes.device_profile_uuid,
            acc_fakes.device_profile_name,
            acc_fakes.device_profile_groups,
            acc_fakes.device_profile_description,
        ), ]
        self.assertEqual(datalist, list(data))

    def test_device_profile_list_long(self):
        arglist = ['--long']
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {}

        self.mock_acc_client.device_profiles.assert_called_with(**kwargs)

        collist = (
            'created_at',
            'updated_at',
            'uuid',
            'name',
            'groups',
            'description'
        )
        self.assertEqual(collist, columns)

        datalist = [(
            acc_fakes.device_profile_created_at,
            acc_fakes.device_profile_updated_at,
            acc_fakes.device_profile_uuid,
            acc_fakes.device_profile_name,
            acc_fakes.device_profile_groups,
            acc_fakes.device_profile_description,
        ), ]
        self.assertEqual(datalist, list(data))


class TestDeviceProfileShow(TestDeviceProfile):

    def setUp(self):
        super(TestDeviceProfileShow, self).setUp()
        self.cmd = osc_device_profile.ShowDeviceProfile(self.app, None)

    def test_device_profile_show_with_name(self):
        arg_list = [acc_fakes.device_profile_name]
        verify_list = []
        parsed_args = self.check_parser(self.cmd, arg_list, verify_list)
        result = self.assertRaises(exc.CommandError,
                                   self.cmd.take_action,
                                   parsed_args)
        self.assertIn("Only UUID of device_profile allowed. "
                      "Invalid input: fake_devprof_name", str(result))


class TestDeviceProfileCreate(TestDeviceProfile):

    def setUp(self):
        super(TestDeviceProfileCreate, self).setUp()

        fake_dp = acc_fakes.FakeAcceleratorResource(
            None,
            copy.deepcopy(acc_fakes.DEVICE_PROFILE),
            loaded=True)
        self.mock_acc_client.create_device_profile.return_value = fake_dp
        self.mock_acc_client.get_device_profile.return_value = fake_dp
        self.cmd = osc_device_profile.CreateDeviceProfile(self.app, None)

    def test_device_profile_create(self):
        arglist = ['test', '[]']
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {'name': 'test', 'groups': [], 'description': None}

        self.mock_acc_client.create_device_profile.assert_called_with(**kwargs)

        collist = (
            'created_at',
            'updated_at',
            'uuid',
            'name',
            'groups',
            'description'
        )
        self.assertEqual(collist, columns)

        datalist = [
            acc_fakes.device_profile_created_at,
            acc_fakes.device_profile_updated_at,
            acc_fakes.device_profile_uuid,
            acc_fakes.device_profile_name,
            acc_fakes.device_profile_groups,
            acc_fakes.device_profile_description,
        ]
        self.assertEqual(datalist, list(data))
