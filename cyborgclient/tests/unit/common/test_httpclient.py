# All Rights Reserved.
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

import io
import json
from unittest import mock

from http import client as http_client


from cyborgclient.common import httpclient as http
from cyborgclient import exceptions as exc
from cyborgclient.tests.unit import utils


def _get_error_body(faultstring=None, debuginfo=None):
    error_body = {
        'faultstring': faultstring,
        'debuginfo': debuginfo
    }
    raw_error_body = json.dumps(error_body)
    body = {'error_message': raw_error_body}
    raw_body = json.dumps(body)
    return raw_body


HTTP_CLASS = http_client.HTTPConnection
HTTPS_CLASS = http.VerifiedHTTPSConnection
DEFAULT_TIMEOUT = 600


class HttpClientTest(utils.BaseTestCase):

    def test_url_generation_trailing_slash_in_base(self):
        client = http.HTTPClient('http://localhost/')
        url = client._make_connection_url('/v1/accelerators')
        self.assertEqual('/v1/accelerators', url)

    def test_url_generation_without_trailing_slash_in_base(self):
        client = http.HTTPClient('http://localhost')
        url = client._make_connection_url('/v1/accelerators')
        self.assertEqual('/v1/accelerators', url)

    def test_url_generation_prefix_slash_in_path(self):
        client = http.HTTPClient('http://localhost/')
        url = client._make_connection_url('/v1/accelerators')
        self.assertEqual('/v1/accelerators', url)

    def test_url_generation_without_prefix_slash_in_path(self):
        client = http.HTTPClient('http://localhost')
        url = client._make_connection_url('v1/accelerators')
        self.assertEqual('/v1/accelerators', url)

    def test_server_exception_empty_body(self):
        error_body = _get_error_body()
        fake_resp = utils.FakeResponse({'content-type': 'application/json'},
                                       io.StringIO(error_body),
                                       version=1,
                                       status=500)
        client = http.HTTPClient(
            'http://localhost/',
            api_version='/v1')
        client.get_connection = (
            lambda *a, **kw: utils.FakeConnection(fake_resp))

        error = self.assertRaises(exc.InternalServerError,
                                  client.json_request,
                                  'GET', '/v1/accelerators')
        self.assertEqual('Internal Server Error (HTTP 500)', str(error))

    def test_server_exception_msg_only(self):
        error_msg = 'test error msg'
        error_body = _get_error_body(error_msg)
        fake_resp = utils.FakeResponse({'content-type': 'application/json'},
                                       io.StringIO(error_body),
                                       version=1,
                                       status=500)
        client = http.HTTPClient(
            'http://localhost/',
            api_version='/v1')
        client.get_connection = (
            lambda *a, **kw: utils.FakeConnection(fake_resp))

        error = self.assertRaises(exc.InternalServerError,
                                  client.json_request,
                                  'GET', '/v1/accelerators')
        self.assertEqual(error_msg + ' (HTTP 500)', str(error))

    def test_server_exception_msg_and_traceback(self):
        error_msg = 'another test error'
        error_trace = ("\"Traceback (most recent call last):\\n\\n  "
                       "File \\\"/usr/local/lib/python2.7/...")
        error_body = _get_error_body(error_msg, error_trace)
        fake_resp = utils.FakeResponse({'content-type': 'application/json'},
                                       io.StringIO(error_body),
                                       version=1,
                                       status=500)
        client = http.HTTPClient(
            'http://localhost/',
            api_version='/v1')
        client.get_connection = (
            lambda *a, **kw: utils.FakeConnection(fake_resp))

        error = self.assertRaises(exc.InternalServerError,
                                  client.json_request,
                                  'GET', '/v1/accelerators')

        self.assertEqual(
            '%(error)s (HTTP 500)\n%(trace)s' % {'error': error_msg,
                                                 'trace': error_trace},
            "%(error)s\n%(details)s" % {'error': str(error),
                                        'details': str(error.details)})

    def test_get_connection_params(self):
        endpoint = 'http://cyborg-host:6666'
        expected = (HTTP_CLASS,
                    ('cyborg-host', 6666, ''),
                    {'timeout': DEFAULT_TIMEOUT})
        params = http.HTTPClient.get_connection_params(endpoint)
        self.assertEqual(expected, params)

    def test_get_connection_params_with_trailing_slash(self):
        endpoint = 'http://cyborg-host:6666/'
        expected = (HTTP_CLASS,
                    ('cyborg-host', 6666, ''),
                    {'timeout': DEFAULT_TIMEOUT})
        params = http.HTTPClient.get_connection_params(endpoint)
        self.assertEqual(expected, params)

    def test_get_connection_params_with_ssl(self):
        endpoint = 'https://cyborg-host:6666'
        expected = (HTTPS_CLASS,
                    ('cyborg-host', 6666, ''),
                    {
                        'timeout': DEFAULT_TIMEOUT,
                        'ca_file': None,
                        'cert_file': None,
                        'key_file': None,
                        'insecure': False,
                    })
        params = http.HTTPClient.get_connection_params(endpoint)
        self.assertEqual(expected, params)

    def test_get_connection_params_with_ssl_params(self):
        endpoint = 'https://cyborg-host:6666'
        ssl_args = {
            'ca_file': '/path/to/ca_file',
            'cert_file': '/path/to/cert_file',
            'key_file': '/path/to/key_file',
            'insecure': True,
        }

        expected_kwargs = {'timeout': DEFAULT_TIMEOUT}
        expected_kwargs.update(ssl_args)
        expected = (HTTPS_CLASS,
                    ('cyborg-host', 6666, ''),
                    expected_kwargs)
        params = http.HTTPClient.get_connection_params(endpoint, **ssl_args)
        self.assertEqual(expected, params)

    def test_get_connection_params_with_timeout(self):
        endpoint = 'http://cyborg-host:6666'
        expected = (HTTP_CLASS,
                    ('cyborg-host', 6666, ''),
                    {'timeout': 300.0})
        params = http.HTTPClient.get_connection_params(endpoint, timeout=300)
        self.assertEqual(expected, params)

    def test_get_connection_params_with_version(self):
        endpoint = 'http://cyborg-host:6666/v1'
        expected = (HTTP_CLASS,
                    ('cyborg-host', 6666, ''),
                    {'timeout': DEFAULT_TIMEOUT})
        params = http.HTTPClient.get_connection_params(endpoint)
        self.assertEqual(expected, params)

    def test_get_connection_params_with_version_trailing_slash(self):
        endpoint = 'http://cyborg-host:6666/v1/'
        expected = (HTTP_CLASS,
                    ('cyborg-host', 6666, ''),
                    {'timeout': DEFAULT_TIMEOUT})
        params = http.HTTPClient.get_connection_params(endpoint)
        self.assertEqual(expected, params)

    def test_get_connection_params_with_subpath(self):
        endpoint = 'http://cyborg-host:6666/cyborg'
        expected = (HTTP_CLASS,
                    ('cyborg-host', 6666, '/cyborg'),
                    {'timeout': DEFAULT_TIMEOUT})
        params = http.HTTPClient.get_connection_params(endpoint)
        self.assertEqual(expected, params)

    def test_get_connection_params_with_subpath_trailing_slash(self):
        endpoint = 'http://cyborg-host:6666/cyborg/'
        expected = (HTTP_CLASS,
                    ('cyborg-host', 6666, '/cyborg'),
                    {'timeout': DEFAULT_TIMEOUT})
        params = http.HTTPClient.get_connection_params(endpoint)
        self.assertEqual(expected, params)

    def test_get_connection_params_with_subpath_version(self):
        endpoint = 'http://cyborg-host:6666/cyborg/v1'
        expected = (HTTP_CLASS,
                    ('cyborg-host', 6666, '/cyborg'),
                    {'timeout': DEFAULT_TIMEOUT})
        params = http.HTTPClient.get_connection_params(endpoint)
        self.assertEqual(expected, params)

    def test_get_connection_params_with_subpath_version_trailing_slash(self):
        endpoint = 'http://cyborg-host:6666/cyborg/v1/'
        expected = (HTTP_CLASS,
                    ('cyborg-host', 6666, '/cyborg'),
                    {'timeout': DEFAULT_TIMEOUT})
        params = http.HTTPClient.get_connection_params(endpoint)
        self.assertEqual(expected, params)

    def test_401_unauthorized_exception(self):
        error_body = _get_error_body()
        fake_resp = utils.FakeResponse({'content-type': 'text/plain'},
                                       io.StringIO(error_body),
                                       version=1,
                                       status=401)
        client = http.HTTPClient(
            'http://localhost/',
            api_version='/v1')

        client.get_connection = (lambda *a,
                                 **kw: utils.FakeConnection(fake_resp))

        self.assertRaises(exc.Unauthorized, client.json_request,
                          'GET', '/v1/accelerators')


class SessionClientTest(utils.BaseTestCase):

    def test_server_exception_msg_and_traceback(self):
        error_msg = 'another test error'
        error_trace = ("\"Traceback (most recent call last):\\n\\n  "
                       "File \\\"/usr/local/lib/python2.7/...")
        error_body = _get_error_body(error_msg, error_trace)

        fake_session = utils.FakeSession({'Content-Type': 'application/json'},
                                         error_body,
                                         500)

        client = http.SessionClient(
            api_version='/v1',
            session=fake_session)

        error = self.assertRaises(exc.InternalServerError,
                                  client.json_request,
                                  'GET', '/v1/accelerators')

        self.assertEqual(
            '%(error)s (HTTP 500)\n%(trace)s' % {'error': error_msg,
                                                 'trace': error_trace},
            "%(error)s\n%(details)s" % {'error': str(error),
                                        'details': str(error.details)})

    def test_server_exception_empty_body(self):
        error_body = _get_error_body()

        fake_session = utils.FakeSession({'Content-Type': 'application/json'},
                                         error_body,
                                         500)

        client = http.SessionClient(
            api_version='/v1',
            session=fake_session)

        error = self.assertRaises(exc.InternalServerError,
                                  client.json_request,
                                  'GET', '/v1/accelerators')

        self.assertEqual('Internal Server Error (HTTP 500)', str(error))

    def test_bypass_url(self):
        fake_response = utils.FakeSessionResponse(
            {}, content="", status_code=201)
        fake_session = mock.MagicMock()
        fake_session.request.side_effect = [fake_response]

        client = http.SessionClient(
            api_version='/v1',
            session=fake_session, endpoint_override='http://cyborg')

        client.json_request('GET', '/v1/accelerators')
        self.assertEqual(
            fake_session.request.call_args[1]['endpoint_override'],
            'http://cyborg'
        )

    def test_exception(self):
        fake_response = utils.FakeSessionResponse(
            {}, content="", status_code=504)
        fake_session = mock.MagicMock()
        fake_session.request.side_effect = [fake_response]
        client = http.SessionClient(
            api_version='/v1',
            session=fake_session, endpoint_override='http://cyborg')
        self.assertRaises(exc.GatewayTimeout,
                          client.json_request,
                          'GET', '/v1/accelerators')
