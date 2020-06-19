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
#

from cyborgclient.tests.unit.osc import fakes
from osc_lib.tests import utils
from unittest import mock
import uuid

deployable_created_at = '2019-06-24T00:00:00.000000+00:00'
deployable_updated_at = '2019-06-24T11:11:11.111111+11:11'
deployable_uuid = uuid.uuid4().hex
deployable_name = 'fake_dep_name'
deployable_parent_id = None
deployable_root_id = 1
deployable_num_accelerators = 4
deployable_device_id = 0

DEPLOYABLE = {
    'created_at': deployable_created_at,
    'updated_at': deployable_updated_at,
    'id': deployable_uuid,
    'name': deployable_name,
    'parent_id': deployable_parent_id,
    'root_id': deployable_root_id,
    'num_accelerators': deployable_num_accelerators,
    'device_id': deployable_device_id,
}

device_created_at = '2019-06-24T00:00:00.000000+00:00'
device_updated_at = '2019-06-24T22:22:22.222222+22:22'
device_id = 1
device_uuid = uuid.uuid4().hex
device_name = 'fake_dev_name'
device_type = 'fake_dev_type'
device_vendor = '0x8086'
device_model = 'fake_dev_model'
device_hostname = 'fake_host'
device_std_board_info = '{"product_id": "0x09c4"}'
device_vendor_board_info = 'fake_vb_info'

DEVICE = {
    'created_at': device_created_at,
    'updated_at': device_updated_at,
    'id': device_id,
    'uuid': device_uuid,
    'type': device_type,
    'vendor': device_vendor,
    'model': device_model,
    'hostname': device_hostname,
    'std_board_info': device_std_board_info,
    'vendor_board_info': device_vendor_board_info
}

device_profile_created_at = '2019-06-24T00:00:00.000000+00:00'
device_profile_updated_at = '2019-06-24T11:11:11.111111+11:11'
device_profile_id = 1
device_profile_uuid = uuid.uuid4().hex
device_profile_name = 'fake_devprof_name'
device_profile_groups = [
    {"resources:ACCELERATOR_FPGA": "1",
     "trait:CUSTOM_FPGA_INTEL_PAC_ARRIA10": "required",
     "trait:CUSTOM_FUNCTION_ID_3AFB": "required",
     },
    {"resources:CUSTOM_ACCELERATOR_FOO": "2",
     "resources:CUSTOM_MEMORY": "200",
     "trait:CUSTOM_TRAIT_ALWAYS": "required",
     }
]

DEVICE_PROFILE = {
    'created_at': device_profile_created_at,
    'updated_at': device_profile_updated_at,
    'id': device_profile_id,
    'uuid': device_profile_uuid,
    'name': device_profile_name,
    'groups': device_profile_groups,
}

accelerator_request_uuid = uuid.uuid4().hex
accelerator_request_state = 'fake_state'
accelerator_request_device_profile_name = 'fake_arq_devprof_name'
accelerator_request_hostname = 'fake_arq_hostname'
accelerator_request_device_rp_uuid = 1
accelerator_request_instance_uuid = 2
accelerator_request_attach_handle_type = 3
accelerator_request_attach_handle_info = 4

ACCELERATOR_REQUEST = {
    'uuid': accelerator_request_uuid,
    'state': accelerator_request_state,
    'device_profile_name': accelerator_request_device_profile_name,
    'hostname': accelerator_request_hostname,
    'device_rp_uuid': accelerator_request_device_rp_uuid,
    'instance_uuid': accelerator_request_instance_uuid,
    'attach_handle_type': accelerator_request_attach_handle_type,
    'attach_handle_info': accelerator_request_attach_handle_info,
}


class TestAccelerator(utils.TestCommand):

    def setUp(self):
        super(TestAccelerator, self).setUp()

        self.app.client_manager.auth_ref = mock.MagicMock(auth_token="TOKEN")
        self.app.client_manager.accelerator = mock.MagicMock()


class FakeAcceleratorResource(fakes.FakeResource):

    def get_keys(self):
        return {'property': 'value'}
