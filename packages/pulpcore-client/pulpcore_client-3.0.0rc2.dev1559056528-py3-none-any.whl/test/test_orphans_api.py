# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.api.orphans_api import OrphansApi  # noqa: E501
from pulpcore.client.pulpcore.rest import ApiException


class TestOrphansApi(unittest.TestCase):
    """OrphansApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulpcore.api.orphans_api.OrphansApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_orphans_delete(self):
        """Test case for orphans_delete

        Delete orphans  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
