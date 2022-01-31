#!/usr/bin/env python3

import connexion
import logging

from swagger_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'VOX Cloud Proxy'}, pythonic_params=True)
    app.run(port=23456)

if __name__ == '__main__':
    logFormat = '[%(asctime)-15s] %(levelname)s %(name)s - %(message)s' 
    logging.basicConfig(level=logging.INFO, format=logFormat)
    main()
