"""Test the utilities module"""

import json
from importlib.resources import files
from geoenvo.geometry import Geometry
from geoenvo.resolvers.world_terrestrial_ecosystems import WorldTerrestrialEcosystems
from geoenvo.utilities import (
    EnvironmentDataModel,
    get_attributes,
    compile_response,
    Data,
)
from tests.conftest import load_response, load_geometry


def test_set_identifier():
    """Test the set_identifier adds the identifier to the data model"""

    # No attributes to start
    environment = EnvironmentDataModel()
    assert environment.data["dataSource"]["identifier"] is None

    # Identifier is present after running the method
    identifier = "Some arbitrary identifier"
    environment.set_identifier(identifier)
    assert environment.data["dataSource"]["identifier"] == identifier


def test_set_resolver():
    """Test the set_resolver adds the resolver to the data model"""

    # No attributes to start
    environment = EnvironmentDataModel()
    assert environment.data["dataSource"]["resolver"] is None

    # resolver is present after running the method
    resolver = "Some arbitrary resolver"
    environment.set_resolver(resolver)
    assert environment.data["dataSource"]["resolver"] == resolver


def test_set_date_created():
    """Test the set_date_created adds the date_created to the data model"""

    # No attributes to start
    environment = EnvironmentDataModel()
    assert environment.data["dateCreated"] is None

    # Date_created is present after running the method
    environment.set_date_created()
    assert environment.data["dateCreated"] is not None


def test_set_properties():
    """Test the set_properties adds the properties to the data model"""

    # No attributes to start
    environment = EnvironmentDataModel()
    assert len(environment.data["properties"]) == 0

    # Properties are present after running the method
    environment.set_properties({"Some property": "Some value"})
    assert len(environment.data["properties"]) > 0


def test_data_model(empty_environment_data_model):
    """Test the EnvironmentDataModel class"""
    data_model = EnvironmentDataModel()

    # Has the correct default values
    assert data_model.data == empty_environment_data_model


def test_get_attributes():
    """Test the get_attributes function."""
    response = load_response("wte_success")

    # The get_attributes function should return a dictionary of attributes
    # from the response object. The dictionary should contain the requested
    # attributes.
    attributes = ["Raster.LF_ClassNa", "Raster.LC_ClassNa", "Raster.Temp_Class"]
    result = get_attributes(response.data, attributes)
    assert isinstance(result, dict)
    for a in attributes:
        assert a in result
        assert len(result[a]) > 0

    # An empty list is returned for attributes that are not present.
    result = get_attributes(response.data, ["Not a valid attribute"])
    assert "Not a valid attribute" in result
    assert len(result["Not a valid attribute"]) == 0


def test_compile_response(scenarios, mocker, empty_data_model):
    # Compiles a list of Environment into the data model represented by the
    # Data object and tests for expected properties

    # Create a list of Environment objects, then compile
    environments = []
    for scenario in scenarios:
        mocker.patch("requests.get", return_value=scenario.get("response"))
        resolver = scenario["resolvers"]
        environment = resolver.resolve(Geometry(scenario["geometry"]))
        environments.extend(environment)
    identifier = "Some identifier"
    geometry = scenarios[0]["geometry"]  # Any geometry will do
    result = compile_response(Geometry(geometry), environments, identifier)

    # Top level keys are present
    assert result._data.keys() == empty_data_model.keys()
    # Identifier value matches the input
    assert result._data["identifier"] == identifier
    # Geometry value matches the input
    assert result._data["geometry"] == geometry
    # Environment is a list of environments, which are dictionaries
    assert isinstance(result._data["properties"]["environment"], list)
    # Check that the environment are a list of dictionaries
    for env in result._data["properties"]["environment"]:
        assert isinstance(env, dict)


def test_apply_vocabulary_mapping(data_model):
    # Remove the vocabulary terms from the test data model to set the baseline
    # for the test
    data_model.data["properties"]["environment"][0]["mappedProperties"] = []
    data = data_model

    # Apply vocabulary mapping for each environment
    data.apply_vocabulary_mapping("ENVO")

    # Check that the vocabulary terms are set for each environment, and that
    # no "sssom:NoMapping" is present
    for item in data._data["properties"]["environment"]:
        assert len(item["mappedProperties"]) > 0
        for term in item["mappedProperties"]:
            assert "sssom:nomapping" not in term["uri"].lower()


def test_apply_vocabulary_mapping_for_unrecognized_vocabularies(data_model):
    # Remove the vocabulary terms from the test data model to set the baseline
    # for the test
    data_model.data["properties"]["environment"][0]["mappedProperties"] = []

    # Apply a vocabulary mapping for an unrecognized vocabulary results in no
    # changes to the data model
    data_model.apply_vocabulary_mapping("SomeUnrecognizedVocabulary")
    assert data_model.data["properties"]["environment"][0]["mappedProperties"] == []


def test_data_methods_of_data_class():
    # Getter
    d = {"type": "Feature"}
    data = Data({"type": "Feature"})
    assert data.data == d

    # Setter
    d = {"type": "Environment"}
    data.data = d
    assert data.data == d


def test_attributes_methods_of_data_class():
    # Getter
    data = Data({"type": "Feature"})
    assert data.attributes is not None
    assert isinstance(data.attributes, dict)

    # Setter
    value = {"Some attribute": "Some value"}
    assert data.attributes != value
    data.attributes = value
    assert data.attributes == value


def test_data_methods_of_environment_data_model_class():
    # Getter
    environment = EnvironmentDataModel()
    assert environment.data is not None
    assert isinstance(environment.data, dict)

    # Setter
    value = {"type": "Feature"}
    assert environment.data != value
    environment.data = value
    assert environment.data == value


def test_to_schema_org(data_model):
    # Create instance of the Data object to convert to schema.org format.

    schema_org = data_model.to_schema_org()

    # Load from file
    with open(files("tests.data.schema_org").joinpath(f"schema_org.jsonld"), "r") as f:
        expected = json.load(f)

    assert schema_org == expected


def test__to_schema_org_geo(data_model):
    # Polygon
    geo = data_model._to_schema_org_geo()
    assert geo == {
        "@type": "GeoShape",
        "polygon": "39.804 -123.552 39.804 -120.83 40.441 -120.83 40.441 -123.552 39.804 -123.552",
    }

    # Point
    data_model.data["geometry"]["type"] = "Point"
    data_model.data["geometry"]["coordinates"] = [-123.552, 39.804, 0]
    geo = data_model._to_schema_org_geo()
    assert geo == {
        "@type": "GeoCoordinates",
        "latitude": 39.804,
        "longitude": -123.552,
        "elevation": 0,
    }

    # Other types
    data_model.data["geometry"]["type"] = "LineString"
    geo = data_model._to_schema_org_geo()
    assert geo is None


def test__to_schema_org_additional_property(data_model):
    # With properties
    additional_property = data_model._to_schema_org_additional_property()
    assert isinstance(additional_property, list)
    for item in additional_property:
        assert isinstance(item, dict)
        assert item["@type"] == "PropertyValue"
        assert "name" in item
        assert "value" in item

    # With duplicates removed
    data_model.data["properties"]["environment"].append(
        data_model.data["properties"]["environment"][0]
    )
    additional_property = data_model._to_schema_org_additional_property()
    for item in additional_property:
        assert additional_property.count(item) == 1

    # Without properties
    data = data_model
    data.data["properties"]["environment"] = []
    additional_property = data._to_schema_org_additional_property()
    assert additional_property is None


def test__to_schema_org_keywords(data_model):
    # With ENVO terms
    keywords = data_model._to_schema_org_keywords()
    assert isinstance(keywords, list)
    for item in keywords:
        assert "@id" in item
        assert "@type" in item
        assert "name" in item
        assert "inDefinedTermSet" in item
        assert "termCode" in item

    # With duplicates removed
    data_model.data["properties"]["environment"].append(
        data_model.data["properties"]["environment"][0]
    )
    keywords = data_model._to_schema_org_keywords()
    for item in keywords:
        assert keywords.count(item) == 1

    # Without ENVO terms
    data = data_model
    data.data["properties"]["environment"] = []
    keywords = data._to_schema_org_keywords()
    assert keywords is None
