# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestVoxController(BaseTestCase):
    """VoxController integration test stubs"""

    def test_login(self):
        """Test case for login

        Login
        """
        body = User()
        response = self.client.open(
            '/login/{method}'.format(method='method_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
