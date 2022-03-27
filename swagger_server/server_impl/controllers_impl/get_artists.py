import logging

from flask import current_app
from swagger_server.models.vox_artists import VoxArtists

logger = logging.getLogger(__name__)

def get_artists(sort_by: str = 'name', limit: int = 1000, asc: bool = True) -> VoxArtists:
    with current_app.app_context():
        logger.info(f"Getting artists. sort_by={sort_by}, asc={asc}, limit={limit}")
        if sort_by == 'name':
            return current_app.vox_cache.get_artist_by(lambda artist: artist.name, asc, limit)
        elif sort_by == 'latest':
            return current_app.vox_cache.get_artist_by(lambda artist: artist.ts_modified, asc, limit)

