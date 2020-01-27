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

from cyborgclient.osc.v2 import device as osc_device
from cyborgclient.tests.unit.osc.v2 import fakes as acc_fakes


class TestDevice(acc_fakes.TestAccelerator):

    def setUp(self):
        super(TestDevice, self).setUp()

        self.mock_acc_client = self.app.client_manager.accelerator
        self.mock_acc_client.reset_mock()


class TestDeviceList(TestDevice):

    def setUp(self):
        super(TestDeviceList, self).setUp()

        self.mock_acc_client.devices.return_value = [
            acc_fakes.FakeAcceleratorResource(
                None,
                copy.deepcopy(acc_fakes.DEVICE),
                loaded=True)
        ]

        self.cmd = osc_device.ListDevice(self.app, None)

    def test_device_list(self):
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {}

        self.mock_acc_client.devices.assert_called_with(**kwargs)

        collist = (
            'uuid',
            'type',
            'vendor',
            'hostname',
            'std_board_info'
        )
        self.assertEqual(collist, columns)

        datalist = [(
            acc_fakes.device_uuid,
            acc_fakes.device_type,
            acc_fakes.device_vendor,
            acc_fakes.device_hostname,
            acc_fakes.device_std_board_info,
        ), ]
        self.assertEqual(datalist, list(data))

    def test_device_list_long(self):
        arglist = ['--long']
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {}

        self.mock_acc_client.devices.assert_called_with(**kwargs)

        collist = (
            'created_at',
            'updated_at',
            'uuid',
            'type',
            'vendor',
            'model',
            'hostname',
            'std_board_info',
            'vendor_board_info',
        )
        self.assertEqual(collist, columns)

        datalist = [(
            acc_fakes.device_created_at,
            acc_fakes.device_updated_at,
            acc_fakes.device_uuid,
            acc_fakes.device_type,
            acc_fakes.device_vendor,
            acc_fakes.device_model,
            acc_fakes.device_hostname,
            acc_fakes.device_std_board_info,
            acc_fakes.device_vendor_board_info,
        ), ]
        self.assertEqual(datalist, list(data))
