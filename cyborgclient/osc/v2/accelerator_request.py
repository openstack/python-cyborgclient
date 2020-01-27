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


class ListAcceleratorRequest(command.Lister):
    """List all accelerator requests"""

    def get_parser(self, prog_name):
        parser = super(ListAcceleratorRequest, self).get_parser(prog_name)
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
                "uuid",
                "state",
                "device_profile_name",
                "hostname",
                "device_rp_uuid",
                "instance_uuid",
                "attach_handle_type",
                "attach_handle_info",
            )
            columns = (
                "uuid",
                "state",
                "device_profile_name",
                "hostname",
                "device_rp_uuid",
                "instance_uuid",
                "attach_handle_type",
                "attach_handle_info",
            )
        else:
            column_headers = (
                "uuid",
                "state",
                "device_profile_name",
                "instance_uuid",
                "attach_handle_type",
                "attach_handle_info",
            )
            columns = (
                "uuid",
                "state",
                "device_profile_name",
                "instance_uuid",
                "attach_handle_type",
                "attach_handle_info",
            )

        data = acc_client.accelerator_requests()
        if not data:
            return (), ()
        formatters = {}
        return (column_headers,
                (oscutils.get_item_properties(
                    s, columns, formatters=formatters) for s in data))


class CreateAcceleratorRequest(command.ShowOne):
    """Register a new accelerator_request with the accelerator service"""

    log = logging.getLogger(__name__ + ".CreateAcceleratorRequest")

    def get_parser(self, prog_name):
        parser = super(CreateAcceleratorRequest, self).get_parser(prog_name)

        parser.add_argument(
            'device_profile_name',
            metavar='<device_profile_name>',
            help=_("The name of device_profile for accelerator_request."))
        parser.add_argument(
            'device_profile_group_id',
            metavar='<device_profile_group_id>',
            help=_("The group id of device_profile \
                   for the accelerator_request."))
        parser.add_argument(
            '--image-uuid',
            metavar='<glance_image_uuid>',
            dest='img_uuid',
            help=_("The uuid of image saved in glance."))

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        acc_client = self.app.client_manager.accelerator

        attrs = {
            'device_profile_name': parsed_args.device_profile_name,
            'device_profile_group_id': parsed_args.device_profile_group_id,
            'image_uuid': parsed_args.img_uuid,
        }

        accelerator_request = acc_client.create_accelerator_request(**attrs)

        return _show_accelerator_request(acc_client,
                                         accelerator_request.uuid)


class DeleteAcceleratorRequest(command.Command):
    """Delete accelerator request(s)."""

    log = logging.getLogger(__name__ + ".DeleteAcceleratorRequest")

    def get_parser(self, prog_name):
        parser = super(DeleteAcceleratorRequest, self).get_parser(prog_name)
        parser.add_argument(
            "accelerator_requests",
            metavar="<uuid>",
            nargs="+",
            help=_("UUID(s) of the accelerator_request(s) to delete.")
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        acc_client = self.app.client_manager.accelerator

        failures = []
        for uuid in parsed_args.accelerator_requests:
            try:
                acc_client.delete_accelerator_request(uuid, False)
                print(_('Deleted accelerator_request %s') % uuid)
            except exc.ClientException as e:
                failures.append(_("Failed to delete accelerator_request\
                                %(accelerator_request)s: %(error)s")
                                % {'uuid': uuid, 'error': e})

        if failures:
            raise exc.ClientException("\n".join(failures))


class ShowAcceleratorRequest(command.ShowOne):
    """Show accelerator_request details."""

    log = logging.getLogger(__name__ + ".ShowAcceleratorRequest")

    def get_parser(self, prog_name):
        parser = super(ShowAcceleratorRequest, self).get_parser(prog_name)
        parser.add_argument(
            "accelerator_request",
            metavar="<uuid>",
            help=_("UUID of the accelerator_request.")
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        acc_client = self.app.client_manager.accelerator

        return _show_accelerator_request(acc_client,
                                         parsed_args.accelerator_request)


def _show_accelerator_request(acc_client, uuid):
    """Show detailed info about accelerator_request."""

    columns = (
        "uuid",
        "state",
        "device_profile_name",
        "hostname",
        "device_rp_uuid",
        "instance_uuid",
        "attach_handle_type",
        "attach_handle_info",
    )

    try:
        accelerator_request = acc_client.get_accelerator_request(uuid)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('accelerator_request not found: %s') % uuid)

    formatters = {
        'data': utils.json_formatter,
    }
    data = accelerator_request.to_dict()
    return columns, oscutils.get_dict_properties(data, columns,
                                                 formatters=formatters)


class BindAcceleratorRequest(command.ShowOne):
    """Bind accelerator to instance."""

    log = logging.getLogger(__name__ + ".BindAcceleratorRequest")

    def get_parser(self, prog_name):
        parser = super(BindAcceleratorRequest, self).get_parser(prog_name)

        parser.add_argument(
            'accelerator_request',
            metavar='<accelerator_request>',
            help=_("UUID of the accelerator request")
        )
        parser.add_argument(
            'hostname',
            metavar='<hostname>',
            help=_("Bind hostname of the accelerator request")
        )
        parser.add_argument(
            "instance_uuid",
            metavar="<instance_uuid>",
            help=_("Bind instance_uuid of the accelerator request")
        )
        parser.add_argument(
            "device_rp_uuid",
            metavar="<device_rp_uuid>",
            help=_("Bind device_rp_uuid of the accelerator request")
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        acc_client = self.app.client_manager.accelerator

        properties = []
        if parsed_args.hostname:
            hostname = ["hostname=%s" % parsed_args.hostname]
            properties.extend(utils.args_array_to_patch('add', hostname))
        if parsed_args.instance_uuid:
            instance_uuid = ["instance_uuid=%s" % parsed_args.instance_uuid]
            properties.extend(utils.args_array_to_patch('add', instance_uuid))
        if parsed_args.device_rp_uuid:
            device_rp_uuid = ["device_rp_uuid=%s" % parsed_args.device_rp_uuid]
            properties.extend(utils.args_array_to_patch('add', device_rp_uuid))

        if properties:
            acc_client.update_accelerator_request(
                parsed_args.accelerator_request, properties)
            return _show_accelerator_request(acc_client,
                                             parsed_args.accelerator_request)
        else:
            self.log.warning("Please specify what to set.")


class UnbindAcceleratorRequest(command.ShowOne):
    """Unbind accelerator from instance."""

    log = logging.getLogger(__name__ + ".UnbindAcceleratorRequest")

    def get_parser(self, prog_name):
        parser = super(UnbindAcceleratorRequest, self).get_parser(prog_name)

        parser.add_argument(
            'accelerator_request',
            metavar='<accelerator_request>',
            help=_("UUID of the accelerator request")
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        acc_client = self.app.client_manager.accelerator

        properties = [{'path': '/hostname', 'op': 'remove'},
                      {'path': '/instance_uuid', 'op': 'remove'},
                      {'path': '/device_rp_uuid', 'op': 'remove'}]

        acc_client.update_accelerator_request(parsed_args.accelerator_request,
                                              properties)

        return _show_accelerator_request(acc_client,
                                         parsed_args.accelerator_request)
