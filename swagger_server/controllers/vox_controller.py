import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.vox_album import VoxAlbum  # noqa: E501
from swagger_server.models.vox_albums import VoxAlbums  # noqa: E501
from swagger_server.models.vox_artists import VoxArtists  # noqa: E501
from swagger_server.models.vox_library import VoxLibrary  # noqa: E501
from swagger_server.models.vox_library_creation import VoxLibraryCreation  # noqa: E501
from swagger_server.models.vox_tracks import VoxTracks  # noqa: E501
from swagger_server import util

import swagger_server.server_impl.controllers_impl.get_album_by_id as get_album_by_id_impl
import swagger_server.server_impl.controllers_impl.get_artist_albums as get_artist_albums_impl
import swagger_server.server_impl.controllers_impl.get_artists as get_artists_impl
import swagger_server.server_impl.controllers_impl.get_tracks_by_album as get_tracks_by_album_impl
import swagger_server.server_impl.controllers_impl.library_build as library_build_impl
import swagger_server.server_impl.controllers_impl.login as login_impl
import swagger_server.server_impl.controllers_impl.status as status_impl


def get_album_by_id(id):  # noqa: E501
    """Get single album from VOX Lbrary, by id

     # noqa: E501

    :param id: The VOX album id.
    :type id: str

    :rtype: VoxAlbum
    """
    return get_album_by_id_impl.get_album_by_id(id)

def get_artist_albums(artist_id, sort_by, limit, ascending):  # noqa: E501
    """Get albums from artist from VOX Lbrary, by artist id

     # noqa: E501

    :param artist_id: The VOX artist id.
    :type artist_id: str
    :param sort_by: sort by name or latest.
    :type sort_by: str
    :param limit: limit number of items returned
    :type limit: int
    :param ascending: ascending
    :type ascending: bool

    :rtype: VoxAlbums
    """
    return get_artist_albums_impl.get_artist_albums(artist_id, sort_by, limit, ascending)

def get_artists(sort_by, limit, ascending):  # noqa: E501
    """Get artists from VOX Lbrary

     # noqa: E501

    :param sort_by: sort by name or latest.
    :type sort_by: str
    :param limit: limit number of items returned
    :type limit: int
    :param ascending: ascending
    :type ascending: bool

    :rtype: VoxArtists
    """
    return get_artists_impl.get_artists(sort_by, limit, ascending)

def get_tracks_by_album(album_id):  # noqa: E501
    """Get tracks from VOX Lbrary, by album id

     # noqa: E501

    :param album_id: The VOX album id.
    :type album_id: str

    :rtype: VoxTracks
    """
    return get_tracks_by_album_impl.get_tracks_by_album(album_id)

def library_build(body):  # noqa: E501
    """Build an in-memory VOX Library

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: VoxLibrary
    """
    if connexion.request.is_json:
        body = VoxLibraryCreation.from_dict(connexion.request.get_json())  # noqa: E501
    return library_build_impl.library_build(body)

def login(body, method):  # noqa: E501
    """Login

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param method: The login method.  Only facebook is supported for now.
    :type method: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return login_impl.login(body, method)

def status():  # noqa: E501
    """Status of VOX Proxy

     # noqa: E501


    :rtype: None
    """
    return status_impl.status()
