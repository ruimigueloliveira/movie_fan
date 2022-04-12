import connexion
import six
import json
from flask import request
import pymongo

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server import util

client = pymongo.MongoClient("mongodb+srv://rentalsinc:<password>@rental.hxgwe.mongodb.net/Rental?retryWrites=true&w=majority")
db = client.rentals

def products_get():  # noqa: E501
    """products_get

    Returns all products available # noqa: E501


    :rtype: List[InlineResponse2002]
    """
    prods_ls = []
    for p in db.products.find():
        prods_ls.append(p)

    # f = open("products.json", "r")
    return prods_ls


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

    # client = pymongo.MongoClient("mongodb+srv://rentalsinc:rentals123@rental.hxgwe.mongodb.net/Rental?retryWrites=true&w=majority")
    # client = pymongo.MongoClient("127.0.0.1", 27017)



    dict = {
        '_id': str(request.form.getlist("entity")[0]) + '_' + str(id_),
        'prod_id': str(id_),
        'entity': str(request.form.getlist("entity")[0]),
        'user': str(request.form.getlist("username")[0]),
        'price': str(request.form.getlist("price")[0]),
        'title': str(request.form.getlist("title")[0]),
        'rental_time': str(request.form.getlist("rental_time")[0])
    }

    db.products.insert_one(dict)

    print('Entity: ' + str(request.form.getlist("entity")[0]))
    print('User: ' + str(request.form.getlist("username")[0]))
    print('Rental time: ' + str(request.form.getlist("rental_time")[0]))
    print('Movie ID: ' + str(id_))
    print('Movie Price: ' + str(request.form.getlist("price")[0]))
    print('Movie Title: ' + str(request.form.getlist("title")[0]))

    return "Producted with id " + str(id_) + " added successfully"


def products_id_put(id_):  # noqa: E501
    """products_id_put

    Updates product # noqa: E501

    :param id_:
    :type id_: int

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def user_products_user_id_get(user_id):  # noqa: E501
    """user_products_user_id_get

    Returns the details of the product # noqa: E501

    :param user_id:
    :type user_id: int

    :rtype: InlineResponse2002
    """
    return 'do some magic!'
