########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

from cloudify_rest_client.responses import ListResponse


class Secret(dict):

    def __init__(self, secret):
        super(Secret, self).__init__()
        self.update(secret)

    @property
    def key(self):
        """
        :return: The key of the secret.
        """
        return self.get('key')

    @property
    def value(self):
        """
        :return: The value of the secret.
        """
        return self.get('value')

    @property
    def created_at(self):
        """
        :return: Secret creation date.
        """
        return self.get('created_at')

    @property
    def updated_at(self):
        """
        :return: Secret modification date.
        """
        return self.get('updated_at')


class SecretsClient(object):

    def __init__(self, api):
        self.api = api

    def create(self, key, value, private_resource=False):
        query_params = {'private_resource': private_resource}
        data = {'value': value}
        response = self.api.put('/secrets/{0}'.format(key),
                                params=query_params,
                                data=data)
        return Secret(response)

    def update(self, key, value):
        data = {'value': value}
        response = self.api.patch('/secrets/{0}'.format(key), data=data)

        return Secret(response)

    def get(self, key):
        response = self.api.get('/secrets/{0}'.format(key))
        return Secret(response)

    def list(self, sort=None, is_descending=False, **kwargs):
        """
        Returns a list of currently stored secrets.

        :param sort: Key for sorting the list.
        :param is_descending: True for descending order, False for ascending.
        :param kwargs: Optional filter fields. For a list of available fields
               see the REST service's models.Secret.fields
        :return: Secrets list.
        """

        params = kwargs
        if sort:
            params['_sort'] = '-' + sort if is_descending else sort

        response = self.api.get('/secrets', params=params)
        return ListResponse([Secret(item) for item in response['items']],
                            response['metadata'])

    def delete(self, key):
        response = self.api.delete('/secrets/{0}'.format(key))
        return Secret(response)

    def set_global(self, key):
        """
        Updates the secret's availability to global

        :param key: Secret's key to update.
        :return: The secret.
        """
        return self.api.patch('/secrets/{0}/set-global'.format(key))
