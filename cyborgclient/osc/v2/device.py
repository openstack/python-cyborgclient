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


"""Cyborg v2 Acceleration accelerator action implementations"""
import logging

from openstack import exceptions as sdk_exc
from osc_lib.command import command
from osc_lib import utils as oscutils

from cyborgclient.common import utils
from cyborgclient import exceptions as exc
from cyborgclient.i18n import _


class ListDevice(command.Lister):
    """List all devices"""

    def get_parser(self, prog_name):
        parser = super(ListDevice, self).get_parser(prog_name)
        parser.add_argument(
            '--long',
            dest='detail',
            action='store_true',
            default=False,
            help=_("List additional fields in output")
        )
        return parser

    def take_action(self, parsed_args):
        acc_client = self.app.client_manager.accelerator

        if parsed_args.detail:
            column_headers = (
                "created_at",
                "updated_at",
                "uuid",
                "type",
                "vendor",
                "model",
                "hostname",
                "std_board_info",
                "vendor_board_info"
            )

            columns = (
                "created_at",
                "updated_at",
                "uuid",
                "type",
                "vendor",
                "model",
                "hostname",
                "std_board_info",
                "vendor_board_info"
            )
        else:
            column_headers = (
                "uuid",
                "type",
                "vendor",
                "hostname",
                "std_board_info",
            )
            columns = (
                "uuid",
                "type",
                "vendor",
                "hostname",
                "std_board_info",
            )

        data = acc_client.devices()
        if not data:
            return (), ()
        formatters = {}
        return (column_headers,
                (oscutils.get_item_properties(
                    s, columns, formatters=formatters) for s in data))


class ShowDevice(command.ShowOne):
    """Show device details."""
    log = logging.getLogger(__name__ + ".ShowDevice")

    def get_parser(self, prog_name):
        parser = super(ShowDevice, self).get_parser(prog_name)
        parser.add_argument(
            "device",
            metavar="<uuid>",
            help=_("UUID of the device.")
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        acc_client = self.app.client_manager.accelerator
        return _show_device(acc_client,
                            parsed_args.device)


def _show_device(acc_client, uuid):
    """Show detailed info about device."""
    columns = (
        "created_at",
        "updated_at",
        "uuid",
        "type",
        "vendor",
        "model",
        "hostname",
        "std_board_info",
        "vendor_board_info"
    )
    try:
        device = acc_client.get_device(uuid)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('device not found: %s') % uuid)
    formatters = {
        'data': utils.json_formatter,
    }
    data = device.to_dict()
    return columns, oscutils.get_dict_properties(data, columns,
                                                 formatters=formatters)
