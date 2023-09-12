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
from cyborgclient.osc.v2 import attribute as osc_attribute
from cyborgclient.tests.unit.osc.v2 import fakes as acc_fakes


class TestAttribute(acc_fakes.TestAccelerator):

    def setUp(self):
        super(TestAttribute, self).setUp()

        self.mock_acc_client = self.app.client_manager.accelerator
        self.mock_acc_client.reset_mock()


class TestAttributeList(TestAttribute):

    def setUp(self):
        super(TestAttributeList, self).setUp()

        self.mock_acc_client.attributes.return_value = [
            acc_fakes.FakeAcceleratorResource(
                None,
                copy.deepcopy(acc_fakes.ATTRIBUTE),
                loaded=True)
        ]

        self.cmd = osc_attribute.ListAttribute(self.app, None)

    def test_device_profile_list(self):
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {}

        self.mock_acc_client.attributes.assert_called_with(**kwargs)

        collist = (
            'uuid',
            'deployable_id',
            'key',
            'value'
        )
        self.assertEqual(collist, columns)

        datalist = [(
            acc_fakes.attribute_uuid,
            acc_fakes.attribute_deployable_id,
            acc_fakes.attribute_key,
            acc_fakes.attribute_value,
        ), ]
        self.assertEqual(datalist, list(data))

    def test_device_profile_list_long(self):
        arglist = ['--long']
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {}

        self.mock_acc_client.attributes.assert_called_with(**kwargs)

        collist = (osc_attribute.ListAttribute.columns +
                   osc_attribute.ListAttribute.detail_cols)
        self.assertEqual(list(collist), list(columns))

        datalist = [(
            acc_fakes.attribute_uuid,
            acc_fakes.attribute_deployable_id,
            acc_fakes.attribute_key,
            acc_fakes.attribute_value,
            acc_fakes.attribute_created_at,
            acc_fakes.attribute_updated_at,
        ), ]
        self.assertEqual(datalist, list(data))


class TestAttributeCreate(TestAttribute):

    def setUp(self):
        super(TestAttributeCreate, self).setUp()

        fake_arq = acc_fakes.FakeAcceleratorResource(
            None,
            copy.deepcopy(acc_fakes.ATTRIBUTE),
            loaded=True)
        self.mock_acc_client.create_attribute.return_value = fake_arq
        self.mock_acc_client.get_attribute.return_value = fake_arq
        self.cmd = osc_attribute.CreateAttribute(self.app, None)

    def test_attribute_create(self):
        arglist = ['1', 'traits1', 'CUSTOM_FAKE_DEVICE']
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        kwargs = {'deployable_id': '1',
                  'key': 'traits1', 'value': 'CUSTOM_FAKE_DEVICE'}

        self.mock_acc_client.create_attribute.assert_called_with(**kwargs)

        collist = (
            "created_at",
            "updated_at",
            "uuid",
            "deployable_id",
            "key",
            "value",
        )

        self.assertEqual(collist, columns)

        datalist = [
            acc_fakes.attribute_created_at,
            acc_fakes.attribute_updated_at,
            acc_fakes.attribute_uuid,
            acc_fakes.attribute_deployable_id,
            acc_fakes.attribute_key,
            acc_fakes.attribute_value,
        ]
        self.assertEqual(datalist, list(data))


class TestAttributeShow(TestAttribute):

    def setUp(self):
        super(TestAttributeShow, self).setUp()

        fake_arq = acc_fakes.FakeAcceleratorResource(
            None,
            copy.deepcopy(acc_fakes.ATTRIBUTE),
            loaded=True)
        self.mock_acc_client.get_attribute.return_value = fake_arq
        self.cmd = osc_attribute.ShowAttribute(self.app, None)

    def test_attribute_get(self):
        arglist = [acc_fakes.attribute_uuid]
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.mock_acc_client.get_attribute.assert_called_with(
            acc_fakes.attribute_uuid)

        collist = (
            "created_at",
            "updated_at",
            "uuid",
            "deployable_id",
            "key",
            "value",
        )

        self.assertEqual(collist, columns)

        datalist = [
            acc_fakes.attribute_created_at,
            acc_fakes.attribute_updated_at,
            acc_fakes.attribute_uuid,
            acc_fakes.attribute_deployable_id,
            acc_fakes.attribute_key,
            acc_fakes.attribute_value,
        ]
        self.assertEqual(datalist, list(data))

    def test_attribute_get_not_exist(self):
        get_arq_req = self.mock_acc_client.get_attribute
        get_arq_req.side_effect = sdk_exc.ResourceNotFound
        arglist = [acc_fakes.attribute_uuid]
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaisesRegex(
            exc.CommandError,
            'Attribute %s not found' % acc_fakes.attribute_uuid,
            self.cmd.take_action, parsed_args)


class TestAttributeDelete(TestAttribute):

    def setUp(self):
        super(TestAttributeDelete, self).setUp()
        self.cmd = osc_attribute.DeleteAttribute(self.app, None)

    def test_attribute_delete(self):

        arglist = [acc_fakes.attribute_uuid]
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.mock_acc_client.delete_attribute.assert_called_with(
            acc_fakes.attribute_uuid, False)

    def test_attribute_delete_not_exist(self):
        get_arq_req = self.mock_acc_client.delete_attribute
        get_arq_req.side_effect = sdk_exc.ResourceNotFound
        arglist = [acc_fakes.attribute_uuid]
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaisesRegex(
            exc.CommandError,
            'Attribute %s not found' % acc_fakes.attribute_uuid,
            self.cmd.take_action, parsed_args)

    def test_attribute_delete_for_client_exception(self):
        get_arq_req = self.mock_acc_client.delete_attribute
        get_arq_req.side_effect = exc.ClientException
        arglist = [acc_fakes.attribute_uuid]
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(
            exc.ClientException,
            self.cmd.take_action, parsed_args)
