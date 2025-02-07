"""The resolvers module"""

from abc import ABC, abstractmethod
from geoenvo.geometry import Geometry


class Resolver(ABC):
    def __init__(self):
        self._geometry = None  # TODO: should be dict?
        self._data = None  # TODO: should be dict?
        self._env_attributes = None  # TODO: should be dict?

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
    def has_ecosystem(self) -> bool:
        pass
