# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_products_get(self):
        """Test case for products_get

        
        """
        response = self.client.open(
            '/movie-fan/Rental/v1/products',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_id_delete(self):
        """Test case for products_id_delete

        
        """
        response = self.client.open(
            '/movie-fan/Rental/v1/products/{id_}'.format(id_=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_id_get(self):
        """Test case for products_id_get

        
        """
        response = self.client.open(
            '/movie-fan/Rental/v1/products/{id_}'.format(id_=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_id_post(self):
        """Test case for products_id_post

        
        """
        response = self.client.open(
            '/movie-fan/Rental/v1/products/{id_}'.format(id_=56),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_products_id_put(self):
        """Test case for products_id_put

        
        """
        response = self.client.open(
            '/movie-fan/Rental/v1/products/{id_}'.format(id_=56),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_products_user_id_get(self):
        """Test case for user_products_user_id_get

        
        """
        response = self.client.open(
            '/movie-fan/Rental/v1/user-products/{user_id}'.format(user_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
