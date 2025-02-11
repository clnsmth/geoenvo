"""The resolvers module"""

from datetime import datetime
from json import dumps, loads
import pandas as pd
import requests
from geoenvo.resolver import Resolver
from geoenvo.geometry import Geometry
from geoenvo.environment import Environment
from geoenvo.utilities import user_agent
from geoenvo.utilities import EnvironmentDataModel


class EcologicalMarineUnits(Resolver):
    def __init__(self):
        super().__init__()
        self._geometry = None
        self._data = None
        self._env_attributes = {
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
    def env_attributes(self):
        return self._env_attributes

    @env_attributes.setter
    def env_attributes(self, env_attributes: dict):
        self._env_attributes = env_attributes

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
        unique_emu_ecosystems = self.unique_environment()
        for unique_emu_ecosystem in unique_emu_ecosystems:
            ecosystem = EnvironmentDataModel()
            ecosystem.set_identifier("https://doi.org/10.5066/P9Q6ZSGN")
            ecosystem.set_resolver(self.__class__.__name__)
            ecosystem.set_date_created()
            attributes = self.set_attributes(  # TODO: Move this processing to self.unique_environment() to match WTE implmementation
                unique_ecosystem_attributes=unique_emu_ecosystem
            )
            ecosystem.set_properties(attributes)
            result.append(Environment(data=ecosystem.data))
        return result

    def unique_environment(self):
        if not self.has_ecosystem():
            return list()
        # FIXME? - get_ecosystems_for_geometry_z_values does two things:
        #  1. gets ecosystems for z values
        #  2. gets unique ecosystems
        #  This doesn't follow the pattern for WTE and ECU, where all
        #  ecosystems are first retrieved, then unique ecosystems are
        #  derived. Either this function should be split into two, or the
        #  WTE and ECU function's get and unique operations should be
        #  combined into one.

        # FIXME? This pattern differs from WTE and ECU implementations.
        #  Change? See implementation notes.
        data = self.convert_codes_to_values()

        # FIXME? This pattern differs from WTE and ECU implementations.
        #  Change? See implementation notes.
        descriptors = self.get_ecosystems_for_geometry_z_values(data=data)
        return descriptors

    def has_ecosystem(self):
        # FIXME: This produces an error when running the geographic
        #  coverage in the file knb-lter-ntl.420.2.
        res = len(self.data["features"])
        if res == 0:
            return False
        if res > 0:
            return True

    def set_attributes(self, unique_ecosystem_attributes):
        if len(unique_ecosystem_attributes) == 0:
            return None
        # There are two attributes for EMU, OceanName and Name_2018, the latter
        # of which is composed of 7 atomic attributes.
        attributes = loads(unique_ecosystem_attributes)["attributes"]
        # Get OceanName
        ocean_name = attributes.get("OceanName")
        # Atomize Name_2018: Split on commas and remove whitespace
        descriptors = attributes.get("Name_2018")
        descriptors = descriptors.split(",")
        descriptors = [g.strip() for g in descriptors]
        # Add ocean name to front of descriptors list in preparation for the
        # zipping operation below
        descriptors = [ocean_name] + descriptors
        env_attributes = self._env_attributes
        atomic_attribute_labels = env_attributes.keys()
        # Zip descriptors and atomic attribute labels
        ecosystems = [dict(zip(atomic_attribute_labels, descriptors))]
        # Iterate over atomic attributes and set labels and annotations
        ecosystem = ecosystems[0]
        # attributes = {}
        # env_attributes
        for attribute in ecosystem.keys():
            label = ecosystem.get(attribute)
            env_attributes[attribute] = label
        # Add composite EMU_Description class and annotation.
        # Get ecosystems values and join with commas
        # TODO Fix issue where an attribute from the initialized list returned
        #  by  Attributes() was missing for some reason and thus an annotation
        #  couldn't  be found for it. If arbitrary joining of empties to the
        #  annotation string  is done, then the annotation may be wrong. Best
        #  to just leave it out.
        EMU_Descriptor = [f for f in env_attributes.values()]
        # Knock of the last one, which is EMU_Descriptor
        EMU_Descriptor = EMU_Descriptor[:-1]

        # FIXME: This is a hack to deal with the fact that some of the
        #  attributes are None. This is a problem with the data, not the
        #  code. The code should be fixed to deal with this. This is related
        #  to the FIXMEs in convert_codes_to_values. The issue can be
        #  reproduced by running on the geographic coverage in the file
        #  knb-lter-sbc.100.11.xml.
        if None in EMU_Descriptor:
            EMU_Descriptor = ["n/a" if f is None else f for f in EMU_Descriptor]

        EMU_Descriptor = ", ".join(EMU_Descriptor)
        env_attributes["EMU_Descriptor"] = EMU_Descriptor

        # Convert property keys into a more readable format
        new_env_attributes = {
            "oceanName": env_attributes["OceanName"],
            "depth": env_attributes["Depth"],
            "temperature": env_attributes["Temperature"],
            "salinity": env_attributes["Salinity"],
            "dissolvedOxygen": env_attributes["Dissolved Oxygen"],
            "nitrate": env_attributes["Nitrate"],
            "phosphate": env_attributes["Phosphate"],
            "silicate": env_attributes["Silicate"],
            "ecosystem": env_attributes["EMU_Descriptor"],
        }
        return new_env_attributes

    @staticmethod
    def get_annotation(
        label: str,
    ):  # TODO deprecate this once moved to Environment class method
        return "Placeholder"  # TODO - add EMU sssom and parse

    def convert_codes_to_values(self):
        # Convert the codes listed under the Name_2018 and OceanName
        # attributes to the descriptive string values so the EMU
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

    def get_ecosystems_for_geometry_z_values(self, data):
        # - Get the z values from the geometry attribute of the response
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
        # Get the unique set of ecosystems (don't want duplicates) and
        # convert back to a list as preferred by subsequent operations
        res = set(res)
        res = list(res)
        return res
