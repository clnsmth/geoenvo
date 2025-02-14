"""The resolvers module"""

from abc import ABC, abstractmethod
from geoenvo.geometry import Geometry


class Resolver(ABC):
    def __init__(self):
        self._geometry = None  # TODO: should be dict?
        self._data = None  # TODO: should be dict?
        self._env_attributes = None  # TODO: should be dict?

    @property
    @abstractmethod
    def geometry(self):
        pass

    @geometry.setter
    @abstractmethod
    def geometry(self, geometry: dict):
        pass

    @property
    @abstractmethod
    def data(self):
        pass

    @data.setter
    @abstractmethod
    def data(self, data: dict):
        pass

    @property
    @abstractmethod
    def env_attributes(self):
        pass

    @env_attributes.setter
    @abstractmethod
    def env_attributes(self, env_attributes: dict):
        pass

    @abstractmethod
    def resolve(self, geometry: Geometry) -> list:
        pass

    @abstractmethod
    def convert_data(self, data) -> list:
        pass

    @abstractmethod
    def unique_environment(self) -> list:
        pass

    @abstractmethod
    def has_environment(self) -> bool:
        pass
