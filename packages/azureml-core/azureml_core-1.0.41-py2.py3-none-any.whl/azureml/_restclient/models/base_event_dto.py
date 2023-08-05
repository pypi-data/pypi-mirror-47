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


class BaseEventDto(Model):
    """BaseEventDto.

    :param timestamp:
    :type timestamp: datetime
    :param name:
    :type name: str
    :param data:
    :type data: object
    """

    _attribute_map = {
        'timestamp': {'key': 'timestamp', 'type': 'iso-8601'},
        'name': {'key': 'name', 'type': 'str'},
        'data': {'key': 'data', 'type': 'object'},
    }

    def __init__(self, timestamp=None, name=None, data=None):
        super(BaseEventDto, self).__init__()
        self.timestamp = timestamp
        self.name = name
        self.data = data
