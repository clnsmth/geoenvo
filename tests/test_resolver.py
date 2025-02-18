"""Test the resolver module"""

from geoenvo.resolver import Resolver
from geoenvo.geometry import Geometry
from geoenvo.data_sources import WorldTerrestrialEcosystems
from geoenvo.data_sources import EcologicalMarineUnits


def test_identify(use_mock, scenarios, assert_identify, mocker):
    for scenario in scenarios:

        if use_mock:
            mocker.patch("requests.get", return_value=scenario.get("response"))

        # Configure
        data_source = [scenario.get("data_source")]
        resolver = Resolver(data_source)
        geometry = Geometry(scenario.get("geometry"))

        # Run
        result = resolver.resolve(geometry)

        # Assert
        assert_identify(result, scenario)


def test_data_source():
    # Get
    resolver = Resolver([WorldTerrestrialEcosystems()])
    assert resolver.data_source is not None
    assert isinstance(resolver.data_source, list)
    assert isinstance(resolver.data_source[0], WorldTerrestrialEcosystems)

    # Set
    resolver.data_source = [EcologicalMarineUnits()]
    assert resolver.data_source is not None
    assert isinstance(resolver.data_source, list)
    assert isinstance(resolver.data_source[0], EcologicalMarineUnits)
