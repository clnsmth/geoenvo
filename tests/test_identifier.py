"""Test the identifier module"""

from geoenvo.identifier import Identifier
from geoenvo.geometry import Geometry
from geoenvo.data_sources import WorldTerrestrialEcosystems
from geoenvo.data_sources import EcologicalMarineUnits


def test_identify(use_mock, scenarios, assert_identify, mocker):
    for scenario in scenarios:

        if use_mock:
            mocker.patch("requests.get", return_value=scenario.get("response"))

        # Configure
        data_source = [scenario.get("data_source")]
        identifier = Identifier(data_source)
        geometry = Geometry(scenario.get("geometry"))

        # Run
        result = identifier.identify(geometry)

        # Assert
        assert_identify(result)


def test_data_source():
    # Get
    identifier = Identifier([WorldTerrestrialEcosystems()])
    assert identifier.data_source is not None
    assert isinstance(identifier.data_source, list)
    assert isinstance(identifier.data_source[0], WorldTerrestrialEcosystems)

    # Set
    identifier.data_source = [EcologicalMarineUnits()]
    assert identifier.data_source is not None
    assert isinstance(identifier.data_source, list)
    assert isinstance(identifier.data_source[0], EcologicalMarineUnits)
