"""Test the identifier module"""

from geoenvo.identifier import Identifier
from geoenvo.geometry import Geometry
from geoenvo.resolvers.world_terrestrial_ecosystems import WorldTerrestrialEcosystems
from geoenvo.resolvers.ecological_marine_units import EcologicalMarineUnits


def test_identify(use_mock, scenarios, assert_identify, mocker):
    for scenario in scenarios:

        if use_mock:
            mocker.patch("requests.get", return_value=scenario.get("response"))

        # Configure
        resolver = [scenario.get("resolvers")]
        identifier = Identifier(resolver)
        geometry = Geometry(scenario.get("geometry"))

        # Run
        result = identifier.identify(geometry)

        # Assert
        assert_identify(result)


def test_resolver():
    # Get
    identifier = Identifier([WorldTerrestrialEcosystems()])
    assert identifier.resolver is not None
    assert isinstance(identifier.resolver, list)
    assert isinstance(identifier.resolver[0], WorldTerrestrialEcosystems)

    # Set
    identifier.resolver = [EcologicalMarineUnits()]
    assert identifier.resolver is not None
    assert isinstance(identifier.resolver, list)
    assert isinstance(identifier.resolver[0], EcologicalMarineUnits)


