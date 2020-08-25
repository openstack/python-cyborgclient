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
from oslo_serialization import jsonutils

from cyborgclient.common import utils
from cyborgclient import exceptions as exc
from cyborgclient.i18n import _


class ListDeviceProfile(command.Lister):
    """List all device profiles"""

    def get_parser(self, prog_name):
        parser = super(ListDeviceProfile, self).get_parser(prog_name)
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
                "name",
                "groups"
            )
            columns = (
                "created_at",
                "updated_at",
                "uuid",
                "name",
                "groups"
            )
        else:
            column_headers = (
                "uuid",
                "name",
                "groups",
            )
            columns = (
                "uuid",
                "name",
                "groups",
            )

        data = acc_client.device_profiles()
        if not data:
            return (), ()
        formatters = {}
        return (column_headers,
                (oscutils.get_item_properties(
                    s, columns, formatters=formatters) for s in data))


class CreateDeviceProfile(command.ShowOne):
    """Register a new device_profile with the accelerator service"""
    log = logging.getLogger(__name__ + ".CreateDeviceProfile")

    def get_parser(self, prog_name):
        parser = super(CreateDeviceProfile, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_("Unique name for the device_profile."))
        parser.add_argument(
            'groups',
            metavar='<groups>',
            help=_("""groups for the device_profile.
                   e.g. '[{"resources:<type>":1,
                   "trait:CUSTOM_<type>_<product_id>": "required",
                   "trait:CUSTOM_<type>_<vendor>": "required"}]'"""))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        acc_client = self.app.client_manager.accelerator

        attrs = {
            'name': parsed_args.name,
            'groups': list(jsonutils.loads(parsed_args.groups)),
        }
        device_profile = acc_client.create_device_profile(**attrs)
        return _show_device_profile(acc_client, device_profile.uuid)


class DeleteDeviceProfile(command.Command):
    """Delete deviceProfile(s)."""

    log = logging.getLogger(__name__ + ".DeleteDeviceProfile")

    def get_parser(self, prog_name):
        parser = super(DeleteDeviceProfile, self).get_parser(prog_name)
        parser.add_argument(
            "device_profiles",
            metavar="<uuid>",
            nargs="+",
            help=_("UUID(s) of the device_profile(s) to delete.")
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        acc_client = self.app.client_manager.accelerator

        failures = []
        for uuid in parsed_args.device_profiles:
            try:
                acc_client.delete_device_profile(uuid, False)
                print(_('Deleted device_profile %s') % uuid)
            except exc.ClientException as e:
                failures.append(_("Failed to delete device_profile \
                                %(device_profile)s: %(error)s")
                                % {'uuid': uuid, 'error': e})
        if failures:
            raise exc.ClientException("\n".join(failures))


class ShowDeviceProfile(command.ShowOne):
    """Show device_profile details."""
    log = logging.getLogger(__name__ + ".ShowDeviceProfile")

    def get_parser(self, prog_name):
        parser = super(ShowDeviceProfile, self).get_parser(prog_name)
        parser.add_argument(
            "device_profile",
            metavar="<uuid>",
            help=_("UUID of the device_profile.")
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        acc_client = self.app.client_manager.accelerator
        return _show_device_profile(acc_client,
                                    parsed_args.device_profile)


def _show_device_profile(acc_client, uuid):
    """Show detailed info about device_profile."""
    columns = (
        "created_at",
        "updated_at",
        "uuid",
        "name",
        "groups",
    )
    try:
        device_profile = acc_client.get_device_profile(uuid)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('device_profile not found: %s') % uuid)
    formatters = {
        'data': utils.json_formatter,
    }
    data = device_profile.to_dict()
    return columns, oscutils.get_dict_properties(data, columns,
                                                 formatters=formatters)
