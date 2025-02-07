"""The identify module"""

from typing import List
from spinneret.resolver import Resolver
from spinneret.geometry import Geometry
from spinneret.utilities import compile_response, Data
from tests.conftest import load_geometry


class Identifier:
    def __init__(self, resolver: List[Resolver]):
        self._resolver = resolver

    def identify(self, geometry: Geometry, identifier: str = None) -> Data:
        try:
            results = []
            for resolver in self._resolver:
                environment = resolver.resolve(geometry)
                results.extend(environment)
            result = compile_response(
                geometry=geometry, environment=results, identifier=identifier
            )
            result.set_envo_terms()
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            result = compile_response(geometry=geometry, environment=[])
            return result


if __name__ == "__main__":
    import json
    from spinneret.resolvers.world_terrestrial_ecosystems import (
        WorldTerrestrialEcosystems,
    )
    from spinneret.resolvers.ecological_marine_units import EcologicalMarineUnits
    from spinneret.resolvers.ecological_coastal_units import EcologicalCoastalUnits
    from spinneret.identifier import Identifier
    from spinneret.geometry import Geometry

    # Create a geometry in GeoJSON format
    # polygon_on_land_and_ocean = load_geometry(
    #     "polygon_on_land_and_ocean_example")
    polygon_on_land_and_ocean = {
        "type": "Polygon",
        "coordinates": [
            [
                [-123.716239, 39.325978],
                [-123.8222818, 39.3141049],
                [-123.8166231, 39.2943269],
                [-123.716239, 39.325978],
            ]
        ],
    }
    geometry = Geometry(polygon_on_land_and_ocean)

    # Configure the identifier with data sources to query
    identifier = Identifier(
        resolver=[
            WorldTerrestrialEcosystems(),
            EcologicalMarineUnits(),
            EcologicalCoastalUnits(),
        ]
    )

    # Identify the environment for the geometry
    result = identifier.identify(geometry)

    print(json.dumps(result._data, indent=2))
