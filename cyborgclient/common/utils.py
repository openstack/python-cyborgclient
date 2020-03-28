#   Copyright 2016 Huawei, Inc. All rights reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
import logging

from oslo_serialization import jsonutils

from cyborgclient import exceptions as exc

LOG = logging.getLogger(__name__)


def common_filters(marker=None, limit=None, sort_key=None, sort_dir=None):
    """Generate common filters for any list request.

    :param marker: entity ID from which to start returning entities.
    :param limit: maximum number of entities to return.
    :param sort_key: field to use for sorting.
    :param sort_dir: direction of sorting: 'asc' or 'desc'.
    :returns: list of string filters.
    """
    filters = []
    if isinstance(limit, int):
        filters.append('filters.field=limit')
        filters.append('filters.value=%d' % limit)
    if marker is not None:
        filters.append('filters.field=marker')
        filters.append('filters.value=%s' % marker)
    if sort_key is not None:
        filters.append('filters.field=sort_key')
        filters.append('filters.value=%s' % sort_key)
    if sort_dir is not None:
        filters.append('filters.field=sort_dir')
        filters.append('filters.value=%s' % sort_dir)
    return filters


def add_filters(filters, **kwargs):
    if kwargs:
        for field, value in kwargs.iteritems():
            filters.append('filters.field=%s' % field)
            filters.append('filters.value=%s' % value)
    return filters


def print_list_field(field):
    return lambda obj: ', '.join(getattr(obj, field))


def get_response_body(resp):
    body = resp.content
    content_type = resp.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        try:
            body = resp.json()
        except ValueError:
            LOG.error('Could not decode response body as JSON')
    elif 'application/octet-stream' in content_type:
        try:
            body = resp.body()
        except ValueError:
            LOG.error('Could not decode response body as raw')
    else:
        body = None
    return body


def addresses_formatter(network_client, networks):
    output = []
    for (network, addresses) in networks.items():
        if not addresses:
            continue
        addrs = [addr['addr'] for addr in addresses]
        network_data = network_client.find_network(
            network, ignore_missing=False)
        net_ident = network_data.name or network_data.id
        addresses_csv = ', '.join(addrs)
        group = "%s=%s" % (net_ident, addresses_csv)
        output.append(group)
    return '; '.join(output)


def image_formatter(image_client, image_id):
    if image_id:
        image = image_client.images.get(image_id)
        return '%s (%s)' % (image.name, image_id)
    return ''


def flavor_formatter(bc_client, flavor_id):
    if flavor_id:
        flavor = bc_client.flavor.get(flavor_id)
        return '%s (%s)' % (flavor.name, flavor_id)
    return ''


def clean_listing_columns(headers, columns, data_sample):
    col_headers = []
    cols = []
    for header, col in zip(headers, columns):
        if hasattr(data_sample, col):
            col_headers.append(header)
            cols.append(col)
    return tuple(col_headers), tuple(cols)


def json_formatter(js):
    return jsonutils.dumps(js, indent=2, ensure_ascii=False)


def split_and_deserialize(string):
    """Split and try to JSON deserialize a string.

    Gets a string with the KEY=VALUE format, split it (using '=' as the
    separator) and try to JSON deserialize the VALUE.
    :returns: A tuple of (key, value).
    """

    try:
        key, value = string.split("=", 1)
    except ValueError:
        raise exc.CommandError(_('Attributes must be a list of '
                                 'PATH=VALUE not "%s"') % string)
    try:
        value = jsonutils.loads(value)
    except ValueError:
        pass

    return (key, value)


def args_array_to_patch(op, attributes):
    patch = []
    for attr in attributes:
        # Sanitize
        if not attr.startswith('/'):
            attr = '/' + attr

        if op in ['add', 'replace']:
            path, value = split_and_deserialize(attr)
            patch.append({'op': op, 'path': path, 'value': value})

        elif op == "remove":
            # For remove only the key is needed
            patch.append({'op': op, 'path': attr})
        else:
            raise exc.CommandError(_('Unknown PATCH operation: %s') % op)
    return patch
