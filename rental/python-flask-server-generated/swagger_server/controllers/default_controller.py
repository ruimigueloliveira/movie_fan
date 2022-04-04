import connexion
import six
import json

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


def products_id_delete(id):  # noqa: E501
    """products_id_delete

    Lets the admin delete a product # noqa: E501

    :param id:
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def products_id_get(id):  # noqa: E501
    """products_id_get

    Returns the details of the product # noqa: E501

    :param id:
    :type id: int

    :rtype: InlineResponse200
    """
    f = open("products.json", "r")
    return json.load(f)

def products_id_post(id):  # noqa: E501
    """products_id_post

    Add a product for rental # noqa: E501

    :param id:
    :type id: int

    :rtype: InlineResponse2001
    """

    print("POST WORKING")
    # try:
    #     print("ENTRA AQYU")
    #     dict1 = {
    #         "product4": {
    #             "product_id": str(id),
    #             "product_name": "product4",
    #             "state": "free",
    #             "price": 0,
    #             "date_limit": "december"
    #         }
    #     }
    #
    #     # the json file where the output must be stored
    #     out_file = open("products.json", "w")
    #
    #     json.dump(dict1, out_file, indent = 6)
    #
    #     out_file.close()
    #     return 'Product added'
    # except:
    #     return 'Failed to add a product'

    return 'Failed to add a product'



def products_id_put(id):  # noqa: E501
    """products_id_put

    Updates product # noqa: E501

    :param id:
    :type id: int

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def products_pay_id_put(id):  # noqa: E501
    """products_pay_id_put

    Rents the product # noqa: E501

    :param id:
    :type id: int

    :rtype: InlineResponse200
    """
    return 'do some magic!'
