# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class InlineResponse2001(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, product_id: str=None, product_name: str=None, state: str=None, price: float=None, date_limit: str=None):  # noqa: E501
        """InlineResponse2001 - a model defined in Swagger

        :param product_id: The product_id of this InlineResponse2001.  # noqa: E501
        :type product_id: str
        :param product_name: The product_name of this InlineResponse2001.  # noqa: E501
        :type product_name: str
        :param state: The state of this InlineResponse2001.  # noqa: E501
        :type state: str
        :param price: The price of this InlineResponse2001.  # noqa: E501
        :type price: float
        :param date_limit: The date_limit of this InlineResponse2001.  # noqa: E501
        :type date_limit: str
        """
        self.swagger_types = {
            'product_id': str,
            'product_name': str,
            'state': str,
            'price': float,
            'date_limit': str
        }

        self.attribute_map = {
            'product_id': 'product_id',
            'product_name': 'product_name',
            'state': 'state',
            'price': 'price',
            'date_limit': 'date_limit'
        }
        self._product_id = product_id
        self._product_name = product_name
        self._state = state
        self._price = price
        self._date_limit = date_limit

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2001':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_1 of this InlineResponse2001.  # noqa: E501
        :rtype: InlineResponse2001
        """
        return util.deserialize_model(dikt, cls)

    @property
    def product_id(self) -> str:
        """Gets the product_id of this InlineResponse2001.


        :return: The product_id of this InlineResponse2001.
        :rtype: str
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id: str):
        """Sets the product_id of this InlineResponse2001.


        :param product_id: The product_id of this InlineResponse2001.
        :type product_id: str
        """

        self._product_id = product_id

    @property
    def product_name(self) -> str:
        """Gets the product_name of this InlineResponse2001.


        :return: The product_name of this InlineResponse2001.
        :rtype: str
        """
        return self._product_name

    @product_name.setter
    def product_name(self, product_name: str):
        """Sets the product_name of this InlineResponse2001.


        :param product_name: The product_name of this InlineResponse2001.
        :type product_name: str
        """

        self._product_name = product_name

    @property
    def state(self) -> str:
        """Gets the state of this InlineResponse2001.


        :return: The state of this InlineResponse2001.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state: str):
        """Sets the state of this InlineResponse2001.


        :param state: The state of this InlineResponse2001.
        :type state: str
        """

        self._state = state

    @property
    def price(self) -> float:
        """Gets the price of this InlineResponse2001.


        :return: The price of this InlineResponse2001.
        :rtype: float
        """
        return self._price

    @price.setter
    def price(self, price: float):
        """Sets the price of this InlineResponse2001.


        :param price: The price of this InlineResponse2001.
        :type price: float
        """

        self._price = price

    @property
    def date_limit(self) -> str:
        """Gets the date_limit of this InlineResponse2001.


        :return: The date_limit of this InlineResponse2001.
        :rtype: str
        """
        return self._date_limit

    @date_limit.setter
    def date_limit(self, date_limit: str):
        """Sets the date_limit of this InlineResponse2001.


        :param date_limit: The date_limit of this InlineResponse2001.
        :type date_limit: str
        """

        self._date_limit = date_limit