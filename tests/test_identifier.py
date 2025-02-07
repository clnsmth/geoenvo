"""Test the identifier module"""

from spinneret.identifier import Identifier
from spinneret.geometry import Geometry


def test_identify(mocker, use_mock, scenarios, assert_identify):

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
