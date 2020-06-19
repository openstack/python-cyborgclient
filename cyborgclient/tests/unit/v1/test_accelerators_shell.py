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

from unittest import mock

from cyborgclient.tests.unit.v1 import shell_test_base


class ShellTest(shell_test_base.TestCommandLineArgument):

    @mock.patch('cyborgclient.common.cliutils.print_list')
    def test_accelerator_list(self, mock_print_list):
        pass
