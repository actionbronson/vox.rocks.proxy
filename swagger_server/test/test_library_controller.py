# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.library_creation import LibraryCreation  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLibraryController(BaseTestCase):
    """LibraryController integration test stubs"""

    def test_library_build(self):
        """Test case for library_build

        Build an in-memory VOX Library
        """
        body = LibraryCreation()
        response = self.client.open(
            '/library/build',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
