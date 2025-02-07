"""Test the EcologicalMarineUnits resolver"""

from json import loads

from tests.conftest import load_response, load_geometry
from geoenvo.resolvers.ecological_marine_units import EcologicalMarineUnits


def test_convert_codes_to_values():
    """Test the convert_codes_to_values method

    Codes listed in the response object should be converted to their string
    value equivalents."""

    # Successful response from the EMU resolver
    resolver = EcologicalMarineUnits()
    resolver._data = load_response("emu_success").json()
    # Codes are numeric values initially
    for feature in resolver._data.get("features"):
        assert isinstance(feature.get("attributes").get("Name_2018"), int)
        assert isinstance(feature.get("attributes").get("OceanName"), int)
    # Codes are strings after conversion
    resolver.convert_codes_to_values()
    for feature in resolver._data.get("features"):
        assert isinstance(feature.get("attributes").get("Name_2018"), str)
        assert isinstance(feature.get("attributes").get("OceanName"), str)

    # Unsuccessful response from the EMU resolver
    resolver = EcologicalMarineUnits()
    resolver._data = load_response("emu_fail").json()
    # The response is an empty list
    assert isinstance(resolver._data.get("features"), list)
    assert len(resolver._data.get("features")) == 0


def test_get_ecosystems_for_geometry_z_values():
    """Test the get_ecosystems_for_geometry method.

    When a geometry has a single z value (i.e. discrete depth) the
    get_ecosystems_for_geometry_z_values method should return any EMUs
    intersecting with the z value, including both bounding EMUs when the z
    value equals the boundary between the 2 EMUs. When a geometry has 2 z
    values (i.e. range of depths) the method should return any EMUs
    intersecting with the range, including both bounding EMUs when the z value
    equals the boundary between the 2 EMUs. When a geometry has no z values
    (i.e. no depth) the method should return all EMUs.

    Rather than using a set of geographic coverage fixtures, each exemplifying
    the scenarios, we reduce the number of API calls to the EMU server by
    modifying the z values of the response objects geometry attribute.

    The results of the assertions were determined by visual inspection of the
    EMU server map service interface at the geographic coverage represented in
    the test fixture. Or rather the test fixture was set based on a specific
    data point in the EMU server map service interface.
    """

    # A set of tests on a point location with z values
    resolver = EcologicalMarineUnits()
    resolver._data = load_response("emu_success_point_on_ocean_with_depth").json()
    resolver._geometry = load_geometry("point_on_ocean_with_depth")

    # Single z value within EMU returns one EMU
    ecosystems = resolver.get_ecosystems_for_geometry_z_values(resolver._data)
    expected_ecosystems = {18}
    assert isinstance(ecosystems, list)
    for ecosystem in ecosystems:
        assert isinstance(ecosystem, str)
        assert loads(ecosystem)["attributes"]["Name_2018"] in expected_ecosystems
    assert len(ecosystems) == 1

    # Single z value on the border between two EMUs returns two EMUs
    resolver._geometry["coordinates"][2] = -30
    ecosystems = resolver.get_ecosystems_for_geometry_z_values(resolver._data)
    expected_ecosystems = {18, 24}
    assert isinstance(ecosystems, list)
    for ecosystem in ecosystems:
        assert isinstance(ecosystem, str)
        assert loads(ecosystem)["attributes"]["Name_2018"] in expected_ecosystems
    assert len(ecosystems) == 2

    # No z values returns all EMUs.
    resolver._geometry["coordinates"][2] = None
    ecosystems = resolver.get_ecosystems_for_geometry_z_values(resolver._data)
    expected_ecosystems = {18, 24, 11, 26, 8, 19}
    assert isinstance(ecosystems, list)
    for ecosystem in ecosystems:
        assert isinstance(ecosystem, str)
        assert loads(ecosystem)["attributes"]["Name_2018"] in expected_ecosystems
    assert len(ecosystems) == 6
