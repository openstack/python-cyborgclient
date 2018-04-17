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
        filters.append('limit=%s' % limit)
    if marker is not None:
        filters.append('marker=%s' % marker)
    if sort_key is not None:
        filters.append('sort_key=%s' % sort_key)
    if sort_dir is not None:
        filters.append('sort_dir=%s' % sort_dir)
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
