# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class VoxLibrary(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, size_human: str=None, tracks_count: int=None, artists_count: int=None, albums_count: int=None, size: int=None):  # noqa: E501
        """VoxLibrary - a model defined in Swagger

        :param size_human: The size_human of this VoxLibrary.  # noqa: E501
        :type size_human: str
        :param tracks_count: The tracks_count of this VoxLibrary.  # noqa: E501
        :type tracks_count: int
        :param artists_count: The artists_count of this VoxLibrary.  # noqa: E501
        :type artists_count: int
        :param albums_count: The albums_count of this VoxLibrary.  # noqa: E501
        :type albums_count: int
        :param size: The size of this VoxLibrary.  # noqa: E501
        :type size: int
        """
        self.swagger_types = {
            'size_human': str,
            'tracks_count': int,
            'artists_count': int,
            'albums_count': int,
            'size': int
        }

        self.attribute_map = {
            'size_human': 'size_human',
            'tracks_count': 'tracks_count',
            'artists_count': 'artists_count',
            'albums_count': 'albums_count',
            'size': 'size'
        }
        self._size_human = size_human
        self._tracks_count = tracks_count
        self._artists_count = artists_count
        self._albums_count = albums_count
        self._size = size

    @classmethod
    def from_dict(cls, dikt) -> 'VoxLibrary':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The VoxLibrary of this VoxLibrary.  # noqa: E501
        :rtype: VoxLibrary
        """
        return util.deserialize_model(dikt, cls)

    @property
    def size_human(self) -> str:
        """Gets the size_human of this VoxLibrary.


        :return: The size_human of this VoxLibrary.
        :rtype: str
        """
        return self._size_human

    @size_human.setter
    def size_human(self, size_human: str):
        """Sets the size_human of this VoxLibrary.


        :param size_human: The size_human of this VoxLibrary.
        :type size_human: str
        """
        if size_human is None:
            raise ValueError("Invalid value for `size_human`, must not be `None`")  # noqa: E501

        self._size_human = size_human

    @property
    def tracks_count(self) -> int:
        """Gets the tracks_count of this VoxLibrary.


        :return: The tracks_count of this VoxLibrary.
        :rtype: int
        """
        return self._tracks_count

    @tracks_count.setter
    def tracks_count(self, tracks_count: int):
        """Sets the tracks_count of this VoxLibrary.


        :param tracks_count: The tracks_count of this VoxLibrary.
        :type tracks_count: int
        """
        if tracks_count is None:
            raise ValueError("Invalid value for `tracks_count`, must not be `None`")  # noqa: E501

        self._tracks_count = tracks_count

    @property
    def artists_count(self) -> int:
        """Gets the artists_count of this VoxLibrary.


        :return: The artists_count of this VoxLibrary.
        :rtype: int
        """
        return self._artists_count

    @artists_count.setter
    def artists_count(self, artists_count: int):
        """Sets the artists_count of this VoxLibrary.


        :param artists_count: The artists_count of this VoxLibrary.
        :type artists_count: int
        """
        if artists_count is None:
            raise ValueError("Invalid value for `artists_count`, must not be `None`")  # noqa: E501

        self._artists_count = artists_count

    @property
    def albums_count(self) -> int:
        """Gets the albums_count of this VoxLibrary.


        :return: The albums_count of this VoxLibrary.
        :rtype: int
        """
        return self._albums_count

    @albums_count.setter
    def albums_count(self, albums_count: int):
        """Sets the albums_count of this VoxLibrary.


        :param albums_count: The albums_count of this VoxLibrary.
        :type albums_count: int
        """

        self._albums_count = albums_count

    @property
    def size(self) -> int:
        """Gets the size of this VoxLibrary.


        :return: The size of this VoxLibrary.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size: int):
        """Sets the size of this VoxLibrary.


        :param size: The size of this VoxLibrary.
        :type size: int
        """
        if size is None:
            raise ValueError("Invalid value for `size`, must not be `None`")  # noqa: E501

        self._size = size
