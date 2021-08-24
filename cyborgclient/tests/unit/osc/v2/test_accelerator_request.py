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

from openstack import exceptions as sdk_exc

from cyborgclient import exceptions as exc
from cyborgclient.osc.v2 import accelerator_request as osc_accelerator_request
from cyborgclient.tests.unit.osc.v2 import fakes as acc_fakes


class TestAcceleratorRequest(acc_fakes.TestAccelerator):

    def setUp(self):
        super(TestAcceleratorRequest, self).setUp()

        self.mock_acc_client = self.app.client_manager.accelerator
        self.mock_acc_client.reset_mock()


class TestAcceleratorRequestList(TestAcceleratorRequest):

    def setUp(self):
        super(TestAcceleratorRequestList, self).setUp()

        self.mock_acc_client.accelerator_requests.return_value = [
            acc_fakes.FakeAcceleratorResource(
                None,
                copy.deepcopy(acc_fakes.ACCELERATOR_REQUEST),
                loaded=True)
        ]

        self.cmd = osc_accelerator_request.ListAcceleratorRequest(
            self.app, None
        )

    def test_accelerator_request_list(self):
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {}

        self.mock_acc_client.accelerator_requests.assert_called_with(**kwargs)

        collist = (
            'uuid',
            'state',
            'device_profile_name',
            'instance_uuid',
            'attach_handle_type',
            'attach_handle_info',
        )
        self.assertEqual(collist, columns)

        datalist = [(
            acc_fakes.accelerator_request_uuid,
            acc_fakes.accelerator_request_state,
            acc_fakes.accelerator_request_device_profile_name,
            acc_fakes.accelerator_request_instance_uuid,
            acc_fakes.accelerator_request_attach_handle_type,
            acc_fakes.accelerator_request_attach_handle_info,
        ), ]
        self.assertEqual(datalist, list(data))

    def test_accelerator_request_list_long(self):
        arglist = ['--long']
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {}

        self.mock_acc_client.accelerator_requests.assert_called_with(**kwargs)

        collist = (
            'uuid',
            'state',
            'device_profile_name',
            'hostname',
            'device_rp_uuid',
            'instance_uuid',
            'attach_handle_type',
            'attach_handle_info',
        )
        self.assertEqual(collist, columns)

        datalist = [(
            acc_fakes.accelerator_request_uuid,
            acc_fakes.accelerator_request_state,
            acc_fakes.accelerator_request_device_profile_name,
            acc_fakes.accelerator_request_hostname,
            acc_fakes.accelerator_request_device_rp_uuid,
            acc_fakes.accelerator_request_instance_uuid,
            acc_fakes.accelerator_request_attach_handle_type,
            acc_fakes.accelerator_request_attach_handle_info,
        ), ]
        self.assertEqual(datalist, list(data))


class TestAcceleratorRequestDelete(TestAcceleratorRequest):

    def setUp(self):
        super(TestAcceleratorRequestDelete, self).setUp()
        self.cmd = osc_accelerator_request.DeleteAcceleratorRequest(
            self.app, None
        )

    def test_accelerator_request_delete_non_existed(self):
        self.mock_acc_client.delete_accelerator_request.side_effect = \
            sdk_exc.ResourceNotFound

        arg_list = [acc_fakes.accelerator_request_uuid]
        verify_list = []
        parsed_args = self.check_parser(self.cmd, arg_list, verify_list)
        result = self.assertRaises(exc.ClientException,
                                   self.cmd.take_action,
                                   parsed_args)
        self.assertIn("No accelerator_request with UUID " +
                      acc_fakes.accelerator_request_uuid + " exists",
                      str(result))


class TestAcceleratorRequestCreate(TestAcceleratorRequest):

    def setUp(self):
        super(TestAcceleratorRequestCreate, self).setUp()

        fake_arq = acc_fakes.FakeAcceleratorResource(
            None,
            copy.deepcopy(acc_fakes.ACCELERATOR_REQUEST),
            loaded=True)
        self.mock_acc_client.create_accelerator_request.return_value = fake_arq
        self.mock_acc_client.get_accelerator_request.return_value = fake_arq

        self.cmd = osc_accelerator_request.CreateAcceleratorRequest(
            self.app, None
        )

    def test_accelerator_request_create(self):
        arglist = ["dp_name"]
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {'device_profile_name': 'dp_name',
                  'device_profile_group_id': None,
                  'image_uuid': None}

        self.mock_acc_client.create_accelerator_request.assert_called_with(
            **kwargs)

        collist = (
            'uuid',
            'state',
            'device_profile_name',
            'hostname',
            'device_rp_uuid',
            'instance_uuid',
            'attach_handle_type',
            'attach_handle_info',
        )
        self.assertEqual(collist, columns)

        datalist = [
            acc_fakes.accelerator_request_uuid,
            acc_fakes.accelerator_request_state,
            acc_fakes.accelerator_request_device_profile_name,
            acc_fakes.accelerator_request_hostname,
            acc_fakes.accelerator_request_device_rp_uuid,
            acc_fakes.accelerator_request_instance_uuid,
            acc_fakes.accelerator_request_attach_handle_type,
            acc_fakes.accelerator_request_attach_handle_info,
        ]
        self.assertEqual(datalist, list(data))


class TestAcceleratorRequestShow(TestAcceleratorRequest):

    def setUp(self):
        super(TestAcceleratorRequestShow, self).setUp()

        fake_arq = acc_fakes.FakeAcceleratorResource(
            None,
            copy.deepcopy(acc_fakes.ACCELERATOR_REQUEST),
            loaded=True)
        self.mock_acc_client.get_accelerator_request.return_value = fake_arq
        self.cmd = osc_accelerator_request.ShowAcceleratorRequest(
            self.app, None
        )

    def test_accelerator_request_get(self):
        arglist = [acc_fakes.accelerator_request_uuid]
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.mock_acc_client.get_accelerator_request.assert_called_with(
            acc_fakes.accelerator_request_uuid)

        collist = (
            'uuid',
            'state',
            'device_profile_name',
            'hostname',
            'device_rp_uuid',
            'instance_uuid',
            'attach_handle_type',
            'attach_handle_info',
        )
        self.assertEqual(collist, columns)

        datalist = [
            acc_fakes.accelerator_request_uuid,
            acc_fakes.accelerator_request_state,
            acc_fakes.accelerator_request_device_profile_name,
            acc_fakes.accelerator_request_hostname,
            acc_fakes.accelerator_request_device_rp_uuid,
            acc_fakes.accelerator_request_instance_uuid,
            acc_fakes.accelerator_request_attach_handle_type,
            acc_fakes.accelerator_request_attach_handle_info,
        ]
        self.assertEqual(datalist, list(data))

    def test_accelerator_request_get_not_exist(self):
        get_arq_req = self.mock_acc_client.get_accelerator_request
        get_arq_req.side_effect = sdk_exc.ResourceNotFound
        arglist = [acc_fakes.accelerator_request_uuid]
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaisesRegex(
            exc.CommandError,
            'accelerator_request not found: ' +
            acc_fakes.accelerator_request_uuid,
            self.cmd.take_action, parsed_args)
