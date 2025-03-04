"""
world_terrestrial_ecosystems.py
================================

This module defines the ``WorldTerrestrialEcosystems`` class, a concrete
implementation of the ``DataSource`` abstract base class (ABC). This class
interacts with the World Terrestrial Ecosystems dataset, retrieving
environmental information based on geographic locations.

Key functionalities of this module include:

- Querying and resolving spatial geometries to terrestrial ecosystem
  classifications.
- Structuring and converting data into a standardized format.
- Extracting unique environmental descriptions from the dataset.
"""

import warnings
from json import dumps, loads
from typing import List

import requests
from geoenvo.data_sources.data_source import DataSource
from geoenvo.geometry import Geometry
from geoenvo.environment import Environment
from geoenvo.utilities import user_agent
from geoenvo.utilities import _json_extract, EnvironmentDataModel


class WorldTerrestrialEcosystems(DataSource):
    """
    A concrete implementation of ``DataSource`` that retrieves terrestrial
    ecosystem classifications from the World Terrestrial Ecosystems dataset
    (Sayre 2022).

    Note, this data source only accepts ``Point`` geometries directly.
    ``Polygon`` geometries are supported indirectly via the ``grid_size``
    property, which enables subsampling of the polygon into representative
    points. Each point is resolved individually, and the results are
    aggregated into the final response.

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
        self._properties = {  # TODO is this used anywhere?
            "Raster.Temp_Class": None,
            "Raster.Moisture_C": None,
            "Raster.LC_ClassNa": None,
            "Raster.LF_ClassNa": None,
            "Raster.Temp_Moist": None,
            "Raster.ClassName": None,
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

    def resolve(self, geometry: Geometry) -> List[Environment]:
        # Enable the grid size sampling option for polygons, which the data
        # source would otherwise convert to a centroid point.
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
            results.extend(response.get("results", []))
        self.data = {"results": results}

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
        base = (
            "https://rmgsc.cr.usgs.gov/arcgis/rest/services/"
            + "wte"
            + "/MapServer/identify"
        )
        payload = {
            "f": "json",
            "geometry": dumps(geometry.to_esri()["geometry"]),
            "geometryType": geometry.to_esri()["geometryType"],
            "tolerance": 2,
            "mapExtent": "-2.865, 47.628, 5.321, 50.017",
            "imageDisplay": "600,550,96",
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
        results = self.data.get("results")
        for result in results:
            if not self.has_environment(result):
                continue
            res = dict()
            for property in properties:
                res[property] = result["attributes"].get(property)
            res = dumps(res)
            descriptors.append(res)
        descriptors = set(descriptors)
        descriptors = [loads(d) for d in descriptors]

        # Convert properties into a more readable format
        new_descriptors = []
        for descriptor in descriptors:
            new_descriptor = {
                "temperature": descriptor["Raster.Temp_Class"],
                "moisture": descriptor["Raster.Moisture_C"],
                "landCover": descriptor["Raster.LC_ClassNa"],
                "landForm": descriptor["Raster.LF_ClassNa"],
                "climate": descriptor["Raster.Temp_Moist"],
                "ecosystem": descriptor["Raster.ClassName"],
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
        res = _json_extract(data, "UniqueValue.Pixel Value")
        if len(res) == 0:
            return False
        if len(res) > 0 and res[0] == "NoData":
            return False
        return True
