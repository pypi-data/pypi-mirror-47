# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 2.3.33.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse

from .. import models


class ExperimentOperations(object):
    """ExperimentOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer

        self.config = config

    def get(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ExperimentDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.ExperimentDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('ExperimentDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}'}

    def create(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, custom_headers=None, raw=False, **operation_config):
        """Creates the named experiment, or returns an existing experiment with
        that name.

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param experiment_name:
        :type experiment_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ExperimentDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.ExperimentDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.create.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('ExperimentDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    create.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}'}

    def list(
            self, subscription_id, resource_group_name, workspace_name, filter=None, continuationtoken=None, orderby=None, sortorder=None, top=None, custom_headers=None, raw=False, **operation_config):
        """

        :param subscription_id: The Azure Subscription ID.
        :type subscription_id: str
        :param resource_group_name: Name of the resource group in which the
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: The name of the workspace.
        :type workspace_name: str
        :param filter:
        :type filter: str
        :param continuationtoken:
        :type continuationtoken: str
        :param orderby:
        :type orderby: list[str]
        :param sortorder: Possible values include: 'Asc', 'Desc'
        :type sortorder: str
        :param top:
        :type top: int
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PaginatedExperimentDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.PaginatedExperimentDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.list.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if filter is not None:
            query_parameters['$filter'] = self._serialize.query("filter", filter, 'str')
        if continuationtoken is not None:
            query_parameters['$continuationtoken'] = self._serialize.query("continuationtoken", continuationtoken, 'str')
        if orderby is not None:
            query_parameters['$orderby'] = self._serialize.query("orderby", orderby, '[str]', div=',')
        if sortorder is not None:
            query_parameters['$sortorder'] = self._serialize.query("sortorder", sortorder, 'str')
        if top is not None:
            query_parameters['$top'] = self._serialize.query("top", top, 'int')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('PaginatedExperimentDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    list.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments'}
