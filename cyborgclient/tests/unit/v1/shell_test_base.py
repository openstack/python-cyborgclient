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

import re
from unittest import mock

from testtools import matchers

from cyborgclient.tests.unit import utils

FAKE_ENV = {'OS_USERNAME': 'username',
            'OS_PASSWORD': 'password',
            'OS_PROJECT_NAME': 'project_name',
            'OS_AUTH_URL': 'http://no.where/v2.0',
            'BYPASS_URL': 'http://cyborg'}


class TestCommandLineArgument(utils.TestCase):

    def setUp(self):
        super(TestCommandLineArgument, self).setUp()
        self.make_env(fake_env=FAKE_ENV)
        session_client = mock.patch(
            'cyborgclient.common.httpclient.SessionClient')
        session_client.start()
        loader = mock.patch('keystoneauth1.loading.get_plugin_loader')
        loader.start()
        session = mock.patch('keystoneauth1.session.Session')
        session.start()

        self.addCleanup(session_client.stop)
        self.addCleanup(loader.stop)
        self.addCleanup(session.stop)

    def _test_arg_success(self, command):
        stdout, stderr = self.shell(command)

    def _test_arg_failure(self, command, error_msg):
        stdout, stderr = self.shell(command, (2,))
        for line in error_msg:
            self.assertThat((stdout + stderr),
                            matchers.MatchesRegex(line,
                            re.DOTALL | re.MULTILINE))
