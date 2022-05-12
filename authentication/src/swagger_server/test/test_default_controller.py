# coding: utf-8

from __future__ import absolute_import

import requests
from swagger_server.test import BaseTestCase

PORT = 8001


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
                       'Response body is : ' + response.json())

    def test_v1_auth_token_post(self):
        """Test case for v1_auth_token_post

        Log-in Step 1 (Credentials) - Input valid credentials. Return valid authorization code.
        """
        response = requests.post(
            f"http://localhost:{PORT}/deti-egs-moviefan/Authentication/1.0.0/v1/auth-token",
            json=dict(username="user1", email="user1@it.org", password="user1Pa$$")
        )
        self.assert200(response,
                       'Response body is : ' + response.json())

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
                       'Response body is : ' + response.json())

    def test_v1_validate_access_token_post(self):
        """Test case for v1_validate_access_token_post

        Log-in Step 3 (Validation) - Check validity of access token.
        """
        response = requests.post(
            url=f'http://localhost:{PORT}/deti-egs-moviefan/Authentication/1.0.0/v1/validate-access-token',
            json=dict(
                auth_code='31d38d6e8ce7ab42f34467135aa19225982f9e8965595bbe74f8734'
                          '8a16a9455c4387cc5d66f02b68d76f5310e7cdd76db98a09cfdeffcb1a50f7e145122b044',
                access_token='07cad294e65af23925cc85cf9a435ba2d8cd6e3bd52433736a0dfba29e50c499f79f31'
                             '1870ece437b16a62c79ee9f7b74a495020d68c43d1db17d5880efadb13-ds1652374634009943200'
            )
        )
        self.assert200(response,
                       'Response body is : ' + response.json())

    def test_v1_signout_post(self):
        """Test case for v1_signout_post

        Deletes an user from the registry.
        """
        response = requests.post(
            f"http://localhost:{PORT}/deti-egs-moviefan/Authentication/1.0.0/v1/signout",
            json=dict(username="user1", email="user1@it.org", password="user1Pa$$")
        )
        self.assert200(response,
                       'Response body is : ' + response.json())


if __name__ == '__main__':
    import unittest

    unittest.main()
