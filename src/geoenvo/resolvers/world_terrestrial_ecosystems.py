"""The resolvers module"""

import warnings
from json import dumps, loads
import requests
from geoenvo.resolver import Resolver
from geoenvo.geometry import Geometry
from geoenvo.environment import Environment
from geoenvo.utilities import user_agent
from geoenvo.utilities import _json_extract, EnvironmentDataModel


class WorldTerrestrialEcosystems(Resolver):
    def __init__(self):
        super().__init__()
        self._geometry = None
        self._data = None
        self._env_attributes = {  # TODO is this used anywhere?
            "Raster.Temp_Class": None,
            "Raster.Moisture_C": None,
            "Raster.LC_ClassNa": None,
            "Raster.LF_ClassNa": None,
            "Raster.Temp_Moist": None,
            "Raster.ClassName": None,
        }
        self._grid_size = None

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry: dict):
        self._geometry = geometry

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: dict):
        self._data = data

    @property
    def env_attributes(self):
        return self._env_attributes

    @env_attributes.setter
    def env_attributes(self, env_attributes: dict):
        self._env_attributes = env_attributes

    @property
    def grid_size(self):
        return self._grid_size

    @grid_size.setter
    def grid_size(self, grid_size: float):
        self._grid_size = grid_size

    def resolve(self, geometry: Geometry):

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
    def _request(geometry: Geometry):
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

    def convert_data(self):
        result = []
        unique_wte_environments = self.unique_environment()
        for unique_wte_environment in unique_wte_environments:
            environment = EnvironmentDataModel()
            environment.set_identifier("https://doi.org/10.5066/P9DO61LP")
            environment.set_resolver(self.__class__.__name__)
            environment.set_date_created()
            environment.set_properties(unique_wte_environment)
            result.append(Environment(data=environment.data))
        return result

    def unique_environment(self):
        # Parse the attributes of the environment(s) in the data to a form
        # that can be compared for uniqueness.
        if not self.has_environment():
            return list()
        descriptors = []
        attributes = self.env_attributes.keys()
        results = self.data.get("results")
        for result in results:
            if not self.has_environment(result):
                continue
            res = dict()
            for attribute in attributes:
                res[attribute] = result["attributes"].get(attribute)
            res = dumps(res)
            descriptors.append(res)
        descriptors = set(descriptors)
        descriptors = [loads(d) for d in descriptors]

        # Convert property keys into a more readable format
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

    def has_environment(self, data=None):
        """
        The data parameter enables the method to be used with a different
        dataset than the one stored in the resolver instance.
        """
        if data is None:
            data = self.data
        res = _json_extract(data, "UniqueValue.Pixel Value")
        if len(res) == 0:
            return False
        if len(res) > 0 and res[0] == "NoData":
            return False
        return True
