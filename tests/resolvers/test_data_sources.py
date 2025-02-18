"""Test the data_source modules"""


def test_data_source_init(data_sources):
    """Test the DataSource class initialization"""
    for data_source in data_sources:
        assert data_source._geometry is None
        assert data_source._data is None
        assert len(data_source._env_properties) > 0


def test_data_source_properties(scenarios):
    """Test that the DataSource instance classes have the expected properties"""
    for scenario in scenarios:
        properties = scenario.get("data_source")._env_properties
        expected_properties = scenario.get("raw_properties")
        assert all([key in expected_properties for key in properties.keys()])


def test_get_unique_environments(scenarios):
    """Test the get_unique_environments method.

    The get_unique_environments method should return a set of unique environments
    contained in a given server response object. The way environments are
    expressed by each server (in JSON format) differs, so the function should
    be capable of recognizing the format and parsing it accordingly. The set
    object returned by the get_unique_environments method enables iterative
    parsing of the contents by the builder routine of the get_wte_environments
    and get_ecu_environments methods of the Response object. Note, currently,
    the resolve operation used to query the WTE server does not return more
    than one environment per query.
    """
    for scenario in scenarios:
        # Configure the data_source
        data_source = scenario["data_source"]
        data_source._data = scenario["response"].json()
        data_source._geometry = scenario["geometry"]

        # Run the method
        unique_environments = data_source.unique_environment()
        assert isinstance(unique_environments, list)
        assert len(unique_environments) == scenario["unique_environment"]


def test_has_environment(scenarios):
    """Test the has_environment method."""
    for scenario in scenarios:
        data_source = scenario["data_source"]
        data_source._data = scenario["response"].json()
        data_source._geometry = scenario["geometry"]
        assert data_source.has_environment() == scenario["has_environment"]


def test_convert_data(scenarios, empty_environment_data_model):
    """Test the convert_data method.

    Configure the data_source and convert the raw HTTP response into the data
    model of the Environment class. The properties of the data model are a
    little different for each data_source.
    """
    for scenario in scenarios:

        # Configure and run
        data_source = scenario["data_source"]
        data_source._data = scenario["response"].json()
        data_source._geometry = scenario["geometry"]
        result = data_source.convert_data()

        # Test the returned data
        if len(result) > 0:
            for item in result:
                # Top level keys
                assert item._data.keys() == empty_environment_data_model.keys()
                # dataSource keys and values
                assert item._data["dataSource"]["identifier"] == scenario["identifier"]
                assert (
                    item._data["dataSource"]["name"] == data_source.__class__.__name__
                )
                # dateCreated key and value
                assert item._data["dateCreated"] is not None
                # properties keys and values
                for key, value in item._data["properties"].items():
                    assert key in item._data["properties"].keys()
                    assert item._data["properties"][key] is not None
                # mappedProperties are not yet populated
                assert isinstance(item._data["mappedProperties"], list)
                assert len(item._data["mappedProperties"]) == 0
        else:
            assert result == []


def test_geometry(scenarios):
    for scenario in scenarios:
        # Get
        data_source = scenario["data_source"]
        assert data_source.geometry is None
        # Set
        data_source.geometry = scenario["geometry"]
        assert data_source.geometry == scenario["geometry"]


def test_data(scenarios):
    for scenario in scenarios:
        # Get
        data_source = scenario["data_source"]
        assert data_source.data is None
        # Set
        data_source.data = scenario["response"]
        assert data_source.data == scenario["response"]


def test_env_properties(scenarios):
    for scenario in scenarios:
        # Get
        data_source = scenario["data_source"]
        assert data_source.env_properties is not None
        # Set
        default_value = data_source.env_properties
        data_source.env_properties = {"test": "test"}
        assert data_source.env_properties != default_value
