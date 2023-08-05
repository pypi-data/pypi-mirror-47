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

from msrest.serialization import Model


class CreateParentRunDto(Model):
    """CreateParentRunDto.

    :param num_iterations:
    :type num_iterations: int
    :param training_type: Possible values include: 'TrainFull',
     'TrainAndValidate', 'CrossValidate', 'MeanCrossValidate'
    :type training_type: str or ~_restclient.models.enum
    :param acquisition_function: Possible values include: 'EI', 'PI', 'UCB'
    :type acquisition_function: str or ~_restclient.models.enum
    :param metrics:
    :type metrics: list[str]
    :param primary_metric: Possible values include: 'AUC_weighted',
     'accuracy', 'balanced_accuracy', 'average_precision_score_weighted',
     'precision_score_weighted', 'spearman_correlation',
     'normalized_root_mean_squared_error', 'r2_score',
     'normalized_mean_absolute_error', 'normalized_root_mean_squared_log_error'
    :type primary_metric: str or ~_restclient.models.enum
    :param train_split:
    :type train_split: float
    :param max_time_seconds:
    :type max_time_seconds: int
    :param acquisition_parameter:
    :type acquisition_parameter: float
    :param num_cross_validation:
    :type num_cross_validation: int
    :param target:
    :type target: str
    :param raw_aml_settings_string:
    :type raw_aml_settings_string: str
    :param aml_settings_json_string:
    :type aml_settings_json_string: str
    :param data_prep_json_string:
    :type data_prep_json_string: str
    :param enable_subsampling:
    :type enable_subsampling: bool
    """

    _attribute_map = {
        'num_iterations': {'key': 'numIterations', 'type': 'int'},
        'training_type': {'key': 'trainingType', 'type': 'str'},
        'acquisition_function': {'key': 'acquisitionFunction', 'type': 'str'},
        'metrics': {'key': 'metrics', 'type': '[str]'},
        'primary_metric': {'key': 'primaryMetric', 'type': 'str'},
        'train_split': {'key': 'trainSplit', 'type': 'float'},
        'max_time_seconds': {'key': 'maxTimeSeconds', 'type': 'int'},
        'acquisition_parameter': {'key': 'acquisitionParameter', 'type': 'float'},
        'num_cross_validation': {'key': 'numCrossValidation', 'type': 'int'},
        'target': {'key': 'target', 'type': 'str'},
        'raw_aml_settings_string': {'key': 'rawAMLSettingsString', 'type': 'str'},
        'aml_settings_json_string': {'key': 'amlSettingsJsonString', 'type': 'str'},
        'data_prep_json_string': {'key': 'dataPrepJsonString', 'type': 'str'},
        'enable_subsampling': {'key': 'enableSubsampling', 'type': 'bool'},
    }

    def __init__(self, num_iterations=None, training_type=None, acquisition_function=None, metrics=None, primary_metric=None, train_split=None, max_time_seconds=None, acquisition_parameter=None, num_cross_validation=None, target=None, raw_aml_settings_string=None, aml_settings_json_string=None, data_prep_json_string=None, enable_subsampling=None):
        super(CreateParentRunDto, self).__init__()
        self.num_iterations = num_iterations
        self.training_type = training_type
        self.acquisition_function = acquisition_function
        self.metrics = metrics
        self.primary_metric = primary_metric
        self.train_split = train_split
        self.max_time_seconds = max_time_seconds
        self.acquisition_parameter = acquisition_parameter
        self.num_cross_validation = num_cross_validation
        self.target = target
        self.raw_aml_settings_string = raw_aml_settings_string
        self.aml_settings_json_string = aml_settings_json_string
        self.data_prep_json_string = data_prep_json_string
        self.enable_subsampling = enable_subsampling
