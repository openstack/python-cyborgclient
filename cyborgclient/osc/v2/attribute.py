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

from osc_lib.command import command
from osc_lib import utils as oscutils

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
