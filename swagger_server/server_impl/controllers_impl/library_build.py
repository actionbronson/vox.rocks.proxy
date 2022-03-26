import logging

from typing import Any, Callable
from hurry.filesize import size

from swagger_server.models.vox_library_creation import VoxLibraryCreation
from swagger_server.models.vox_artist import VoxArtist
from swagger_server.models.vox_album import VoxAlbum
from swagger_server.models.vox_library import VoxLibrary

from swagger_server.server_impl import vox_session_manager

logger = logging.getLogger(__name__)

def library_build(lib_creation: VoxLibraryCreation):
    session = vox_session_manager.get_session()
    vox_library_cache = vox_session_manager.get_vox_cache()
    def _add_artists(artists_json, len_artists):
        artists = [VoxArtist(id=artist['id'], 
                            name=artist['name'], 
                            ts_added=artist['dateAdded'], 
                            ts_modified=artist['lastModified']) for artist in artists_json]
        logger.info(f'Adding {len_artists} artists to library.')
        vox_library_cache.add_artists(artists)

    def _add_albums(albums_json, _):
        albums = [(album['artistId'], VoxAlbum(id=album['id'],
                            name=album['name'], 
                            ts_added=album['dateAdded'],
                            ts_modified=album['lastModified'],
                            format=album['format'],
                            release_year=album['releaseYear'],
                            tracks_count=album['tracksCount'])) for album in albums_json]
        artists_albums = {}
        for artist_id, album in albums:
            albums = artists_albums.setdefault(artist_id, [])
            albums.append(album)
        vox_library_cache.add_artists_albums(artists_albums)

    def _generic_vox_api_fetcher(url: str, func: Callable[[list,int], None]):
        headers={"Authorization": vox_session_manager.get_access_token(),
                "User-Agent": "Loop/0.14.34 (Mac OS X Version 12.1 (Build 21C52))",
                "x-api-version": "2"}
        skip = 0
        while True:
            resp = session.get(url,
                                params={"filter[limit]": 1000, 
                                        "filter[skip]": skip, 
                                        "filter[where][isDeleted]": "false"},
                                headers=headers)
            resp.raise_for_status()
            items: list = resp.json()
            len_items: int = len(items)
            func(items, len_items)
            if len_items < 1000:
                logger.info(f"Received {len_items} items.  Breaking out.")
                break
            else:
                skip += 1000
                logger.info(f"We reached the limit on {url}, length={len_items}.  Fetching more and skipping first {skip}.")

    logger.info(f"Acquiring artists from VOX api, building library cache.")
    _generic_vox_api_fetcher("https://api.vox.rocks/api/artists", _add_artists)
    _generic_vox_api_fetcher("https://api.vox.rocks/api/albums", _add_albums)
    
    account_resp = session.get("https://my.vox.rocks/account/accountSummary")
    account_resp.raise_for_status()
    account_details = account_resp.json()
    return VoxLibrary(size_human=size(account_details['size']), 
                        size=account_details['size'],
                        tracks_count=account_details['tracksCount'],
                        albums_count=vox_library_cache.num_albums(),
                        artists_count=vox_library_cache.num_artists())
