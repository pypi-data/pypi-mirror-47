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


class RunMetricOperations(object):
    """RunMetricOperations operations.

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

    def post(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, run_id, metric_dto=None, custom_headers=None, raw=False, **operation_config):
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
        :param run_id:
        :type run_id: str
        :param metric_dto:
        :type metric_dto: ~_restclient.models.MetricDto
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or ClientRawResponse if raw=true
        :rtype: None or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.post.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'runId': self._serialize.url("run_id", run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if metric_dto is not None:
            body_content = self._serialize.body(metric_dto, 'MetricDto')
        else:
            body_content = None

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response
    post.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runs/{runId}/metrics'}

    def post_batch(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, run_id, batch_metric_dto=None, custom_headers=None, raw=False, **operation_config):
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
        :param run_id:
        :type run_id: str
        :param batch_metric_dto:
        :type batch_metric_dto: ~_restclient.models.BatchMetricDto
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or ClientRawResponse if raw=true
        :rtype: None or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.post_batch.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'runId': self._serialize.url("run_id", run_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if batch_metric_dto is not None:
            body_content = self._serialize.body(batch_metric_dto, 'BatchMetricDto')
        else:
            body_content = None

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response
    post_batch.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runs/{runId}/batch/metrics'}

    def get(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, metric_id, custom_headers=None, raw=False, **operation_config):
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
        :param metric_id:
        :type metric_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: RunMetricDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.RunMetricDto or
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
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str'),
            'metricId': self._serialize.url("metric_id", metric_id, 'str')
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
            deserialized = self._deserialize('RunMetricDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/metrics/{metricId}'}

    def list(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, filter=None, continuationtoken=None, orderby=None, sortorder=None, top=None, mergestrategytype=None, mergestrategyoptions=None, mergestrategysettingsversion=None, mergestrategysettingsselectmetrics=None, custom_headers=None, raw=False, **operation_config):
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
        :param mergestrategytype: Possible values include: 'Default', 'None',
         'MergeToVector'
        :type mergestrategytype: str
        :param mergestrategyoptions: Possible values include: 'None',
         'ReportUnmergedMetricsValues'
        :type mergestrategyoptions: str
        :param mergestrategysettingsversion:
        :type mergestrategysettingsversion: str
        :param mergestrategysettingsselectmetrics: Possible values include:
         'SelectAll', 'SelectByFirstValueSchema'
        :type mergestrategysettingsselectmetrics: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PaginatedRunMetricDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.PaginatedRunMetricDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.list.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str')
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
        if mergestrategytype is not None:
            query_parameters['mergestrategytype'] = self._serialize.query("mergestrategytype", mergestrategytype, 'str')
        if mergestrategyoptions is not None:
            query_parameters['mergestrategyoptions'] = self._serialize.query("mergestrategyoptions", mergestrategyoptions, 'str')
        if mergestrategysettingsversion is not None:
            query_parameters['mergestrategysettings.version'] = self._serialize.query("mergestrategysettingsversion", mergestrategysettingsversion, 'str')
        if mergestrategysettingsselectmetrics is not None:
            query_parameters['mergestrategysettings.selectmetrics'] = self._serialize.query("mergestrategysettingsselectmetrics", mergestrategysettingsselectmetrics, 'str')

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
            deserialized = self._deserialize('PaginatedRunMetricDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    list.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/metrics'}

    def get_by_query(
            self, subscription_id, resource_group_name, workspace_name, experiment_name, query_params=None, mergestrategytype=None, mergestrategyoptions=None, mergestrategysettingsversion=None, mergestrategysettingsselectmetrics=None, custom_headers=None, raw=False, **operation_config):
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
        :param query_params:
        :type query_params: ~_restclient.models.QueryParamsDto
        :param mergestrategytype: Possible values include: 'Default', 'None',
         'MergeToVector'
        :type mergestrategytype: str
        :param mergestrategyoptions: Possible values include: 'None',
         'ReportUnmergedMetricsValues'
        :type mergestrategyoptions: str
        :param mergestrategysettingsversion:
        :type mergestrategysettingsversion: str
        :param mergestrategysettingsselectmetrics: Possible values include:
         'SelectAll', 'SelectByFirstValueSchema'
        :type mergestrategysettingsselectmetrics: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PaginatedRunMetricDto or ClientRawResponse if raw=true
        :rtype: ~_restclient.models.PaginatedRunMetricDto or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<_restclient.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_by_query.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("subscription_id", subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'experimentName': self._serialize.url("experiment_name", experiment_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if mergestrategytype is not None:
            query_parameters['mergestrategytype'] = self._serialize.query("mergestrategytype", mergestrategytype, 'str')
        if mergestrategyoptions is not None:
            query_parameters['mergestrategyoptions'] = self._serialize.query("mergestrategyoptions", mergestrategyoptions, 'str')
        if mergestrategysettingsversion is not None:
            query_parameters['mergestrategysettings.version'] = self._serialize.query("mergestrategysettingsversion", mergestrategysettingsversion, 'str')
        if mergestrategysettingsselectmetrics is not None:
            query_parameters['mergestrategysettings.selectmetrics'] = self._serialize.query("mergestrategysettingsselectmetrics", mergestrategysettingsselectmetrics, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json-patch+json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        if query_params is not None:
            body_content = self._serialize.body(query_params, 'QueryParamsDto')
        else:
            body_content = None

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('PaginatedRunMetricDto', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_by_query.metadata = {'url': '/history/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/metrics:query'}
