"""
ecological_marine_units.py
===========================

This module defines the ``EcologicalMarineUnits`` class, a concrete
implementation of the ``DataSource`` abstract base class (ABC). This class
interacts with the Ecological Marine Units dataset, retrieving environmental
information for marine regions based on geographic locations.

Key functionalities of this module include:

- Querying and resolving spatial geometries to marine environmental
  classifications.
- Structuring and converting data into a standardized format.
- Extracting unique environmental descriptions from the dataset.
"""

from datetime import datetime
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
    environmental classifications from the Ecological Marine Units dataset.

    Note, this data source supports the resolution of geometries with ``z``
    values (depth). To retrieve environmental data at different depths,
    include the ``z`` component in the input geometry. No additional property
    is required.
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

    def resolve(self, geometry: Geometry) -> List[Environment]:
        self.geometry = geometry.data  # required for filtering on depth
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
            "f": "json",  # GEOJSON doesn't return OceanName and Name_2018
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
            properties = self.set_properties(  # TODO: Move this processing to self.unique_environment() to match WTE implmementation
                unique_environment_properties=unique_emu_environment
            )
            environment.set_properties(properties)
            result.append(Environment(data=environment.data))
        return result

    def unique_environment(self) -> List[dict]:
        if not self.has_environment():
            return list()
        # FIXME? - get_environments_for_geometry_z_values does two things:
        #  1. gets environments for z values
        #  2. gets unique environments
        #  This doesn't follow the pattern for WTE and ECU, where all
        #  environments are first retrieved, then unique environments are
        #  derived. Either this function should be split into two, or the
        #  WTE and ECU function's get and unique operations should be
        #  combined into one.

        # FIXME? This pattern differs from WTE and ECU implementations.
        #  Change? See implementation notes.
        data = self.convert_codes_to_values()

        # FIXME? This pattern differs from WTE and ECU implementations.
        #  Change? See implementation notes.
        descriptors = self.get_environments_for_geometry_z_values(data=data)
        return descriptors

    def has_environment(self) -> bool:
        # FIXME: This produces an error when running the geographic
        #  coverage in the file knb-lter-ntl.420.2.
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
        # There are two properties for EMU, OceanName and Name_2018, the latter
        # of which is composed of 7 atomic properties.
        properties = loads(unique_environment_properties)["attributes"]
        # Get OceanName
        ocean_name = properties.get("OceanName")
        # Atomize Name_2018: Split on commas and remove whitespace
        descriptors = properties.get("Name_2018")
        descriptors = descriptors.split(",")
        descriptors = [g.strip() for g in descriptors]
        # Add ocean name to front of descriptors list in preparation for the
        # zipping operation below
        descriptors = [ocean_name] + descriptors
        properties = self.properties
        atomic_property_labels = properties.keys()
        # Zip descriptors and atomic property labels
        environments = [dict(zip(atomic_property_labels, descriptors))]
        # Iterate over atomic properties and set labels
        environment = environments[0]
        # properties = {}
        # properties
        for property in environment.keys():
            label = environment.get(property)
            properties[property] = label
        # Add composite EMU_Description class
        # Get environments values and join with commas
        # TODO Fix issue where an property from the initialized list returned
        #  by  Attributes() was missing for some reason and thus an annotation
        #  couldn't  be found for it. If arbitrary joining of empties to the
        #  annotation string  is done, then the annotation may be wrong. Best
        #  to just leave it out.
        EMU_Descriptor = [f for f in properties.values()]
        # Knock of the last one, which is EMU_Descriptor
        EMU_Descriptor = EMU_Descriptor[:-1]

        # FIXME: This is a hack to deal with the fact that some of the
        #  properties are None. This is a problem with the data, not the
        #  code. The code should be fixed to deal with this. This is related
        #  to the FIXMEs in convert_codes_to_values. The issue can be
        #  reproduced by running on the geographic coverage in the file
        #  knb-lter-sbc.100.11.xml.
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
        # Convert the codes listed under the Name_2018 and OceanName
        # properties to the descriptive string values so the EMU
        # response object more closely resembles the ECU and WTE
        # response objects and can be processed in the same way. This is a
        # tradeoff between processing the response object in a way that is
        # consistent with the other response objects (supporting readability)
        # and processing the response object in a way that may be more
        # efficient. Profiling has not yet been conducted on this.
        # Create the code-value map for OceanName
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
            # OceeanName
            code = data.get("features")[i]["attributes"]["OceanName"]

            # FIXME: Not all locations have OceanName values (e.g. is a
            #  bay or lake). There is probably a better value to use here.
            #  To recreate this issue run on the geographic coverage
            #  present in knb-lter-bes.5025.1.xml
            if code is None:
                value = "Not an ocean"
            else:
                value = ocean_name_map.loc[ocean_name_map["code"] == code, "name"].iloc[
                    0
                ]

            data.get("features")[i]["attributes"]["OceanName"] = value
            # Name_2018
            code = data.get("features")[i]["attributes"]["Name_2018"]

            # FIXME Not all locations have Name_2018 values (not sure why
            #  this is the case). To recreate this issue run on the
            #  geographic coverage present in knb-lter-sbc.100.11.xml,
            #  edi.99.5.xml.
            try:
                value = name_2018_map.loc[name_2018_map["code"] == code, "name"].iloc[0]
            except IndexError:
                value = "n/a"
            data.get("features")[i]["attributes"]["Name_2018"] = value
        return data  # TODO: why not set to self._data?

    def get_environments_for_geometry_z_values(self, data) -> List[dict]:
        """
        Extracts the depth (Z) values from the geometry property in the
        response object. This method is useful for analyzing environmental
        data at different depth levels.

        :param data: The response data containing geometry information.
        """
        # - Get the z values from the geometry property of the response
        # object
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
