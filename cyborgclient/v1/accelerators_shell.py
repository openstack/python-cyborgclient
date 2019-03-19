# Copyright (c) 2018 Intel, Inc. All rights reserved.
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

from cyborgclient.common import cliutils as utils
from cyborgclient.i18n import _


@utils.arg('--limit',
           metavar='<limit>',
           type=int,
           help=_('Maximum number of accelerators to return'))
@utils.arg('--sort-key',
           metavar='<sort-key>',
           help=_('Column to sort results by'))
@utils.arg('--sort-dir',
           metavar='<sort-dir>',
           choices=['desc', 'asc'],
           help=_('Direction to sort. "asc" or "desc".'))
@utils.arg('--fields',
           default=None,
           metavar='<fields>',
           help=_('Comma-separated list of fields to display. '
                  'Available fields: uuid, name'
                  )
           )
@utils.arg('--detail',
           action='store_true', default=False,
           help=_('Show detailed information about the accelerators.')
           )
def do_accelerator_list(cs, args):
    """Print a list of accelerators.

    (Deprecated for V1)
    """
    utils.deprecated("v1 APIs for accelerator objects are deprecated.")
