from abc import ABC
from urllib import request
import requests
import logging

logger = logging.getLogger(__name__)

class NoActiveSession(Exception):
    pass

class NoAccessibleFileCloud(Exception):
    pass

class VoxSessionManager(object):
    def __init__(self):
        logger.info("Initializing empty session.")
        self.active_session = None

    def set_session(self, id: str, vox_session: requests.Session, vox_details: dict):
        self.active_session = dict(id=id, session=vox_session, details=vox_details)
        logger.info(f"Updated active_session -> [{id}]: {vox_details}")

    def get_details(self) -> dict:
        if not(self.active_session):
            raise NoActiveSession()
        return self.active_session['details']

    def get_access_token(self) -> str:
        return self.get_details()['access_token']

    def get_session(self) -> requests.Session:
        if not(self.active_session):
            raise NoActiveSession()
        return self.active_session['session']

    def get_id(self) -> str:
        if not(self.active_session):
            raise NoActiveSession()
        return self.active_session['id']

    def is_active(self) -> bool:
        return self.active_session != None

    def get_cloud(self, all: bool = False) -> str:
        file_cloud: list = self.get_details()['fileCloud']
        if len(file_cloud['clouds']) == 0:
            raise NoAccessibleFileCloud()
        else:
            return file_cloud['clouds'][1]

    def get_cloud_token(self) -> str:
        file_cloud: list = self.get_details()['fileCloud']
        return file_cloud['token']
