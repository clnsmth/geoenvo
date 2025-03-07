"""
*world_terrestrial_ecosystems.py*
"""

from json import dumps, loads
from pathlib import Path
from typing import List
from importlib.resources import files

import pandas as pd
import requests
from geoenvo.data_sources.data_source import DataSource
from geoenvo.geometry import Geometry
from geoenvo.environment import Environment
from geoenvo.utilities import user_agent, get_properties
from geoenvo.utilities import _json_extract, EnvironmentDataModel


class WorldTerrestrialEcosystems(DataSource):
    """
    A concrete implementation of ``DataSource`` that retrieves terrestrial
    ecosystem classifications from the World Terrestrial Ecosystems dataset
    (Sayre 2022).

    **Note**
        - This data source only accepts ``Point`` geometries directly.
          ``Polygon`` geometries are supported indirectly via the ``grid_size``
          property, which enables subsampling of the polygon into
          representative points. Each point is resolved individually, and the
          results are aggregated into the final response.

    **Further Information**
        - **Spatial Resolution**: Global coverage with a resolution of
          *250 meters*.
        - **Coverage**: Terrestrial ecosystems worldwide, classified by *land
          cover, landform, and climate*.
        - **Explore the Dataset**:
          `https://www.arcgis.com/home/item.html?id=926a206393ec40a590d8caf29ae9a93e <https://www.arcgis.com/home/item.html?id=926a206393ec40a590d8caf29ae9a93e>`_.

    **Citation**
        Sayre, R., 2022, *World Terrestrial Ecosystems (WTE) 2020*: U.S. Geological Survey data release,
        `https://doi.org/10.5066/P9DO61LP <https://doi.org/10.5066/P9DO61LP>`_.
    """

    def __init__(self):
        """
        Initializes the WorldTerrestrialEcosystems data source with default
        properties.
        """
        super().__init__()
        self._geometry = None
        self._data = None
        self._properties = {
            "Temperatur": None,
            "Moisture": None,
            "Landcover": None,
            "Landforms": None,
            "Climate_Re": None,
            "ClassName": None,
        }

        self._grid_size = None

    @property
    def geometry(self) -> dict:
        return self._geometry

    @geometry.setter
    def geometry(self, geometry: dict):
        self._geometry = geometry

    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data

    @property
    def properties(self) -> dict:
        return self._properties

    @properties.setter
    def properties(self, properties: dict):
        self._properties = properties

    @property
    def grid_size(self) -> float:
        """
        Retrieves the grid size used for spatial resolution. The size of the
        grid cells are in the same units as the geometry coordinates.

        Note, if a ``Polygon`` geometry is provided, this property determines
        the spacing of the representative points used for subsampling. Each
        point is resolved individually, and the results are combined in the
        final response.

        :return: The grid size as a float.
        """
        return self._grid_size

    @grid_size.setter
    def grid_size(self, grid_size: float):
        """
        Sets the grid size used for spatial resolution.

        :param grid_size: The grid size as a float.
        """
        self._grid_size = grid_size

    def get_environment(self, geometry: Geometry) -> List[Environment]:
        """
        Resolves a given geometry to environmental descriptions using the
        World Terrestrial Ecosystems dataset.

        :param geometry: The geographic location to resolve.
        :return: A list of ``Environment`` objects containing environmental
            classifications.
        """
        # Enable grid-based sampling for polygons. Without this, the data source
        # would default to using the centroid of the polygon instead.
        geometries = []
        if geometry.geometry_type() == "Polygon" and self.grid_size is not None:
            points = geometry.polygon_to_points(grid_size=self.grid_size)
            for point in points:
                geometries.append(Geometry(point))
        else:
            geometries.append(geometry)

        # Resolve each geometry, and in the case of multiple points, compile
        # a single response object emulating the API response format. This is
        # to maintain compatibility with the downstream code.
        results = []
        for geometry in geometries:
            response = self._request(geometry)
            results.extend(response["properties"].get("Values", []))
        # self.data = {"results": results}  # TODO remove me?
        self.data = {"properties": {"Values": results}}

        return self.convert_data()

    @staticmethod
    def _request(geometry: Geometry) -> dict:
        """
        Sends a request to the World Terrestrial Ecosystems data source and
        retrieves raw response data.

        :param geometry: The geographic location to query.
        :return: A dictionary containing raw response data from the data
            source.
        """
        base = "https://landscape12.arcgis.com/arcgis/rest/services/World_Terrestrial_Ecosystems/ImageServer/identify"
        payload = {
            "geometry": dumps(geometry.to_esri()["geometry"]),
            "geometryType": geometry.to_esri()["geometryType"],
            "returnGeometry": "false",
            "f": "json"
        }
        try:
            response = requests.get(
                base, params=payload, timeout=10, headers=user_agent()
            )
            return response.json()
        except Exception as e:
            return {}

    def convert_data(self) -> List[Environment]:
        result = []
        unique_wte_environments = self.unique_environment()
        for unique_wte_environment in unique_wte_environments:
            environment = EnvironmentDataModel()
            environment.set_identifier("https://doi.org/10.5066/P9DO61LP")
            environment.set_data_source(self.__class__.__name__)
            environment.set_date_created()
            environment.set_properties(unique_wte_environment)
            result.append(Environment(data=environment.data))
        return result

    def unique_environment(self) -> List[dict]:
        # Parse the properties of the environment(s) in the data to a form
        # that can be compared for uniqueness.
        if not self.has_environment():
            return list()
        descriptors = []
        properties = self.properties.keys()
        self.data = map_codes(self.data)
        results = self.data.get("results")
        for result in results:
            res = dict()
            for property in properties:
                res[property] = result.get(property)
            res = dumps(res)
            descriptors.append(res)
        descriptors = set(descriptors)
        descriptors = [loads(d) for d in descriptors]

        # Convert properties into a more readable format
        new_descriptors = []
        for descriptor in descriptors:
            new_descriptor = {
                "temperature": descriptor["Temperatur"],
                "moisture": descriptor["Moisture"],
                "landCover": descriptor["Landcover"],
                "landForm": descriptor["Landforms"],
                "climate": descriptor["Climate_Re"],
                "ecosystem": descriptor["ClassName"],
            }
            new_descriptors.append(new_descriptor)
        return new_descriptors

    def has_environment(self, data=None) -> bool:
        """
        The data parameter enables the method to be used with a different
        dataset than the one stored in the data source instance.
        """
        if data is None:
            data = self.data

        # # If codes are mapped  # TODO needed?
        # if data.get("results"):
        #     if len(data["results"][0]) == 0:
        #         return False
        #     return True

        # If codes are unmapped
        if data.get("properties"):
            if data["properties"].get("Values"):
                if data["properties"]["Values"][0] == "NoData":
                    return False
                return True


def map_codes(json: dict) -> dict:

    # Load the mapping file as a DataFrame for easy lookup
    with open(
            files("src.geoenvo.data.data_source_attributes").joinpath(
                "WTE_raster_attribute_table.json"), "r") as file:
        attribute_table = loads(file.read())
    features = attribute_table.get("features")
    attributes = [feature["attributes"] for feature in features]
    df = pd.DataFrame(attributes)

    mapped_results = []
    for code in json["properties"].get("Values"):
        # Get the row from the data frame where the attribute matches the
        # value in the Value column. Also pair down the columns to only the
        # ones we want to return.
        if code == "NoData":
            continue
        row = df[df["Value"] == int(code)]
        row = row[["Landforms", "Landcover", "Climate_Re", "ClassName", "Moisture", "Temperatur"]]
        mapped_results.append(row.to_dict("records")[0])
    return {"results": mapped_results}


def write_raster_attribute_table(output_directory: Path = files("src.geoenvo.data.data_source_attributes")) -> None:
    """
    Writes the raster attribute table for the World Terrestrial Ecosystems to
    local file for reference. The table enables the conversion of environmental
    classification codes to human-readable descriptions.
    """
    base = "https://landscape12.arcgis.com/arcgis/rest/services/World_Terrestrial_Ecosystems/ImageServer/rasterAttributeTable"
    payload = {
        "f": "pjson"
    }
    try:
        response = requests.get(
            base, params=payload, timeout=10, headers=user_agent()
        )
    except Exception as e:
        return {}

    file_path = output_directory.joinpath("WTE_raster_attribute_table.json")
    with open(file_path, "w") as file:
        file.write(dumps(response.json(), indent=4))


if __name__ == "__main__":
    output_directory = files("src.geoenvo.data.data_source_attributes")
    write_raster_attribute_table(output_directory)
