"""Configuration for the test suite"""

import json
import tempfile
import pytest
from importlib.resources import files

from geoenvo.geometry import Geometry
from geoenvo.resolvers.ecological_coastal_units import EcologicalCoastalUnits
from geoenvo.resolvers.ecological_marine_units import EcologicalMarineUnits
from geoenvo.resolvers.world_terrestrial_ecosystems import WorldTerrestrialEcosystems
from geoenvo.utilities import Data, compile_response


@pytest.fixture()
def use_mock():
    return True  # Change this to False for real HTTP requests and data


@pytest.fixture
def resolvers():
    resolvers = [  # List of resolver instances
        EcologicalCoastalUnits(),
        EcologicalMarineUnits(),
        WorldTerrestrialEcosystems(),
    ]
    return resolvers


@pytest.fixture
def scenarios(
    raw_attributes_of_ecological_coastal_units,
    raw_attributes_of_ecological_marine_units,
    raw_attributes_of_world_terrestrial_ecosystems,
    attributes_of_ecological_coastal_units,
    attributes_of_ecological_marine_units,
    attributes_of_world_terrestrial_ecosystems,
):
    scenarios = [
        {  # WTE Success (Envelop on land)
            "resolvers": WorldTerrestrialEcosystems(),
            "response": load_response("wte_success"),
            "geometry": load_geometry("polygon_on_land"),
            "unique_environment": 1,
            "has_ecosystem": True,
            "raw_attributes": raw_attributes_of_world_terrestrial_ecosystems,
            "attributes": attributes_of_world_terrestrial_ecosystems,
            "identifier": "https://doi.org/10.5066/P9DO61LP",
        },
        {  # WTE Fail (A point over the ocean)
            "resolvers": WorldTerrestrialEcosystems(),
            "response": load_response("wte_fail"),
            "geometry": load_geometry("point_on_ocean"),
            "unique_environment": 0,
            "has_ecosystem": False,
            "raw_attributes": raw_attributes_of_world_terrestrial_ecosystems,
            "attributes": attributes_of_world_terrestrial_ecosystems,
            "identifier": "https://doi.org/10.5066/P9DO61LP",
        },
        {  # ECU Success (Envelop spanning coastal area)
            "resolvers": EcologicalCoastalUnits(),
            "response": load_response("ecu_success"),
            "geometry": load_geometry("polygon_on_land_and_ocean"),
            "unique_environment": 34,
            "has_ecosystem": True,
            "raw_attributes": raw_attributes_of_ecological_coastal_units,
            "attributes": attributes_of_ecological_coastal_units,
            "identifier": "https://doi.org/10.5066/P9HWHSPU",
        },
        {  # ECU Fail (Envelope on land)
            "resolvers": EcologicalCoastalUnits(),
            "response": load_response("ecu_fail"),
            "geometry": load_geometry("polygon_on_land"),
            "unique_environment": 0,
            "has_ecosystem": False,
            "raw_attributes": raw_attributes_of_ecological_coastal_units,
            "attributes": attributes_of_ecological_coastal_units,
            "identifier": "https://doi.org/10.5066/P9HWHSPU",
        },
        {  # EMU Success (Envelope over ocean)
            "resolvers": EcologicalMarineUnits(),
            "response": load_response("emu_success"),
            "geometry": load_geometry("polygon_on_ocean"),
            "unique_environment": 7,
            "has_ecosystem": True,
            "raw_attributes": raw_attributes_of_ecological_marine_units,
            "attributes": attributes_of_ecological_marine_units,
            "identifier": "https://doi.org/10.5066/P9Q6ZSGN",
        },
        {  # EMU Fail (Envelope on land)
            "resolvers": EcologicalMarineUnits(),
            "response": load_response("emu_fail"),
            "geometry": load_geometry("polygon_on_land"),
            "unique_environment": 0,
            "has_ecosystem": False,
            "raw_attributes": raw_attributes_of_ecological_marine_units,
            "attributes": attributes_of_ecological_marine_units,
            "identifier": "https://doi.org/10.5066/P9Q6ZSGN",
        },
    ]
    return scenarios


@pytest.fixture
def raw_attributes_of_ecological_coastal_units():
    return {
        "Slope",
        "Sinuosity",
        "Erodibility",
        "Temperature and Moisture Regime",
        "River Discharge",
        "Wave Height",
        "Tidal Range",
        "Marine Physical Environment",
        "Turbidity",
        "Chlorophyll",
        "CSU_Descriptor",
    }


@pytest.fixture
def attributes_of_ecological_coastal_units():
    return {
        "slope",
        "sinuosity",
        "erodibility",
        "temperatureAndMoistureRegime",
        "riverDischarge",
        "waveHeight",
        "tidalRange",
        "marinePhysicalEnvironment",
        "turbidity",
        "chlorophyll",
        "ecosystem",
    }


@pytest.fixture
def raw_attributes_of_ecological_marine_units():
    return {
        "OceanName",
        "Depth",
        "Temperature",
        "Salinity",
        "Dissolved Oxygen",
        "Nitrate",
        "Phosphate",
        "Silicate",
        "EMU_Descriptor",
    }


@pytest.fixture
def attributes_of_ecological_marine_units():
    return {
        "oceanName",
        "depth",
        "temperature",
        "salinity",
        "dissolvedOxygen",
        "nitrate",
        "phosphate",
        "silicate",
        "ecosystem",
    }


@pytest.fixture
def raw_attributes_of_world_terrestrial_ecosystems():
    return {
        "Raster.Temp_Class",
        "Raster.Moisture_C",
        "Raster.LC_ClassNa",
        "Raster.LF_ClassNa",
        "Raster.Temp_Moist",
        "Raster.ClassName",
    }


@pytest.fixture
def attributes_of_world_terrestrial_ecosystems():
    return {"temperature", "moisture", "landCover", "landForm", "climate", "ecosystem"}


@pytest.fixture
def empty_environment_data_model():
    return {
        "type": "Environment",
        "dataSource": {"identifier": None, "resolver": None},
        "dateCreated": None,
        "properties": {},
        "mappedProperties": [],
    }


@pytest.fixture
def empty_data_model():
    return {
        "type": "Feature",
        "identifier": None,
        "geometry": None,
        "properties": {"description": None, "environment": []},
    }


@pytest.fixture
def data_model(mocker):
    mocker.patch("requests.get", return_value=load_response("wte_success"))

    resolver = WorldTerrestrialEcosystems()
    geometry = Geometry(load_geometry("polygon_on_land"))
    environment = resolver.resolve(geometry)

    data = compile_response(
        geometry,
        environment,
        identifier="5b4edec5-ea5e-471a-8a3c-2c1171d59dee",
        description="Polygon on land",
    )
    data.apply_vocabulary_mapping()
    return data


def load_geometry(filename: str):
    """Load test geometry in JSON format."""
    with open(files("tests.data.geometry").joinpath(f"{filename}.json"), "r") as f:
        return json.load(f)


def load_response(filename: str):
    """Load test response in JSON format."""
    with open(files("tests.data.response").joinpath(f"{filename}.json"), "r") as f:
        return Response(json.load(f))


class Response:
    """A mock object of
    https://requests.readthedocs.io/en/latest/api/#requests.Response for
    testing purposes."""

    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


@pytest.fixture
def assert_identify():  # FIXME: success/fail is not the best description
    """Assert properties of a successful (or unsuccessful) response from the
    identify operation."""

    def _assert_identify(result: list):
        assert isinstance(result, Data)

        # Test the geometry object
        assert isinstance(result._data["geometry"], dict)

        # Test the environment objects
        for item in result._data["properties"]["environment"]:
            assert isinstance(item, dict)

        # Set vocabulary terms
        env_with_terms = result.apply_vocabulary_mapping()
        assert isinstance(env_with_terms, Data)
        assert isinstance(env_with_terms._data, dict)
        environment = env_with_terms._data["properties"]["environment"]
        if len(environment) > 0:
            assert isinstance(environment[0]["mappedProperties"], list)
            for key, value in environment[0]["mappedProperties"][0].items():
                assert key in {"label", "uri"}
                assert value is not None
                if key == "uri":
                    assert value.startswith("http")

        # Write to file
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_path = f"{tmpdirname}/file.json"
            result.write(file_path)  # TODO: use Data object
            data_snapshot = result._data  # Save for comparison with read data

            # Read from file
            data = Data()
            data.read(file_path)  # TODO: use Data object
            assert data_snapshot == data._data
            assert isinstance(data._data, dict)

    return _assert_identify


@pytest.fixture
def assert_data_model():
    """Assert properties of the data model returned by the convert_data method."""

    def _assert_data_model(result: Data):
        assert isinstance(result, Data)
        assert isinstance(result._data, dict)

    return _assert_data_model


def _load_conversion_factors():  # TODO move to utilities?
    """Load conversion factors

    Returns
    -------
    dict : conversion factors
        Dictionary of conversion factors for converting from common units of
        length to meters.
    """
    conversion_factors = {
        "meter": 1,
        "decimeter": 1e-1,
        "dekameter": 1e1,
        "hectometer": 1e2,
        "kilometer": 1e3,
        "megameter": 1e6,
        "Foot_US": 0.3048006,
        "foot": 0.3048,
        "Foot_Gold_Coast": 0.3047997,
        "fathom": 1.8288,
        "nauticalMile": 1852,
        "yard": 0.9144,
        "Yard_Indian": 0.914398530744440774,
        "Link_Clarke": 0.2011661949,
        "Yard_Sears": 0.91439841461602867,
        "mile": 1609.344,
    }
    return conversion_factors
