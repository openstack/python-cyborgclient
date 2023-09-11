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


class ListAttribute(command.Lister):
    """List all attributes"""

    column_headers = (
        "uuid",
        "deployable_id",
        "key",
        "value"
    )
    columns = (
        "uuid",
        "deployable_id",
        "key",
        "value"
    )
    detail_cols = ("created_at", "updated_at")

    def get_parser(self, prog_name):
        parser = super(ListAttribute, self).get_parser(prog_name)
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
            self.column_headers += self.detail_cols
            self.columns += self.detail_cols

        data = acc_client.attributes()
        if not data:
            return (), ()
        formatters = {}
        return (self.column_headers,
                (oscutils.get_item_properties(
                    s, self.columns, formatters=formatters) for s in data))


class CreateAttribute(command.ShowOne):
    """Register a new attribute with the accelerator service"""
    log = logging.getLogger(__name__ + ".CreateAttribute")

    def get_parser(self, prog_name):
        parser = super(CreateAttribute, self).get_parser(prog_name)
        parser.add_argument(
            'deployable_id',
            metavar='<deployable_id>',
            help=_("Deployable_id for the attribute."))
        parser.add_argument(
            'key',
            metavar='<key>',
            help=_("""Key for the attribute.
                   e.g. '[{"resources:<type>":1,
                   "trait:CUSTOM_<type>_<product_id>": "required",
                   "trait:CUSTOM_<type>_<vendor>": "required"}]'"""))
        parser.add_argument(
            'value',
            metavar='<value>',
            help=_("Value for the attribute."))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        acc_client = self.app.client_manager.accelerator

        attrs = {
            'deployable_id': parsed_args.deployable_id,
            'key': parsed_args.key,
            'value': parsed_args.value
        }
        attribute = acc_client.create_attribute(**attrs)
        return _show_attribute(acc_client, attribute.uuid)


class DeleteAttribute(command.Command):
    """Delete attribute(s)."""

    log = logging.getLogger(__name__ + ".DeleteAttribute")

    def get_parser(self, prog_name):
        parser = super(DeleteAttribute, self).get_parser(prog_name)
        parser.add_argument(
            "attributes",
            metavar="<uuid>",
            nargs="+",
            help=_("UUID(s) of the attribute(s) to delete.")
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        acc_client = self.app.client_manager.accelerator

        failures = []
        for uuid in parsed_args.attributes:
            try:
                acc_client.delete_attribute(uuid, False)
                print(_('Deleted attribute %s') % uuid)
            except sdk_exc.ResourceNotFound:
                raise exc.CommandError(_('Attribute %s not found') % uuid)
            except exc.ClientException as e:
                failures.append(_("Failed to delete attribute \
                                %(uuid)s: %(error)s")
                                % {'uuid': uuid, 'error': e})
        if failures:
            raise exc.ClientException("\n".join(failures))


class ShowAttribute(command.ShowOne):
    """Show attribute details."""
    log = logging.getLogger(__name__ + ".ShowAttribute")

    def get_parser(self, prog_name):
        parser = super(ShowAttribute, self).get_parser(prog_name)
        parser.add_argument(
            "attribute",
            metavar="<attribute>",
            help=_("UUID of the attribute.")
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        acc_client = self.app.client_manager.accelerator
        return _show_attribute(acc_client,
                               parsed_args.attribute)


def _show_attribute(acc_client, uuid):
    """Show detailed info about device_profile."""

    columns = (
        "created_at",
        "updated_at",
        "uuid",
        "deployable_id",
        "key",
        "value",
    )
    try:
        attribute = acc_client.get_attribute(uuid)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('Attribute %s not found') % uuid)
    except sdk_exc.HttpException as e:
        raise exc.NotAcceptable(message=e.details)

    formatters = {'data': utils.json_formatter}
    data = attribute.to_dict()
    return columns, oscutils.get_dict_properties(data, columns,
                                                 formatters=formatters)
