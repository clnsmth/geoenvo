"""
*ecological_marine_units.py*
"""

from json import dumps, loads
from typing import List

import pandas as pd
import requests
from geoenvo.data_sources.data_source import DataSource
from geoenvo.geometry import Geometry
from geoenvo.environment import Environment
from geoenvo.utilities import user_agent
from geoenvo.utilities import EnvironmentDataModel


class EcologicalMarineUnits(DataSource):
    """
    A concrete implementation of ``DataSource`` that retrieves marine
    environmental classifications from the Ecological Marine Units dataset
    (Sayre 2023).


    **Note**
        - This data source supports the resolution of geometries with ``z``
          values (depth). To retrieve environmental data at different depths,
          include the ``z`` component in the input geometry. No additional
          property is required.
        - If no ``z`` value is specified in the geometry, all vertically
          stacked environments will be returned. If a ``z`` value is included,
          only the intersecting environment layers at that depth will be
          returned.

    **Further Information**
        - **Spatial Resolution**: Global coverage with a resolution of
          *1/4 degree*.
        - **Coverage**: Marine ecosystems worldwide, classified by *ocean name,
          depth, temperature, salinity, dissolved oxygen, nitrate, phosphate,
          and silicate*.
        - **Explore the Dataset**:
          `https://esri.maps.arcgis.com/home/item.html?id=58526e3af88b46a3a1d1eb1738230ee3 <https://esri.maps.arcgis.com/home/item.html?id=58526e3af88b46a3a1d1eb1738230ee3>`_.

    **Citation**
        Sayre, R., 2023, Ecological Marine Units (EMUs): U.S. Geological
        Survey data release, `https://doi.org/10.5066/P9Q6ZSGN <https://doi.org/10.5066/P9Q6ZSGN>`_.
    """

    def __init__(self):
        """
        Initializes the EcologicalMarineUnits data source with default
        properties.
        """
        super().__init__()
        self._geometry = None
        self._data = None
        self._properties = {
            "OceanName": None,
            "Depth": None,
            "Temperature": None,
            "Salinity": None,
            "Dissolved Oxygen": None,
            "Nitrate": None,
            "Phosphate": None,
            "Silicate": None,
            "EMU_Descriptor": None,
        }

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

    def get_environment(self, geometry: Geometry) -> List[Environment]:
        """
        Resolves a given geometry to environmental descriptions using the
        Ecological Marine Units dataset.

        :param geometry: The geographic location to resolve.
        :return: A list of ``Environment`` objects containing environmental
            classifications.
        """
        self.geometry = geometry.data  # access z values to filter on depth
        self.data = self._request(geometry)
        return self.convert_data()

    @staticmethod
    def _request(geometry: Geometry) -> dict:
        """
        Sends a request to the Ecological Marine Units data source and
        retrieves raw response data.

        :param geometry: The geographic location to query.
        :return: A dictionary containing raw response data from the data
            source.
        """
        base = (
            "https://services.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/"
            + "EMU_2018"
            + "/FeatureServer/"
            + "0"
            + "/query"
        )
        payload = {
            "f": "json",
            "geometry": dumps(geometry.to_esri()["geometry"]),
            "geometryType": geometry.to_esri()["geometryType"],
            "where": "1=1",
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": "UnitTop,UnitBottom,OceanName,Name_2018",
            "distance": "10",
            "units": "esriSRUnit_NauticalMile",
            "multipatchOption": "xyFootprint",
            "outSR": '{"wkid":4326}',
            "returnIdsOnly": "false",
            "returnZ": "false",
            "returnM": "false",
            "returnExceededLimitFeatures": "true",
            "sqlFormat": "none",
            "orderByFields": "UnitTop desc",
            "returnDistinctValues": "false",
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
        unique_emu_environments = self.unique_environment()
        for unique_emu_environment in unique_emu_environments:
            environment = EnvironmentDataModel()
            environment.set_identifier("https://doi.org/10.5066/P9Q6ZSGN")
            environment.set_data_source(self.__class__.__name__)
            environment.set_date_created()
            properties = self.set_properties(
                unique_environment_properties=unique_emu_environment
            )
            environment.set_properties(properties)
            result.append(Environment(data=environment.data))
        return result

    def unique_environment(self) -> List[dict]:
        if not self.has_environment():
            return list()
        data = self.convert_codes_to_values()
        descriptors = self.get_environments_for_geometry_z_values(data=data)
        return descriptors

    def has_environment(self) -> bool:
        res = len(self.data["features"])
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

        # There are two properties returned by this data source (OceanName and
        # Name_2018), the latter of which is composed of 7 atomic properties.
        # Split Name_2018 into atomic properties and then zip the descriptors
        # and atomic property labels to create a dictionary of environment
        # properties.
        properties = loads(unique_environment_properties)["attributes"]
        ocean_name = properties.get("OceanName")
        descriptors = properties.get("Name_2018")
        descriptors = descriptors.split(",")
        descriptors = [g.strip() for g in descriptors]

        # Add ocean name to front of descriptors list in preparation for the
        # zipping operation below
        descriptors = [ocean_name] + descriptors
        properties = self.properties
        atomic_property_labels = properties.keys()
        environments = [dict(zip(atomic_property_labels, descriptors))]

        # Iterate over atomic properties and set labels
        environment = environments[0]
        for property in environment.keys():
            label = environment.get(property)
            properties[property] = label

        # Compose a readable EMU_Description classification by joining atomic
        # properties into a single string.
        EMU_Descriptor = [f for f in properties.values()]
        EMU_Descriptor = EMU_Descriptor[:-1]  # last one is the EMU_Descriptor
        # Handle edge case where some of the properties are None. This is an
        # issue with the data source.
        if None in EMU_Descriptor:
            EMU_Descriptor = ["n/a" if f is None else f for f in EMU_Descriptor]
        EMU_Descriptor = ", ".join(EMU_Descriptor)
        properties["EMU_Descriptor"] = EMU_Descriptor

        # Convert properties into a more readable format
        new_properties = {
            "oceanName": properties["OceanName"],
            "depth": properties["Depth"],
            "temperature": properties["Temperature"],
            "salinity": properties["Salinity"],
            "dissolvedOxygen": properties["Dissolved Oxygen"],
            "nitrate": properties["Nitrate"],
            "phosphate": properties["Phosphate"],
            "silicate": properties["Silicate"],
            "ecosystem": properties["EMU_Descriptor"],
        }
        return new_properties

    def convert_codes_to_values(self) -> dict:
        """
        Converts coded classification values (e.g., ``OceanName`` and other
        properties) into descriptive string values. This transformation ensures
        consistency between response objects across different datasets.

        :return: A dictionary with converted classification values.
        """
        data = self.data
        field_names = [field["name"] for field in data["fields"]]
        i = field_names.index("OceanName")
        ocean_name_map = pd.DataFrame(
            data.get("fields")[i].get("domain").get("codedValues")
        )

        # Create the code-value map for Name_2018
        i = field_names.index("Name_2018")
        name_2018_map = pd.DataFrame(
            data.get("fields")[i].get("domain").get("codedValues")
        )

        # Iterate over the features array replacing OceanName and
        # Name_2018 codes with corresponding values in the maps
        for i in range(len(data.get("features"))):
            # OceanName
            code = data.get("features")[i]["attributes"]["OceanName"]
            if code is None:
                value = "Not an ocean"
            else:
                value = ocean_name_map.loc[ocean_name_map["code"] == code, "name"].iloc[
                    0
                ]
            data.get("features")[i]["attributes"]["OceanName"] = value
            # Name_2018
            code = data.get("features")[i]["attributes"]["Name_2018"]

            # Not all locations have Name_2018 values (not sure why this is
            # the case).
            try:
                value = name_2018_map.loc[name_2018_map["code"] == code, "name"].iloc[0]
            except IndexError:
                value = "n/a"
            data.get("features")[i]["attributes"]["Name_2018"] = value
        return data

    def get_environments_for_geometry_z_values(self, data) -> List[dict]:
        """
        Extracts the depth (Z) values from the geometry property in the
        response object. This method is useful for analyzing environmental
        data at different depth levels.

        :param data: The response data containing geometry information.
        """
        # Get the z values from the geometry property of the response object
        geometry = self.geometry
        coordinates = geometry.get("coordinates")
        if len(coordinates) == 3:
            zmin = geometry.get("coordinates")[2]
            zmax = geometry.get("coordinates")[2]
        else:
            zmin = None
            zmax = None
        res = []
        if zmin is None or zmax is None:  # Case with no z values
            for item in data["features"]:
                parsed = {
                    "attributes": {
                        "OceanName": item["attributes"]["OceanName"],
                        "Name_2018": item["attributes"]["Name_2018"],
                    }
                }
                res.append(dumps(parsed))
        else:  # Case when z values are present
            for item in data["features"]:
                top = item["attributes"]["UnitTop"]
                bottom = item["attributes"]["UnitBottom"]
                # Case where zmin and zmax are equal
                if (zmax <= top and zmax >= bottom) and (
                    zmin <= top and zmin >= bottom
                ):
                    parsed = {
                        "attributes": {
                            "OceanName": item["attributes"]["OceanName"],
                            "Name_2018": item["attributes"]["Name_2018"],
                        }
                    }
                    res.append(dumps(parsed))
                # Case where zmin and zmax are not equal (a depth interval)
                if (zmax <= top and zmax >= bottom) or (zmin <= top and zmin >= bottom):
                    parsed = {
                        "attributes": {
                            "OceanName": item["attributes"]["OceanName"],
                            "Name_2018": item["attributes"]["Name_2018"],
                        }
                    }
                    res.append(dumps(parsed))

        # Get the unique set of environments (don't want duplicates) and
        # convert back to a list as preferred by subsequent operations
        res = set(res)
        res = list(res)
        return res
