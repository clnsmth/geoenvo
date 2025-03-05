"""
*utilities.py*
"""

from datetime import datetime


def _json_extract(obj, key) -> list:
    """
    Recursively fetches values from nested JSON structures.

    :param obj: A dictionary representing a JSON object.
    :param key: The key to search for.
    :return: A list of values corresponding to the given key.
    """
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


class EnvironmentDataModel:
    """
    Defines a structured model for environmental data, including metadata such
    as data source, creation date, and mapped properties.
    """

    def __init__(self):
        """
        Initializes an ``EnvironmentDataModel`` object with default
        attributes.
        """
        self._data = {
            "type": "Environment",
            "dataSource": {"identifier": None, "name": None},
            "dateCreated": None,
            "properties": {},
            "mappedProperties": [],
        }

    @property
    def data(self) -> dict:
        """
        Retrieves the environmental data model.

        :return: A dictionary representing the environmental data model.
        """
        return self._data

    @data.setter
    def data(self, data: dict):
        """
        Sets the environmental data model.

        :param data: A dictionary containing the environmental data.
        """
        self._data = data

    def set_identifier(self, identifier: str) -> None:
        """
        Sets the identifier for the data source.

        :param identifier: A unique identifier for the data source.
        """
        self.data["dataSource"]["identifier"] = identifier

    def set_data_source(self, data_source: str) -> None:
        """
        Sets the name of the data source.

        :param data_source: The name of the data source.
        """
        self.data["dataSource"]["name"] = data_source

    def set_date_created(self) -> None:
        """
        Sets the creation date of the environmental data model to the current
        timestamp.
        """
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data["dateCreated"] = date_created

    def set_properties(self, properties: list) -> None:
        """
        Sets the properties of the environmental data model.

        :param properties: A list containing environmental properties.
        """
        self.data["properties"] = properties


def get_properties(data, properties: list) -> dict:
    """
    Recursively retrieves specified properties from a response generated by a
     get_environment or query operation.

    :param data: A dictionary containing the JSON response from the
        get_environment operation.
    :param properties: A list of properties to extract from the JSON response.
    :return: A dictionary of the requested properties and their values.
    """
    res = {}
    for a in properties:
        res[a] = _json_extract(data, a)
    return res


def user_agent() -> dict:
    """
    Defines the geoenvo user agent for HTTP requests.

    :return: A dictionary containing the user agent string.
    """
    header = {"user-agent": "geoenvo Python package"}
    return header
