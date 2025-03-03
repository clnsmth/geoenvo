"""The utils module"""

from datetime import datetime


def _json_extract(obj, key):
    """Recursively fetch values from nested JSON.

    Parameters
    ----------
    obj : dict
        A JSON object
    key : str
        The key to search for

    Returns
    -------
    arr : list
        A list of values for the given key
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


class EnvironmentDataModel:  # TODO: rename to EnvironmentDataModel
    def __init__(self):
        self._data = {
            "type": "Environment",
            "dataSource": {"identifier": None, "name": None},
            "dateCreated": None,
            "properties": {},
            "mappedProperties": [],
        }

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data

    # TODO convert to getter/setter pair
    def set_identifier(self, identifier):
        self.data["dataSource"]["identifier"] = identifier

    # TODO convert to getter/setter pair
    def set_data_source(self, data_source):
        self.data["dataSource"]["name"] = data_source

    # TODO convert to getter/setter pair
    def set_date_created(self):
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data["dateCreated"] = date_created

    # TODO convert to getter/setter pair
    def set_properties(self, properties):
        self.data["properties"] = properties


def get_properties(data, properties):
    """Recursively get properties of a response from an resolve or query
    opperation.

    Parameters
    ----------
    data : dict
        A dictionary of the JSON response from the resolve operation.
    properties : list
        A list of properties to extract from the JSON response. These are
        defined in the map service's layer's definition.

    Returns
    -------
    res : dict
        A dictionary of the requested properties and their values.

    """
    # TODO Get properties/features by source? This would simplify the
    #  methods calls, unless this functionality is needed elsewhere (e.g.
    #  getting other names from response dictionaries).
    res = {}
    for a in properties:
        res[a] = _json_extract(data, a)
    return res


def user_agent():
    """Define the geoenvo user agent in HTTP requests

    For use with the `header` parameter of the requests library.

    Returns
    -------
    dict
        User agent
    """
    header = {"user-agent": "geoenvo Python package"}
    return header
