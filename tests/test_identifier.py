"""Test the identifier module"""

from geoenvo.identifier import Identifier
from geoenvo.geometry import Geometry


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
