import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util
import core.login

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
    
    return core.login.login(body, method)
