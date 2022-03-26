import logging
import requests

from typing import Any, Callable
from swagger_server.models.vox_artist import VoxArtist
from swagger_server.models.vox_album import VoxAlbum
from swagger_server.server_impl import vox_session_manager


logger = logging.getLogger(__name__)

class VoxLibraryCache(object):
    artists_cache: dict
    session: requests.Session

    @staticmethod
    def empty():
        return VoxLibraryCache([])

    def __init__(self, artists: list = []):
        self.session = vox_session_manager.active_session
        self.artists_cache = {artist.id(): {'artist': artist} for artist in artists}
    
    def add_artists(self, artists: list[VoxArtist] = []):
        logger.info(f"Adding {len(artists)} to library cache.")
        self.artists_cache |= {artist.id: {'artist': artist} for artist in artists}
    
    def num_artists(self) -> int:
        return len(self.artists_cache.keys())
    
    def num_albums(self) -> int:
        return sum([len(entry['albums']) for entry in self.artists_cache.values()])

    def get_albums_by(self, id: str, func: Callable[VoxArtist, Any], asc: bool = True, limit: int = None) -> list:
        all_albums = self.artists_cache[id]['albums']
        sorted_albums = sorted(all_albums, key=func, reverse=not(asc))
        logger.info(f"Sorted all {len(all_albums)} albums, limit is {limit}")
        if limit:
            return sorted_albums[:limit]
        else:
            return sorted_albums

    def get_artist_by(self, func: Callable[VoxArtist, Any], asc: bool = True, limit: int = None) -> list:
        all_artists = [artist['artist'] for artist in self.artists_cache.values()]
        sorted_artists = sorted(all_artists, key=func, reverse=not(asc))
        logger.info(f"Sorted all {len(all_artists)} artist, limit is {limit}")
        if limit:
            return sorted_artists[:limit]
        else:
            return sorted_artists

    def get_tracks_by_album(self, album_id: str) -> list:
        # https://api.vox.rocks/api/tracks?filter[limit]=1000&filter[skip]=0&filter[where][albumId][inq][]=61da0b9ebf41726612f9ce60&filter[where][isDeleted]=false
        headers={
            "Authorization": vox_session_manager.get_access_token(),
            "User-Agent": "Loop/0.14.34 (Mac OS X Version 12.1 (Build 21C52))",
            "x-api-version": "2"}
        self.session.get("https://api.vox.rocks/api/tracks", headers=headers, )
        pass

    def add_artists_albums(self, artist_albums: dict[str,list[VoxAlbum]]):
        for artist_id,albums in artist_albums.items():
            artist_albums = self.artists_cache[artist_id].setdefault('albums', [])

            logger.debug(f"Appending {len(albums)} albums to artist: '{artist_id}'.  Already has {len(artist_albums)} albums.")
            artist_albums.extend(albums)