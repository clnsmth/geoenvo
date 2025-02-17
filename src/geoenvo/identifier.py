"""The identify module"""

from typing import List
from geoenvo.data_sources.data_source import DataSource
from geoenvo.geometry import Geometry
from geoenvo.utilities import compile_response, Data
from tests.conftest import load_geometry


class Identifier:
    def __init__(self, data_source: List[DataSource]):
        self._data_source = data_source

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, data_source: List[DataSource]):
        self._data_source = data_source

    def identify(
        self,
        geometry: Geometry,
        vocabulary: str = "ENVO",
        identifier: str = None,
        description: str = None,
    ) -> Data:
        try:
            results = []
            for data_source in self.data_source:
                environment = data_source.resolve(geometry)
                results.extend(environment)
            result = compile_response(
                geometry=geometry,
                environment=results,
                identifier=identifier,
                description=description,
            )
            result.apply_vocabulary_mapping(vocabulary)
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            result = compile_response(geometry=geometry, environment=[])
            return result


if __name__ == "__main__":

    from json import dumps
    from geoenvo.data_sources import (
        WorldTerrestrialEcosystems,
    )
    from geoenvo.identifier import Identifier
    from geoenvo.geometry import Geometry

    # Create a geometry in GeoJSON format
    polygon_on_land = {
        "type": "Polygon",
        "coordinates": [
            [
                [-123.552, 39.804],
                [-120.83, 39.804],
                [-120.83, 40.441],
                [-123.552, 40.441],
                [-123.552, 39.804],
            ]
        ],
    }
    geometry = Geometry(polygon_on_land)

    # Configure the identifier with one or more data sources
    identifier = Identifier(data_source=[WorldTerrestrialEcosystems()])

    # Identify the environment for the geometry
    result = identifier.identify(
        geometry,
        identifier="5b4edec5-ea5e-471a-8a3c-2c1171d59dee",
        description="Polygon on land",
    )

    # The result is a GeoJSON feature with environmental properties
    print(dumps(result.data, indent=2))

    # The result can be converted to Schema.org JSON-LD
    schema_org = result.to_schema_org()
    print(dumps(schema_org, indent=2))
