"""The environment module"""

import json


class Environment:
    def __init__(self, data: dict = dict()):
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data
