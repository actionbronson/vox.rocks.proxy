import logging
import datetime

from swagger_server.server_impl import vox_session_manager

logger = logging.getLogger(__name__)
    
def status() -> dict:
    status = dict(
        status_time=datetime.datetime.now(),
        current_user=vox_session_manager.get_id())
    return status
