"""The data_source module"""

from datetime import datetime
from json import dumps
import requests
from geoenvo.data_sources.data_source import DataSource
from geoenvo.geometry import Geometry
from geoenvo.environment import Environment
from geoenvo.utilities import user_agent
from geoenvo.utilities import EnvironmentDataModel, get_properties


class EcologicalCoastalUnits(DataSource):
    def __init__(self):
        super().__init__()
        self._geometry = None
        self._data = None
        self._properties = {
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
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, properties: dict):
        self._properties = properties

    @property
    def buffer(self):
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
        unique_ecu_environments = self.unique_environment()
        for unique_ecu_environment in unique_ecu_environments:
            environment = EnvironmentDataModel()
            environment.set_identifier("https://doi.org/10.5066/P9HWHSPU")
            environment.set_data_source(self.__class__.__name__)
            environment.set_date_created()
            properties = self.set_properties(  # TODO: Move this processing to self.unique_environment() to match WTE implmementation
                unique_environment_properties=unique_ecu_environment
            )
            environment.set_properties(properties)
            result.append(Environment(data=environment.data))
        return result

    def unique_environment(self):
        if not self.has_environment():
            return list()
        property = "CSU_Descriptor"
        descriptors = get_properties(self._data, [property])[property]
        descriptors = set(descriptors)
        descriptors = list(descriptors)
        return descriptors

    def has_environment(self):
        # FIXME: This produces an error when running the geographic
        #  coverage in the file knb-lter-ntl.420.2.
        res = len(self._data["features"])
        if res == 0:
            return False
        if res > 0:
            return True

    def set_properties(self, unique_environment_properties):
        if len(unique_environment_properties) == 0:
            return None
        # There is only one property for ECU, CSU_Descriptor, which is
        # composed of 10 atomic properties.
        descriptors = unique_environment_properties
        # Atomize: Split on commas and remove whitespace
        descriptors = descriptors.split(",")
        descriptors = [g.strip() for g in descriptors]
        atomic_property_labels = self._properties.keys()
        # Zip descriptors and atomic property labels
        environments = [dict(zip(atomic_property_labels, descriptors))]
        # Iterate over atomic properties and set labels and annotations
        environment = environments[0]
        # properties = {}
        # self._properties
        properties = self._properties
        for property in environment.keys():
            label = environment.get(property)
            properties[property] = label
        # Add composite CSU_Description class
        # Get environments values and join with commas
        # TODO Fix issue where an property from the initialized list returned
        #  by  Attributes() was missing for some reason and thus an annotation
        #  couldn't  be found for it. If arbitrary joining of empties to the
        #  annotation string is done, then the annotation may be wrong. Best to
        #  just leave it out.
        CSU_Descriptor = [f for f in properties.values()]
        # Knock of the last one, which is CSU_Descriptor
        CSU_Descriptor = CSU_Descriptor[:-1]
        CSU_Descriptor = ", ".join(CSU_Descriptor)
        # Knock of the last one, which is CSU_Descriptor
        properties["CSU_Descriptor"] = CSU_Descriptor

        # Convert properties into a more readable format
        new_properties = {
            "slope": properties["Slope"],
            "sinuosity": properties["Sinuosity"],
            "erodibility": properties["Erodibility"],
            "temperatureAndMoistureRegime": properties[
                "Temperature and Moisture Regime"
            ],
            "riverDischarge": properties["River Discharge"],
            "waveHeight": properties["Wave Height"],
            "tidalRange": properties["Tidal Range"],
            "marinePhysicalEnvironment": properties["Marine Physical Environment"],
            "turbidity": properties["Turbidity"],
            "chlorophyll": properties["Chlorophyll"],
            "ecosystem": properties["CSU_Descriptor"],
        }
        return new_properties
