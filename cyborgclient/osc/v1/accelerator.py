#   Copyright (c) 2018 Intel, Inc. All rights reserved.
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


"""Cyborg v1 Acceleration accelerator action implementations"""


from osc_lib.command import command
from osc_lib import utils

from cyborgclient.common import utils as cli_utils
from cyborgclient.i18n import _


class ListAccelerator(command.Lister):
    """List all accelerators"""

    def get_parser(self, prog_name):
        parser = super(ListAccelerator, self).get_parser(prog_name)
        parser.add_argument(
            '--long',
            action='store_true',
            default=False,
            help=_("List additional fields in output")
        )
        return parser

    def take_action(self, parsed_args):
        acc_client = self.app.client_manager.accelerator

        column_headers = (
            "UUID",
            "Name",
            "Type",
            "Description",
            "Device Type",
            "Capability",
        )
        columns = (
            "uuid",
            "name",
            "type",
            "description",
            "device_type",
            "capability",
        )

        data = acc_client.accelerators.list()
        if not data:
            return (), ()
        column_headers, columns = cli_utils.clean_listing_columns(
            column_headers, columns, data[0])
        formatters = {}

        return (column_headers,
                (utils.get_item_properties(
                    s, columns, formatters=formatters) for s in data))
