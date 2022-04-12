# coding: utf-8

from __future__ import absolute_import

import requests
from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase

PORT = 8080


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_v1_signup_post(self):
        """Test case for v1_signup_post

        Registers an user to the database with the given credentials.
        """
        response = requests.post(
            f"http://localhost:{PORT}/deti-egs-moviefan/Authentication/1.0.0/v1/signup",
            json=dict(username="user1", email="user1@it.org", password="user1Pa$$")
        )
        self.assert200(response,
                       'Response body is : ' + response.text)

    def test_v1_auth_token_post(self):
        """Test case for v1_auth_token_post

        Log-in Step 1 (Credentials) - Input valid credentials. Return valid authorization code.
        """
        response = requests.post(
            f"http://localhost:{PORT}/deti-egs-moviefan/Authentication/1.0.0/v1/auth-token",
            json=dict(username="user1", email="user1@it.org", password="user1Pa$$")
        )
        self.assert200(response,
                       'Response body is : ' + response.text)

    def test_v1_access_token_post(self):
        """Test case for v1_access_token_post

        Log-in Step 2 (Tokens) - Give valid authorization code. Return access token if code is valid.
        """
        response = requests.post(
            f"http://localhost:{PORT}/deti-egs-moviefan/Authentication/1.0.0/v1/access-token",
            json=dict(
                authtoken='31d38d6e8ce7ab42f34467135aa19225982f9e8965595bbe74f8734'
                          '8a16a9455c4387cc5d66f02b68d76f5310e7cdd76db98a09cfdeffcb1a50f7e145122b044',
                username="user1", email="user1@it.org", password="user1Pa$$"
            )
        )
        self.assert200(response,
                       'Response body is : ' + response.text)

    def test_v1_validate_access_token_post(self):
        """Test case for v1_validate_access_token_post

        Log-in Step 3 (Validation) - Check validity of access token.
        """
        response = requests.post(
            url=f'http://localhost:{PORT}/deti-egs-moviefan/Authentication/1.0.0/v1/validate-access-token',
            json=dict(
                auth_code='31d38d6e8ce7ab42f34467135aa19225982f9e8965595bbe74f8734'
                          '8a16a9455c4387cc5d66f02b68d76f5310e7cdd76db98a09cfdeffcb1a50f7e145122b044',
                access_token="4f4401760667d012a56cd4f7c454ffe3c705dcfa7ee9eaddd2f170087721817826035"
                             "58dbc4daa4456efc0347357d380e4274ab599df1845f43cf424ba6f7af71652367634526979600"
            )
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_v1_signout_post(self):
        """Test case for v1_signout_post

        Deletes an user from the registry.
        """
        response = self.client.open(
            '/deti-egs-moviefan/Authentication/1.0.0/v1/signout',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
