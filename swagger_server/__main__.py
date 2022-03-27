#!/usr/bin/env python3

import connexion
import logging
import click
from swagger_server import encoder
from flask import current_app, g
from swagger_server.models.vox_library_creation import VoxLibraryCreation

import swagger_server.server_impl.controllers_impl.login as login_impl
import swagger_server.server_impl.controllers_impl.library_build as library_build_impl

from swagger_server.models.user import User
from swagger_server.server_impl.vox_session_manager import VoxSessionManager

logFormat = '[%(asctime)-15s] %(levelname)s %(name)s - %(message)s' 
logging.basicConfig(level=logging.INFO, format=logFormat)
logger = logging.getLogger(__name__)

@click.command()
@click.option('--email', help='email for login')
@click.option('--password', help='password for login')
@click.option('--method', help="login method")
@click.option('--library-build', help="build library", default=True)
def run(email, password, method, library_build):
    app = connexion.App(__name__, specification_dir='./swagger/')
    vox_session_manager = VoxSessionManager()
    with app.app.app_context():
        current_app.vox_session_manager = vox_session_manager
        if email is not None:
            logger.info(f"Automatic logging in with {method} using {email}")
            login_impl.login(User(email, password), method)
            if library_build:
                vox_library_details = library_build_impl.library_build(VoxLibraryCreation())
                logger.info(f"Built library: {vox_library_details}")

        app.app.json_encoder = encoder.JSONEncoder
        app.add_api('swagger.yaml', arguments={'title': 'VOX Cloud Proxy'}, pythonic_params=True)
        logger.info(current_app.vox_session_manager)
        app.run(port=23456, ssl_context=('cert.pem', 'key.pem'))

if __name__ == '__main__':
    #requests_log = logging.getLogger("requests.packages.urllib3")
    #requests_log.setLevel(logging.DEBUG)
    #requests_log.propagate = True
    #import http.client as http_client
    #http_client.HTTPConnection.debuglevel = 1
    run()
