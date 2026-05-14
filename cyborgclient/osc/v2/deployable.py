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


class ListDeployable(command.Lister):
    """List all deployables"""

    def get_parser(self, prog_name):
        parser = super(ListDeployable, self).get_parser(prog_name)
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
                "parent_id",
                "root_id",
                "name",
                "num_accelerators",
                "device_id"
            )

            columns = (
                "created_at",
                "updated_at",
                "id",
                "parent_id",
                "root_id",
                "name",
                "num_accelerators",
                "device_id"
            )
        else:
            column_headers = (
                "uuid",
                "name",
                "device_id",
            )
            columns = (
                "id",
                "name",
                "device_id",
            )
        data = acc_client.deployables()
        if not data:
            return (), ()
        formatters = {}
        return (column_headers,
                (oscutils.get_item_properties(
                    s, columns, formatters=formatters) for s in data))


class ShowDeployable(command.ShowOne):
    """Show deployable details."""
    log = logging.getLogger(__name__ + ".ShowDeployable")

    def get_parser(self, prog_name):
        parser = super(ShowDeployable, self).get_parser(prog_name)
        parser.add_argument(
            "deployable",
            metavar="<uuid>",
            help=_("UUID of the deployable.")
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        acc_client = self.app.client_manager.accelerator
        return _show_deployable(acc_client,
                                parsed_args.deployable)


def _show_deployable(acc_client, uuid):
    """Show detailed info about deployable."""
    columns = (
        "created_at",
        "updated_at",
        "uuid",
        "name",
    )
    try:
        deployable = acc_client.get_deployable(uuid)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('deployable not found: %s') % uuid)
    formatters = {
        'data': utils.json_formatter,
    }
    data = deployable.to_dict()
    data['uuid'] = data.pop('id', uuid)
    return columns, oscutils.get_dict_properties(data, columns,
                                                 formatters=formatters)


class ProgramDeployable(command.ShowOne):
    """Reconfigure deployable."""
    log = logging.getLogger(__name__ + ".ProgramDeployable")

    def get_parser(self, prog_name):
        parser = super(ProgramDeployable, self).get_parser(prog_name)
        parser.add_argument(
            'deployable_uuid',
            metavar='<deployable_uuid>',
            default=False,
            help=_("Deployable UUID for reconfigure.")
        )
        parser.add_argument(
            'image_uuid',
            metavar='<image_uuid>',
            default=False,
            help=_("Image UUID for reconfigure.")
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        acc_client = self.app.client_manager.accelerator
        dep_uuid = parsed_args.deployable_uuid
        try:
            acc_client.get_deployable(dep_uuid)
        except sdk_exc.ResourceNotFound:
            raise exc.CommandError(_('deployable not found: %s') % dep_uuid)

        image_uuid = parsed_args.image_uuid
        image_client = self.app.client_manager.image
        try:
            image_client.get(image_uuid)
        except sdk_exc.ResourceNotFound:
            raise exc.CommandError(_('image not found: %s') % image_uuid)

        program_info = [{'path': '/program',
                         'value': [{'image_uuid': image_uuid}],
                         'op': 'replace'}]
        acc_client.update_deployable(dep_uuid, program_info)
        return _show_deployable(acc_client, dep_uuid)
