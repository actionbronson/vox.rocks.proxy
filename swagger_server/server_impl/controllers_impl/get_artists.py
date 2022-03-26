import logging

from swagger_server.server_impl import vox_session_manager
from swagger_server.models.vox_artists import VoxArtists

logger = logging.getLogger(__name__)

def get_artists(sort_by: str = 'name', limit: int = 1000, asc: bool = True) -> VoxArtists:
    logger.info(f"Getting artists. sort_by={sort_by}, asc={asc}, limit={limit}")
    vox_cache = vox_session_manager.get_vox_cache()
    if sort_by == 'name':
        return vox_cache.get_artist_by(lambda artist: artist.name, asc, limit)
    elif sort_by == 'latest':
        return vox_cache.get_artist_by(lambda artist: artist.ts_modified, asc, limit)

