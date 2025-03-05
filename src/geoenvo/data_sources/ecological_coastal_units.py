"""
*ecological_coastal_units.py*
"""

from json import dumps
from typing import List
import requests
from geoenvo.data_sources.data_source import DataSource
from geoenvo.geometry import Geometry
from geoenvo.environment import Environment
from geoenvo.utilities import user_agent
from geoenvo.utilities import EnvironmentDataModel, get_properties


class EcologicalCoastalUnits(DataSource):
    """
    A concrete implementation of ``DataSource`` that retrieves coastal
    environmental classifications from the Ecological Coastal Units dataset
    (Sayre 2023).

    **Note**
        - Note, this data source does not accept ``Point`` geometries directly.
          Because coastal units are represented as vector polygons, input
          geometries must overlap with them for successful resolution. However,
          ``Point`` geometries can be processed by setting the ``buffer``
          property, which converts them into circular polygons of a given
          radius (in kilometers). These polygons are then resolved against the
          dataset, and all overlapping coastal units are returned in the
          response.

    **Further Information**
        - **Spatial Resolution**: Global coverage with a resolution of
          *1 km (or shorter)*.
        - **Coverage**: Costal ecosystems worldwide, classified by *sinuosity,
          erodibility, temperature and moisture regime, river discharge,
          wave height, tidal range, marine physical environment, turbidity,
          and chlorophyll*.
        - **Explore the Dataset**:
          `https://www.arcgis.com/home/item.html?id=54df078334954c5ea6d5e1c34eda2c87 <https://www.arcgis.com/home/item.html?id=54df078334954c5ea6d5e1c34eda2c87>`_.

    **Citation**
        Sayre, R., 2023, Global Ecological Classification of Coastal Segment
        Units: U.S. Geological Survey data release, `https://doi.org/10.5066/P9HWHSPU <https://doi.org/10.5066/P9HWHSPU>`_.
    """

    def __init__(self):
        """
        Initializes the EcologicalCoastalUnits data source with default
        properties.
        """
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
    def buffer(self) -> float:
        """
        Retrieves the buffer distance used for spatial resolution.

        Since this data source does not accept ``Point`` geometries directly,
        setting the ``buffer`` parameter allows points to be expanded into
        circular polygons before resolution. All overlapping coastal units
        within the buffered area will be included in the response.

        :return: The buffer distance as a float. Units are in **kilometers**.
        """
        return self._buffer

    @buffer.setter
    def buffer(self, buffer: float):
        """
        Sets the buffer distance used for spatial resolution.

        :param buffer: The buffer distance as a float.
        """
        self._buffer = buffer

    def get_environment(self, geometry: Geometry) -> List[Environment]:
        """
        Resolves a given geometry to environmental descriptions using the
        Ecological Coastal Units dataset.

        :param geometry: The geographic location to resolve.
        :return: A list of ``Environment`` objects containing environmental
            classifications.
        """
        # Enable buffer-based sampling for points. Without this, the data
        # source would return None because environments are represented as
        # line vectors, meaning point locations would not overlap with any
        # features.
        if geometry.geometry_type() == "Point" and self.buffer is not None:
            geometry.data = geometry.point_to_polygon(buffer=self.buffer)

        self.data = self._request(geometry)
        return self.convert_data()

    @staticmethod
    def _request(geometry: Geometry) -> dict:
        """
        Sends a request to the Ecological Coastal Units data source and
        retrieves raw response data.

        :param geometry: The geographic location to query.
        :return: A dictionary containing raw response data from the data
            source.
        """
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
            "returnExtentOnly": "false",
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

    def unique_environment(self) -> List[dict]:
        if not self.has_environment():
            return list()
        property = "CSU_Descriptor"
        descriptors = get_properties(self._data, [property])[property]
        descriptors = set(descriptors)
        descriptors = list(descriptors)
        return descriptors

    def has_environment(self) -> bool:
        res = len(self._data["features"])
        if res == 0:
            return False
        if res > 0:
            return True

    def set_properties(self, unique_environment_properties) -> dict:
        """
        Sets the properties for the data source based on unique environmental
        descriptions.

        :param unique_environment_properties: A dictionary containing
            environmental classification attributes.
        :return: The updated properties dictionary.
        """
        if len(unique_environment_properties) == 0:
            return None

        # There is only one property returned by this data source
        # (CSU_Descriptor), which is composed of 10 atomic properties. Split
        # the CSU_Descriptor into atomic properties and then zip the
        # descriptors and atomic property labels to create a dictionary of
        # environment properties.
        descriptors = unique_environment_properties
        descriptors = descriptors.split(",")
        descriptors = [g.strip() for g in descriptors]
        atomic_property_labels = self._properties.keys()
        environments = [dict(zip(atomic_property_labels, descriptors))]

        # Iterate over atomic properties and set labels
        environment = environments[0]
        properties = self._properties
        for property in environment.keys():
            label = environment.get(property)
            properties[property] = label

        # Compose a readable CSU_Descriptor class by joining atomic properties
        # into a single string.
        CSU_Descriptor = [f for f in properties.values()]
        CSU_Descriptor = CSU_Descriptor[:-1]  # last one is the CSU_Description
        CSU_Descriptor = ", ".join(CSU_Descriptor)
        properties["CSU_Descriptor"] = CSU_Descriptor

        # Convert property labels into a more readable format
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
