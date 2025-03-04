"""
*data_source.py*
"""

from abc import ABC, abstractmethod
from typing import List

from geoenvo.geometry import Geometry
from geoenvo.environment import Environment
from geoenvo.response import Response


class DataSource(ABC):
    """
    Abstract base class for data sources that provide environmental information
    based on geographic queries. Implementing classes must define methods for
    resolving spatial geometries to environmental descriptions.
    """

    def __init__(self):
        """
        Initializes the DataSource with placeholders for geometry, data, and
        properties.
        """
        self._geometry = None  # TODO: should be dict?
        self._data = None  # TODO: should be dict?
        self._properties = None  # TODO: should be dict?

    @property
    @abstractmethod
    def geometry(self) -> dict:
        """
        Retrieves the geometry associated with the data source.

        :return: A dictionary representing the geometry.
        """
        pass

    @geometry.setter
    @abstractmethod
    def geometry(self, geometry: dict):
        """
        Sets the geometry for querying the data source.

        :param geometry: A dictionary representing the geometry.
        """
        pass

    @property
    @abstractmethod
    def data(self) -> dict:
        """
        Retrieves the data returned by the data source.

        :return: A dictionary containing retrieved environmental data.
        """
        pass

    @data.setter
    @abstractmethod
    def data(self, data: dict):
        """
        Sets the environmental data for the data source.

        :param data: A dictionary containing environmental data.
        """
        pass

    @property
    @abstractmethod
    def properties(self) -> dict:
        """
        Retrieves the properties associated with the data source.

        :return: A dictionary containing metadata and additional properties.
        """
        pass

    @properties.setter
    @abstractmethod
    def properties(self, properties: dict):
        """
        Sets the properties for the data source.

        :param properties: A dictionary containing metadata and additional
            properties.
        """
        pass

    @abstractmethod
    def resolve(self, geometry: Geometry) -> List[Environment]:
        """
        Resolves a given geometry to environmental descriptions using the data
        source.

        :param geometry: The geographic location to resolve.
        :return: A list of Environment containing environmental descriptions.
        """
        pass

    @abstractmethod
    def convert_data(self) -> List[Environment]:
        """
        Converts raw data from the data source into a standardized format.

        :return: A list of Environment representing converted environmental
            data.
        """
        pass

    @abstractmethod
    def unique_environment(self) -> List[dict]:
        """
        Extracts unique environmental descriptions from the data source.

        :return: A list of dictionaries containing unique environmental
            descriptions.
        """
        pass

    @abstractmethod
    def has_environment(self) -> bool:
        """
        Determines whether the data source contains environmental information
        for the given geometry.

        :return: ``True`` if environmental data is available, otherwise
            ``False``.
        """
        pass
