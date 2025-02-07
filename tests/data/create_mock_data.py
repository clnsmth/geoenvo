"""Create mock data for the tests"""

from json import dumps
from pathlib import Path
from importlib.resources import files
from requests import get

from spinneret.geometry import Geometry
from spinneret.resolvers.world_terrestrial_ecosystems import WorldTerrestrialEcosystems
from spinneret.resolvers.ecological_coastal_units import EcologicalCoastalUnits
from spinneret.resolvers.ecological_marine_units import EcologicalMarineUnits
from spinneret.utilities import user_agent
from tests.conftest import load_geometry


def create_mock_response_content(
    output_directory: Path = files("tests.data.response"),
) -> None:
    """Get response content for each resolver, and for both success and fail
    scenarios, then write to file in tests/data. Success scenarios are when the
    input geometry returns results. Fail scenarios are when the input geometry
    returns no results.
    """

    # WTE Success
    geometry = Geometry(load_geometry("polygon_on_land"))
    resolver = WorldTerrestrialEcosystems()
    response = resolver._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("wte_success.json"), "w") as f:
        f.write(json)

    # WTE Fail
    geometry = Geometry(load_geometry("point_on_ocean"))
    resolver = WorldTerrestrialEcosystems()
    response = resolver._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("wte_fail.json"), "w") as f:
        f.write(json)

    # ECU Success
    geometry = Geometry(load_geometry("polygon_on_ocean_2"))
    resolver = EcologicalCoastalUnits()
    response = resolver._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("ecu_success.json"), "w") as f:
        f.write(json)

    # ECU Fail
    geometry = Geometry(load_geometry("polygon_on_land"))
    resolver = EcologicalCoastalUnits()
    response = resolver._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("ecu_fail.json"), "w") as f:
        f.write(json)

    # EMU Success
    geometry = Geometry(load_geometry("polygon_on_ocean"))
    resolver = EcologicalMarineUnits()
    response = resolver._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("emu_success.json"), "w") as f:
        f.write(json)

    # EMU Fail
    geometry = Geometry(load_geometry("polygon_on_land"))
    resolver = EcologicalMarineUnits()
    response = resolver._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("emu_fail.json"), "w") as f:
        f.write(json)

    # EMU Success (another one, for testing depth inputs)
    geometry = Geometry(load_geometry("point_on_ocean_with_depth"))
    resolver = EcologicalMarineUnits()
    response = resolver._request(geometry)
    json = dumps(response, indent=4)
    with open(
        output_directory.joinpath("emu_success_point_on_ocean_with_depth.json"), "w"
    ) as f:
        f.write(json)


if __name__ == "__main__":
    create_mock_response_content()
