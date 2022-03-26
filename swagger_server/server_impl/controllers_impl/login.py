import requests
import logging

from flask import jsonify
from swagger_server.server_impl.controllers_impl.oauth.provider.facebook import FacebookOauthProvider
from swagger_server.server_impl import vox_session_manager
from swagger_server.models.user import User
from swagger_server.server_impl.controllers_impl.oauth.vox import VoxOAuthLogin

logger = logging.getLogger(__name__)

def login(user: User, method: str):
    def no_login(user: User):
        return requests.Response(
            f"Logging in with {method} is not implemented right now.", 
            status=400)

    METHODS = {"facebook": login_facebook}
    login_fn = METHODS.get(method.lower(), no_login)
    return login_fn(user)

def login_facebook(user: User):
    vox_oauth_login = VoxOAuthLogin(FacebookOauthProvider())
    vox_oauth_resp = vox_oauth_login.login(user)
    vox_session_manager.set_session(user.email, vox_oauth_login.get_session(), vox_oauth_resp.json())
    response = jsonify(vox_session_manager.get_details())
    return response
