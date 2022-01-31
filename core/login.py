import requests
import logging
import lxml.html
from urllib.parse import urljoin, parse_qs, quote_plus
import datetime

# import core.config.vox_config
from core import vox_config
from core import vox_sessions

from swagger_server.models.user import User

logger = logging.getLogger(__name__)

def login(user: User, method: str):
    def no_login(user: User):
        status_code = 400
        logger.error("Logging in with {method} is not implemented right now.")
        return {"user": user.email}, status_code

    METHODS = {"facebook": login_facebook}
    login_fn = METHODS.get(method.lower(), no_login)
    return {"user": user.email}, login_fn(user)

def __get_facebook_login(session: requests.Session, headers: dict, fb_url: str) -> dict:
    logger.info("Obtaining facebook login form.")
    resp = session.get(fb_url, headers=headers)
    resp.raise_for_status()
    html_doc = lxml.html.fromstring(resp.content)
    logging.debug(f"Obtained html doc {html_doc}")
    html_form_fields = html_doc.forms[0].fields
    return dict(url=urljoin(fb_url, html_doc.forms[0].action),
                form_fields={k: html_form_fields[k] for k in html_form_fields})

def __extract_facebook_ext_hash(fb_login_resp: requests.Response):
    logger.info(f"Extracting ext and hash frorm facebook login.")

    login_doc = lxml.html.fromstring(fb_login_resp.content)
    iframes_elems = login_doc.xpath("//iframe") 
    iframe_elem = iframes_elems[0]
    src_url = iframe_elem.get('src')
    url_params = parse_qs(src_url)
    ext, hash = url_params.get('ext')[0], url_params.get('hash')[0]
    logger.debug(f"Obtained ext: {ext} and hash: {hash}")
    return ext, hash

def login_facebook(user: User):
    logger.info(f"Logging in {user.email} using Facebook OAuth.")
    fb_login_config = vox_config["facebook_oauth"].get()
    logger.debug(fb_login_config)
    fb_url = fb_login_config["url"]
    vox_api_key =  fb_login_config["api_key"]  #125005697707172
    vox_redirect_url = fb_login_config["redirect_url"] # "https://my.vox.rocks/auth/facebook/callback"
    vox_cancel_url = fb_login_config["cancel_url"] #"https://my.vox.rocks/auth/facebook/callback?error=access_denied&error_code=200&error_description=Permissions+error&error_reason=user_denied#_=_"
    fb_login_headers = fb_login_config['headers']
    referer_url = (f"{fb_url}/login.php?skip_api_login=1&api_key={vox_api_key}&"
                    "kid_directed_site=0&app_id={vox_api_key}&signed_next=1&"
                    "next={quote_plus(vox_redirect_url)}&"
                    "cancel_url={quote_plus(vox_cancel_url)}&"
                    "display=page&locale=en_US&pl_dbl=0")
    fb_login_headers['referer'] = referer_url
    logging.info(f"Logging in to VOX Cloud with username: '{user.email}'")
    session = requests.Session()
    vox_sessions[user.email] = session
    fb_login = __get_facebook_login(session, fb_login_headers, fb_url)
    login_response = session.post(fb_login['url'], fb_login['form_fields'] | {"email": user.email, "pass": user.password, "cancel_url": vox_cancel_url}, headers = fb_login_headers)
    login_response.raise_for_status()
    ext, hash = __extract_facebook_ext_hash(login_response)
    oauth_url = urljoin(fb_url, "/dialog/oauth")
    logger.info(f"Now authenticating with VOX through OAuth url: {oauth_url}")
    oauth_params = dict(auth_type="rerequest", response_type="code", redirect_uri=vox_redirect_url, scope="email", 
                        client_id=vox_api_key, ret="login", fbapp_pres=0, tp="unspecified", 
                        cbt=datetime.datetime.now().timestamp() * 1000, ext=ext, hash=hash)
    session.get(oauth_url, params=oauth_params, headers=fb_login_headers)
    #yo = session.get('https://my.vox.rocks/account/getapiaccesstoken')
    #auth_url = "https://my.vox.rocks/oauth/authorize/decision/premium?response_type=code&client_id=ca091e45e3282bcb6d9465ed7780c7bc&redirect_uri=com.coppertino.voxcloud%3A%2F%2Foauth&new_cabinet=1&vuid=7fecddf0-9684-11e9-bc86-5fca40692da7&sid=hmgcqq4hlghu8lj74k"
    #print(yo.content)

    status_code = 200
    return status_code
    



