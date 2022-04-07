# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_v1_access_token_post(self):
        """Test case for v1_access_token_post

        Log-in Step 2 (Tokens) - Give valid authorization code. Return access token if code is valid.
        """
        response = self.client.open(
            '/deti-egs-moviefan/Authentication/1.0.0/v1/access-token',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_v1_auth_token_post(self):
        """Test case for v1_auth_token_post

        Log-in Step 1 (Credentials) - Input valid credentials. Return valid authorization code.
        """
        response = self.client.open(
            '/deti-egs-moviefan/Authentication/1.0.0/v1/auth-token',
            method='POST')
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

    def test_v1_signup_post(self):
        """Test case for v1_signup_post

        Registers an user to the database with the given credentials.
        """
        response = self.client.open(
            '/deti-egs-moviefan/Authentication/1.0.0/v1/signup',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_v1_validate_access_token_post(self):
        """Test case for v1_validate_access_token_post

        Log-in Step 3 (Validation) - Check validity of access token.
        """
        response = self.client.open(
            '/deti-egs-moviefan/Authentication/1.0.0/v1/validate-access-token',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
