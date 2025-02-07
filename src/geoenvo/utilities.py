"""The utils module"""

import importlib
import json
from yaml import safe_load
from datetime import datetime
from typing import List
import pandas as pd
from geoenvo.environment import Environment
from geoenvo.geometry import Geometry


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
        self.data = {
            "type": "Environment",
            "dataSource": {"identifier": None, "resolver": None},
            "dateCreated": None,
            "properties": {},
            "envoTerms": [],
        }

    def set_identifier(self, identifier):
        self.data["dataSource"]["identifier"] = identifier

    def set_resolver(self, resolver):
        self.data["dataSource"]["resolver"] = resolver

    def set_date_created(self):
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data["dateCreated"] = date_created

    def set_properties(self, properties):
        self.data["properties"] = properties


class Data:
    def __init__(self, data: dict = dict()):
        self._data = data
        self.attributes = {
            "type": "Feature",
            "identifier": None,
            "geometry": None,
            "properties": {"environment": []},
        }

    def write(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            file.write(json.dumps(self._data))

    def read(self, file_path: str):
        with open(file_path, "r") as file:
            self._data = json.loads(file.read())
        return self

    def set_envo_terms(self):
        # Iterate over list of environments in data
        for environment in self._data["properties"]["environment"]:

            # Load SSSOM of environment for term mapping
            resolver = environment["dataSource"]["resolver"]
            sssom_file = importlib.resources.files("geoenvo.data.sssom").joinpath(
                f"{resolver}-envo.sssom.tsv"
            )
            sssom_meta_file = importlib.resources.files(
                "geoenvo.data.sssom"
            ).joinpath(f"{resolver}-envo.sssom.yml")
            with open(sssom_file, mode="r", encoding="utf-8") as f:
                sssom = pd.read_csv(f, sep="\t")
            with open(sssom_meta_file, mode="r", encoding="utf-8") as f:
                sssom_meta = safe_load(f)

            # Map each property to an ENVO term, if possible
            envo_terms = []
            for key, value in environment["properties"].items():
                try:
                    label = sssom.loc[
                        sssom["subject_label"].str.lower() == value.lower(),
                        "object_label",
                    ].values[0]
                    curie = sssom.loc[
                        sssom["subject_label"].str.lower() == value.lower(), "object_id"
                    ].values[0]
                    curie_prefix = curie.split(":")[0]
                    uri = sssom_meta["curie_map"][curie_prefix] + curie.split(":")[1]
                except IndexError:
                    envo_label = None
                    envo_uri = None

                # Don't add empty values. Empty implies no mapping was found
                if pd.notna(label) and uri is not None:
                    envo_terms.append({"label": label, "uri": uri})

            # Add list of ENVO terms back to the environment object
            environment["envoTerms"] = envo_terms

        return self


def compile_response(
    geometry: Geometry, environment: List[Environment], identifier: str = None
) -> Data:

    # Move data from Environment objects and into a list  # TODO: clean up
    environments = []
    for env in environment:
        environments.append(env._data)

    result = {  # FIXME: just a rudimentary implementation
        "type": "Feature",
        "identifier": identifier,
        "geometry": geometry._data,
        "properties": {"environment": environments},
    }
    return Data(result)


def get_attributes(data, attributes):
    """Recursively get attributes of a response from an identify or query
    opperation.

    Parameters
    ----------
    data : dict
        A dictionary of the JSON response from the identify operation.
    attributes : list
        A list of attributes to extract from the JSON response. These are
        defined in the map service's layer's definition.

    Returns
    -------
    res : dict
        A dictionary of the requested attributes and their values.

    """
    # TODO Get attributes/features by source? This would simplify the
    #  methods calls, unless this functionality is needed elsewhere (e.g.
    #  getting other names from response dictionaries).
    res = {}
    for a in attributes:
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
