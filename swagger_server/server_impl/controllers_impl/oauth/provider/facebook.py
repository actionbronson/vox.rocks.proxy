import logging
import lxml.html
import requests
import datetime

from urllib.parse import urljoin
from swagger_server.models.user import User

from swagger_server.server_impl import vox_config
from swagger_server.server_impl.controllers_impl.oauth.provider.provider import OAuthProvider

logger = logging.getLogger(__name__)

class FacebookOauthProvider(OAuthProvider):
    def __init__(self):
        self.fb_login_config = vox_config["facebook_oauth"].get()
        pass
    
    def get_session(self):
        return self.session

    def __get_facebook_login_form(self, headers: dict, fb_url: str) -> dict:
        logger.info("Obtaining facebook login form.")
        resp = self.session.get(fb_url)
        resp.raise_for_status()
        html_doc = lxml.html.fromstring(resp.content)
        logging.debug(f"Obtained html doc {html_doc}")
        html_form_fields = html_doc.forms[0].fields
        return dict(url=urljoin(fb_url, html_doc.forms[0].action),
                    form_fields={k: html_form_fields[k] for k in html_form_fields})

    def __get_oauth_response(self, session: requests.Session) -> None:#, ext: str, hash: str):
        fb_url = self.fb_login_config["url"]
        vox_api_key =  self.fb_login_config["api_key"]  #125005697707172
        vox_redirect_url = self.fb_login_config["redirect_url"] # "https://my.vox.rocks/auth/facebook/callback"
        oauth_url = urljoin(fb_url, "/dialog/oauth")
        logger.info(f"Requesting OAuth url: {oauth_url}")
        oauth_params = dict(auth_type="rerequest", response_type="code", redirect_uri=vox_redirect_url, scope="email", 
                        client_id=vox_api_key, ret="login", fbapp_pres=0, tp="unspecified", 
                        cbt=datetime.datetime.now().timestamp() * 1000)
        oauth_resp = self.session.get(oauth_url, params=oauth_params, headers=self.fb_login_config['headers'])
        logger.info(session.cookies.values())
        oauth_resp.raise_for_status()

    def login_provider(self, user: User, session: requests.Session) -> None:
        self.session = session
        fb_url = self.fb_login_config["url"]
        fb_login_headers = self.fb_login_config['headers']
        logger.info(f"Logging in {user.email} using Facebook {fb_url}.")
        fb_login = self.__get_facebook_login_form(session, fb_url)
        login_response = self.session.post(
                fb_login['url'], 
                fb_login['form_fields'] | {"email": user.email, "pass": user.password}, 
                headers = fb_login_headers)
        login_response.raise_for_status()
        logger.info(f"{user.email} is logged in to Facebook {fb_url}.")
        self.__get_oauth_response(session)