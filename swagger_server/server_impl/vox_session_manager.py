
from abc import ABC
from urllib import request
import requests
import logging 

logger = logging.getLogger(__name__)

class NoActiveSession(Exception):
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