import connexion
import six
import json
from flask import request
from werkzeug.datastructures import ImmutableMultiDict

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server import util


def products_get():  # noqa: E501
    """products_get

    Returns all products available # noqa: E501


    :rtype: List[InlineResponse2002]
    """
    f = open("products.json", "r")
    return json.load(f)


def products_id_delete(id_):  # noqa: E501
    """products_id_delete

    Lets the admin delete a product # noqa: E501

    :param id_:
    :type id_: int

    :rtype: None
    """
    return 'do some magic!'


def products_id_get(id_):  # noqa: E501
    """products_id_get

    Returns the details of the product # noqa: E501

    :param id_:
    :type id_: int

    :rtype: InlineResponse200
    """
    return 'do some magic!'


def products_id_post(id_):  # noqa: E501
    """products_id_post

    Add a product for rental # noqa: E501

    :param id_:
    :type id_: int

    :rtype: InlineResponse2001
    """


    print('Movie ID: ' + str(id_))
    print('Movie Price: ' + str(request.form.getlist("price")[0]))
    print('Movie Status: ' + str(request.form.getlist("status")[0]))


    dict = {'id_': id_, 'name': 'Ze'}

    return "Producted with id " + str(id_) + " added successfully"


def products_id_put(id_):  # noqa: E501
    """products_id_put

    Updates product # noqa: E501

    :param id_:
    :type id_: int

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def products_pay_id_put(id_):  # noqa: E501
    """products_pay_id_put

    Rents the product # noqa: E501

    :param id_:
    :type id_: int

    :rtype: InlineResponse200
    """
    return 'do some magic!'
