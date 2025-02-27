"""The resolve module"""

from typing import List
from geoenvo.data_sources.data_source import DataSource
from geoenvo.geometry import Geometry
from geoenvo.utilities import compile_response, Response
from tests.conftest import load_geometry


class Resolver:
    def __init__(self, data_source: List[DataSource]):
        self._data_source = data_source

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, data_source: List[DataSource]):
        self._data_source = data_source

    def resolve(
        self,
        geometry: Geometry,
        semantic_resource: str = "ENVO",
        identifier: str = None,
        description: str = None,
    ) -> Response:
        try:
            results = []
            for item in self.data_source:
                environment = item.resolve(geometry)
                results.extend(environment)
            result = compile_response(
                geometry=geometry,
                environment=results,
                identifier=identifier,
                description=description,
            )
            result.apply_term_mapping(semantic_resource)
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            result = compile_response(geometry=geometry, environment=[])
            return result


if __name__ == "__main__":

    from json import dumps
    from geoenvo.data_sources import WorldTerrestrialEcosystems
    from geoenvo.resolver import Resolver
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

    # Configure the resolver with one or more data sources
    resolver = Resolver(data_source=[WorldTerrestrialEcosystems()])

    # Resolve the geometry to environmental descriptions
    response = resolver.resolve(
        geometry,
        identifier="5b4edec5-ea5e-471a-8a3c-2c1171d59dee",
        description="Polygon on land",
    )

    # The response is a GeoJSON feature with environmental properties
    print(dumps(response.data, indent=2))

    # Format as Schema.org
    schema_org = response.to_schema_org()

