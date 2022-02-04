import requests
import logging

from swagger_server.models.user import User
from swagger_server.server_impl.controllers_impl.oauth.provider.provider import OAuthProvider

from swagger_server.server_impl import vox_config

logger = logging.getLogger(__name__)

class VoxOAuthLogin(object):
    def __init__(self, oauth_provider: OAuthProvider) -> None:
        self.oauth_provider = oauth_provider
        self.session = requests.Session()
        pass

    def get_session(self) -> requests.Session:
        return self.session

    def login(self, user: User):
        self.oauth_provider.login_provider(user, self.session)
        vox_login_config = vox_config["vox_oauth"].get()
        vox_oauth_code = ("https://my.vox.rocks/oauth/authorize/decision/premium?"
                        "response_type=code&"
                        f"client_id={vox_login_config['client_id']}&"
                        "redirect_uri=com.coppertino.voxcloud%3A%2F%2Foauth")
        try:
            premium_oauth_code_resp = self.session.get(vox_oauth_code)
            premium_oauth_code_resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Could not obtain VOX Premium code with client_id: {vox_login_config['client_id']}.  Check subscription.")
            raise e

        data = dict(client_id=vox_login_config['client_id'],
                    client_secret=vox_login_config['client_secret'],
                    code=premium_oauth_code_resp.json()['code'],
                    deviceId="Python Client",
                    deviceName="Python Client",
                    grant_type="authorization_code",
                    platform=0,
                    redirect_uri="com.coppertino.voxcloud://oauth",
                    response_type="token")
        try:
            oauth_token_resp = self.session.post("https://my.vox.rocks/oauth/token", data=data)
            oauth_token_resp.raise_for_status()
            return oauth_token_resp
        except requests.exceptions.HTTPError as e:
            logger.error(f"Could not obtain VOX oauth token.")
    