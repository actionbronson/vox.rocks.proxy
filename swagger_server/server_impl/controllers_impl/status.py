import logging
import datetime

from flask import current_app

logger = logging.getLogger(__name__)
    
def status() -> dict:
    with current_app.app_context():
        status = dict(
            status_time=datetime.datetime.now(),
            current_user=current_app.vox_session_manager.get_id(),
            library_details=current_app.vox_library_details)
        return status
