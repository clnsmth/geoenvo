"""The environment module"""

import json


class Environment:
    def __init__(self, data: dict = dict()):
        self._data = data

    def has_environment(self) -> bool:
        if len(self._data) == 0:
            return False
        return True

    def data(self) -> str:  # TODO: remove me
        return self._data
