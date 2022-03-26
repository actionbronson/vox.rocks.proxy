from swagger_server.models.vox_albums import VoxAlbums
from swagger_server.server_impl import vox_session_manager

import logging

logger = logging.getLogger(__name__)

def get_artist_albums(id, sort_by, limit, ascending) -> VoxAlbums:
    vox_cache = vox_session_manager.get_vox_cache()
    logger.info(f"get_artist_albums({id}, {sort_by}, {limit}, {ascending})")
    if sort_by == 'latest':
        sort_by_fn = lambda alb: alb.ts_modified
    elif sort_by == 'name':
        sort_by_fn = lambda alb: alb.name
    else:
        sort_by_fn = lambda alb: alb.release_year
    albums = vox_cache.get_albums_by(id, sort_by_fn, ascending, limit)
    return albums
