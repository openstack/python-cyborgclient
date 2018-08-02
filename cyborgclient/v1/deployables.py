#   Copyright (c) 2018 Intel, Inc. All rights reserved.
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

from cyborgclient.v1 import basemodels


CREATION_ATTRIBUTES = basemodels.CREATION_ATTRIBUTES


class Deployable(basemodels.BaseModel):
    model_name = "Deployable"


class DeployableManager(basemodels.BaseModelManager):
    api_name = "deployables"
    base_url = "accelerators/deployables"
    resource_class = Deployable

    def deallocation(self, deployable_uuid):
        """Delete specified accelerators from instance.

        :param deployable_uuid: deployable_uuid which is attached to the
        instance.
        """
        body = [{"op": "replace", "path": "/instance_uuid", "value": None}]
        resp = self.update(deployable_uuid, body)
        return resp

    def allocation(self, deployable_uuid, instance_uuid):
        body = [{"op": "replace", "path": "/instance_uuid",
                "value": instance_uuid}]
        resp = self.update(deployable_uuid, body)
        return resp

    def list(self, limit=None, marker=None, sort_key=None,
             sort_dir=None, **add_filters):
        """List accelerators.

        :param limit:The maximum number of results to return per
                      request, if:

            1) limit > 0, the maximum number of accelerators to return.
            2) limit == 0, return the entire list of accelerators.
            3) limit param is NOT specified (None), the number of items
               returned respect the maximum imposed by the Cyborg API
               (see Cyborg's api.max_limit option).
        :param sort_key: Optional, field used for sorting.

        :param sort_dir: Optional, direction of sorting, either 'asc' (the
                         default) or 'desc'.
        :param extra_filters: Optional, additional filter parameters for query
                         deployable, such as interface_type=pci, host=node-1.
        :return:A list of accelerators.
        """
        res = super(DeployableManager, self).list(limit=limit, marker=marker,
                                                  sort_key=sort_key,
                                                  sort_dir=sort_dir,
                                                  **add_filters)
        return res
