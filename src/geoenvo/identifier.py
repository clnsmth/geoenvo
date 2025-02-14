"""The identify module"""

from typing import List
from geoenvo.resolver import Resolver
from geoenvo.geometry import Geometry
from geoenvo.utilities import compile_response, Data
from tests.conftest import load_geometry


class Identifier:
    def __init__(self, resolver: List[Resolver]):
        self._resolver = resolver

    @property
    def resolver(self):
        return self._resolver

    @resolver.setter
    def resolver(self, resolver: List[Resolver]):
        self._resolver = resolver

    def identify(
        self, geometry: Geometry, vocabulary: str = "ENVO", identifier: str = None, description: str = None
    ) -> Data:
        try:
            results = []
            for resolver in self.resolver:
                environment = resolver.resolve(geometry)
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
    from geoenvo.resolvers.world_terrestrial_ecosystems import (
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
    identifier = Identifier(resolver=[WorldTerrestrialEcosystems()])

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
