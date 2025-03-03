"""
environment.py
==============

This module defines the ``Environment`` class, which encapsulates environmental
descriptions retrieved from a ``DataSource``. It provides a structured
representation of environmental data, allowing for efficient access and
manipulation.

Key functionalities of this module include:

- Storing and managing environmental data in a structured format.
- Providing access to environmental properties through a simple interface.
"""

import json


class Environment:
    """
    The Environment class represents environmental descriptions retrieved from
    a ``DataSource``. It provides a structured way to store and manage
    environmental data.
    """

    def __init__(self, data: dict = dict()):
        """
        Initializes an Environment object with the given data.

        :param data: A dictionary containing environmental data.
        """
        self._data = data

    @property
    def data(self) -> dict:
        """
        Retrieves the stored environmental data.

        :return: A dictionary representing the environmental data.
        """
        return self._data

    @data.setter
    def data(self, data: dict):
        """
        Updates the environmental data.

        :param data: A dictionary containing updated environmental data.
        """
        self._data = data
