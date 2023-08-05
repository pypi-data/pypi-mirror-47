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


class InnerErrorResponse(Model):
    """InnerErrorResponse.

    :param code:
    :type code: str
    :param inner_error:
    :type inner_error: ~_restclient.models.InnerErrorResponse
    """

    _attribute_map = {
        'code': {'key': 'code', 'type': 'str'},
        'inner_error': {'key': 'innerError', 'type': 'InnerErrorResponse'},
    }

    def __init__(self, code=None, inner_error=None):
        super(InnerErrorResponse, self).__init__()
        self.code = code
        self.inner_error = inner_error
