"""The data_source module"""

from datetime import datetime
from json import dumps, loads
import pandas as pd
import requests
from geoenvo.data_sources.data_source import DataSource
from geoenvo.geometry import Geometry
from geoenvo.environment import Environment
from geoenvo.utilities import user_agent
from geoenvo.utilities import EnvironmentDataModel


class EcologicalMarineUnits(DataSource):
    def __init__(self):
        super().__init__()
        self._geometry = None
        self._data = None
        self._env_properties = {
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
    def env_properties(self):
        return self._env_properties

    @env_properties.setter
    def env_properties(self, env_properties: dict):
        self._env_properties = env_properties

    def resolve(self, geometry: Geometry):
        self.geometry = geometry.data  # required for filtering on depth
        self.data = self._request(geometry)
        return self.convert_data()

    @staticmethod
    def _request(geometry: Geometry):
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

    def convert_data(self):
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

    def unique_environment(self):
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

    def has_environment(self):
        # FIXME: This produces an error when running the geographic
        #  coverage in the file knb-lter-ntl.420.2.
        res = len(self.data["features"])
        if res == 0:
            return False
        if res > 0:
            return True

    def set_properties(self, unique_environment_properties):
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
        env_properties = self.env_properties
        atomic_property_labels = env_properties.keys()
        # Zip descriptors and atomic property labels
        environments = [dict(zip(atomic_property_labels, descriptors))]
        # Iterate over atomic properties and set labels
        environment = environments[0]
        # properties = {}
        # env_properties
        for property in environment.keys():
            label = environment.get(property)
            env_properties[property] = label
        # Add composite EMU_Description class
        # Get environments values and join with commas
        # TODO Fix issue where an property from the initialized list returned
        #  by  Attributes() was missing for some reason and thus an annotation
        #  couldn't  be found for it. If arbitrary joining of empties to the
        #  annotation string  is done, then the annotation may be wrong. Best
        #  to just leave it out.
        EMU_Descriptor = [f for f in env_properties.values()]
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
        env_properties["EMU_Descriptor"] = EMU_Descriptor

        # Convert properties into a more readable format
        new_env_properties = {
            "oceanName": env_properties["OceanName"],
            "depth": env_properties["Depth"],
            "temperature": env_properties["Temperature"],
            "salinity": env_properties["Salinity"],
            "dissolvedOxygen": env_properties["Dissolved Oxygen"],
            "nitrate": env_properties["Nitrate"],
            "phosphate": env_properties["Phosphate"],
            "silicate": env_properties["Silicate"],
            "ecosystem": env_properties["EMU_Descriptor"],
        }
        return new_env_properties


    def convert_codes_to_values(self):
        # Convert the codes listed under the Name_2018 and OceanName
        # properties to the descriptive string values so the EMU
        # response object more closely resembles the ECU and WTE
        # response objects and can be processed in the same way. This is a
        # tradeoff between processing the response object in a way that is
        # consistent with the other response objects (supporting readability)
        # and processing the response object in a way that may be more
        # efficient. Profiling has not yet been conducted on this.
        # Create the code-value map for OceanName
        data = self._data
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

    def get_environments_for_geometry_z_values(self, data):
        # - Get the z values from the geometry property of the response
        # object
        geometry = self._geometry
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
