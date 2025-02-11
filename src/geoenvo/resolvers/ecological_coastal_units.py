"""The resolvers module"""

from datetime import datetime
from json import dumps
import requests
from geoenvo.resolver import Resolver
from geoenvo.geometry import Geometry
from geoenvo.environment import Environment
from geoenvo.utilities import user_agent
from geoenvo.utilities import EnvironmentDataModel, get_attributes


class EcologicalCoastalUnits(Resolver):
    def __init__(self):
        super().__init__()
        self._geometry = None
        self._data = None
        self._env_attributes = {
            "Slope": None,
            "Sinuosity": None,
            "Erodibility": None,
            "Temperature and Moisture Regime": None,
            "River Discharge": None,
            "Wave Height": None,
            "Tidal Range": None,
            "Marine Physical Environment": None,
            "Turbidity": None,
            "Chlorophyll": None,
            "CSU_Descriptor": None,
        }
        self._buffer = None

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
    def buffer(self, buffer: float):
        return self._buffer

    @buffer.setter
    def buffer(self, buffer: float):
        self._buffer = buffer

    def resolve(self, geometry: Geometry):

        # Enable the buffer size sampling option for points, which the data
        # source would otherwise resolve to None, because points don't
        # overlap the vector data of the source.
        if geometry.geometry_type() == "Point" and self.buffer is not None:
            geometry.data = geometry.point_to_polygon(buffer=self.buffer)

        self.data = self._request(geometry)
        return self.convert_data()

    @staticmethod
    def _request(geometry: Geometry):
        base = (
            "https://rmgsc.cr.usgs.gov/arcgis/rest/services/"
            + "gceVector"
            + "/MapServer/"
            + "0"
            + "/query"
        )
        payload = {
            "f": "geojson",
            "geometry": dumps(geometry.to_esri()["geometry"]),
            "geometryType": geometry.to_esri()["geometryType"],
            "where": "1=1",
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": "*",
            "returnTrueCurves": "false",
            "returnIdsOnly": "false",
            "returnCountOnly": "false",
            "returnZ": "false",
            "returnM": "false",
            # "returnDistinctValues": "true",
            "returnExtentOnly": "false",
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
        unique_ecu_ecosystems = self.unique_environment()
        for unique_ecu_ecosystem in unique_ecu_ecosystems:
            ecosystem = EnvironmentDataModel()
            ecosystem.set_identifier("https://doi.org/10.5066/P9HWHSPU")
            ecosystem.set_resolver(self.__class__.__name__)
            ecosystem.set_date_created()
            attributes = self.set_attributes(  # TODO: Move this processing to self.unique_environment() to match WTE implmementation
                unique_ecosystem_attributes=unique_ecu_ecosystem
            )
            ecosystem.set_properties(attributes)
            result.append(Environment(data=ecosystem.data))
        return result

    def unique_environment(self):
        if not self.has_ecosystem():
            return list()
        attribute = "CSU_Descriptor"
        descriptors = get_attributes(self._data, [attribute])[attribute]
        descriptors = set(descriptors)
        descriptors = list(descriptors)
        return descriptors

    def has_ecosystem(self):
        # FIXME: This produces an error when running the geographic
        #  coverage in the file knb-lter-ntl.420.2.
        res = len(self._data["features"])
        if res == 0:
            return False
        if res > 0:
            return True

    def set_attributes(self, unique_ecosystem_attributes):
        if len(unique_ecosystem_attributes) == 0:
            return None
        # There is only one attribute for ECU, CSU_Descriptor, which is
        # composed of 10 atomic attributes.
        descriptors = unique_ecosystem_attributes
        # Atomize: Split on commas and remove whitespace
        descriptors = descriptors.split(",")
        descriptors = [g.strip() for g in descriptors]
        atomic_attribute_labels = self._env_attributes.keys()
        # Zip descriptors and atomic attribute labels
        ecosystems = [dict(zip(atomic_attribute_labels, descriptors))]
        # Iterate over atomic attributes and set labels and annotations
        ecosystem = ecosystems[0]
        # attributes = {}
        # self._env_attributes
        env_attributes = self._env_attributes
        for attribute in ecosystem.keys():
            label = ecosystem.get(attribute)
            env_attributes[attribute] = label
        # Add composite CSU_Description class and annotation.
        # Get ecosystems values and join with commas
        # TODO Fix issue where an attribute from the initialized list returned
        #  by  Attributes() was missing for some reason and thus an annotation
        #  couldn't  be found for it. If arbitrary joining of empties to the
        #  annotation string is done, then the annotation may be wrong. Best to
        #  just leave it out.
        CSU_Descriptor = [f for f in env_attributes.values()]
        # Knock of the last one, which is CSU_Descriptor
        CSU_Descriptor = CSU_Descriptor[:-1]
        CSU_Descriptor = ", ".join(CSU_Descriptor)
        # Knock of the last one, which is CSU_Descriptor
        env_attributes["CSU_Descriptor"] = CSU_Descriptor

        # Convert property keys into a more readable format
        new_env_attributes = {
            "slope": env_attributes["Slope"],
            "sinuosity": env_attributes["Sinuosity"],
            "erodibility": env_attributes["Erodibility"],
            "temperatureAndMoistureRegime": env_attributes[
                "Temperature and Moisture Regime"
            ],
            "riverDischarge": env_attributes["River Discharge"],
            "waveHeight": env_attributes["Wave Height"],
            "tidalRange": env_attributes["Tidal Range"],
            "marinePhysicalEnvironment": env_attributes["Marine Physical Environment"],
            "turbidity": env_attributes["Turbidity"],
            "chlorophyll": env_attributes["Chlorophyll"],
            "ecosystem": env_attributes["CSU_Descriptor"],
        }
        return new_env_attributes

    @staticmethod
    def get_annotation(
        label: str,
    ):  # TODO deprecate this once moved to Environment class method
        return "Placeholder"  # TODO - add ECU sssom and parse
