"""Create mock data for the tests"""

from json import dumps
from pathlib import Path
from importlib.resources import files

from pytest_mock import mocker
from requests import get

from geoenvo.geometry import Geometry
from geoenvo.data_sources import WorldTerrestrialEcosystems
from geoenvo.data_sources import EcologicalCoastalUnits
from geoenvo.data_sources import EcologicalMarineUnits
from geoenvo.resolver import compile_response
from tests.conftest import load_geometry, load_response


def create_mock_response_content(
    output_directory: Path = files("tests.data.response"),
) -> None:
    """Get response content for each data_source, and for both success and fail
    scenarios, then write to file in tests/data. Success scenarios are when the
    input geometry returns results. Fail scenarios are when the input geometry
    returns no results.
    """

    # WTE Success
    geometry = Geometry(load_geometry("polygon_on_land"))
    data_source = WorldTerrestrialEcosystems()
    response = data_source._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("wte_success.json"), "w") as f:
        f.write(json)

    # WTE Fail
    geometry = Geometry(load_geometry("point_on_ocean"))
    data_source = WorldTerrestrialEcosystems()
    response = data_source._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("wte_fail.json"), "w") as f:
        f.write(json)

    # ECU Success
    geometry = Geometry(load_geometry("polygon_on_land_and_ocean"))
    data_source = EcologicalCoastalUnits()
    response = data_source._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("ecu_success.json"), "w") as f:
        f.write(json)

    # ECU Fail
    geometry = Geometry(load_geometry("polygon_on_land"))
    data_source = EcologicalCoastalUnits()
    response = data_source._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("ecu_fail.json"), "w") as f:
        f.write(json)

    # EMU Success
    geometry = Geometry(load_geometry("polygon_on_ocean"))
    data_source = EcologicalMarineUnits()
    response = data_source._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("emu_success.json"), "w") as f:
        f.write(json)

    # EMU Fail
    geometry = Geometry(load_geometry("polygon_on_land"))
    data_source = EcologicalMarineUnits()
    response = data_source._request(geometry)
    json = dumps(response, indent=4)
    with open(output_directory.joinpath("emu_fail.json"), "w") as f:
        f.write(json)

    # EMU Success (another one, for testing depth inputs)
    geometry = Geometry(load_geometry("point_on_ocean_with_depth"))
    data_source = EcologicalMarineUnits()
    response = data_source._request(geometry)
    json = dumps(response, indent=4)
    with open(
        output_directory.joinpath("emu_success_point_on_ocean_with_depth.json"), "w"
    ) as f:
        f.write(json)


def create_schema_org_fixture(
    output_directory: Path = files("tests.data.schema_org"),
) -> None:
    # This code should match that of the data_model fixture for purposes of
    # comparison.

    data_source = WorldTerrestrialEcosystems()
    geometry = Geometry(load_geometry("polygon_on_land"))
    environment = data_source.resolve(geometry)
    data = compile_response(
        geometry,
        environment,
        identifier="5b4edec5-ea5e-471a-8a3c-2c1171d59dee",
        description="Polygon on land",
    )

    data.apply_term_mapping()
    schema_org = dumps(data.to_schema_org(), indent=4)

    with open(output_directory.joinpath("schema_org.jsonld"), "w") as f:
        f.write(schema_org)


if __name__ == "__main__":
    create_mock_response_content()
    # create_schema_org_fixture()
    pass
