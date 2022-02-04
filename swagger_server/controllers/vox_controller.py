import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util

import swagger_server.server_impl.controllers_impl.login as login_impl
import swagger_server.server_impl.controllers_impl.status as status_impl


def login(body, method):  # noqa: E501
    """Login

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param method: The login method.  Only facebook is supported for now.
    :type method: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return login_impl.login(body, method)

def status():  # noqa: E501
    """Status of VOX Proxy

     # noqa: E501


    :rtype: None
    """
    return status_impl.status()
