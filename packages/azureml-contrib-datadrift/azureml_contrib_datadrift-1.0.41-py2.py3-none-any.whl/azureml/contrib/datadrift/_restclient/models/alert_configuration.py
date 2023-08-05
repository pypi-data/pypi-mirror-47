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


class AlertConfiguration(Model):
    """AlertConfiguration.

    :param email_addresses:
    :type email_addresses: list[str]
    """

    _attribute_map = {
        'email_addresses': {'key': 'emailAddresses', 'type': '[str]'},
    }

    def __init__(self, email_addresses=None):
        super(AlertConfiguration, self).__init__()
        self.email_addresses = email_addresses
