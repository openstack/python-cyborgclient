# Copyright (c) 2015 Thales Services SAS
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

import testtools
from unittest import mock

from cyborgclient.v1 import client


class ClientTest(testtools.TestCase):

    @mock.patch('cyborgclient.common.httpclient.SessionClient')
    @mock.patch('keystoneauth1.session.Session')
    def test_init_with_session(self, mock_session, http_client):
        session = mock.Mock()
        client.Client(session=session)
        mock_session.assert_not_called()
        http_client.assert_called_once_with(
            interface='public',
            region_name=None,
            service_name=None,
            service_type='accelerator',
            session=session,
            endpoint_override=None,
            api_version=None)

    @mock.patch('cyborgclient.common.httpclient.SessionClient')
    @mock.patch('keystoneauth1.session.Session')
    def test_init_with_endpoint_override(self, mock_session, http_client):
        session = mock.Mock()
        client.Client(session=session, endpoint_override='cyborgurl')
        mock_session.assert_not_called()
        http_client.assert_called_once_with(
            interface='public',
            region_name=None,
            service_name=None,
            service_type='accelerator',
            session=session,
            endpoint_override='cyborgurl',
            api_version=None)

    @mock.patch('cyborgclient.common.httpclient.SessionClient')
    @mock.patch('keystoneauth1.session.Session')
    def test_init_with_cyborg_url_and_endpoint_override(self, mock_session,
                                                        http_client):
        session = mock.Mock()
        client.Client(session=session, cyborg_url='cyborgurl',
                      endpoint_override='cyborgurl')
        mock_session.assert_not_called()
        http_client.assert_called_once_with(
            interface='public',
            region_name=None,
            service_name=None,
            service_type='accelerator',
            session=session,
            endpoint_override='cyborgurl',
            api_version=None)
