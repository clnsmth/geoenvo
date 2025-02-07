"""Test the resolvers modules"""


def test_resolver_init(resolvers):
    """Test the Resolver class initialization"""
    for resolver in resolvers:
        assert resolver._geometry is None
        assert resolver._data is None
        assert len(resolver._env_attributes) > 0


def test_resolver_attributes(scenarios):
    """Test that the Resolver instance classes have the expected attributes"""
    for scenario in scenarios:
        attributes = scenario.get("resolvers")._env_attributes
        expected_attributes = scenario.get("raw_attributes")
        assert all([key in expected_attributes for key in attributes.keys()])


def test_get_unique_ecosystems(scenarios):
    """Test the get_unique_ecosystems method.

    The get_unique_ecosystems method should return a set of unique ecosystems
    contained in a given server response object. The way ecosystems are
    expressed by each server (in JSON format) differs, so the function should
    be capable of recognizing the format and parsing it accordingly. The set
    object returned by the get_unique_ecosystems method enables iterative
    parsing of the contents by the builder routine of the get_wte_ecosystems
    and get_ecu_ecosystems methods of the Response object. Note, currently,
    the identify operation used to query the WTE server does not return more
    than one ecosystem per query.
    """
    for scenario in scenarios:
        # Configure the resolver
        resolver = scenario["resolvers"]
        resolver._data = scenario["response"].json()
        resolver._geometry = scenario["geometry"]

        # Run the method
        unique_environments = resolver.unique_environment()
        assert isinstance(unique_environments, list)
        assert len(unique_environments) == scenario["unique_environment"]


def test_has_ecosystem(scenarios):
    """Test the has_ecosystem method."""
    for scenario in scenarios:
        resolver = scenario["resolvers"]
        resolver._data = scenario["response"].json()
        resolver._geometry = scenario["geometry"]
        assert resolver.has_ecosystem() == scenario["has_ecosystem"]


def test_convert_data(scenarios, empty_environment_data_model):
    """Test the convert_data method.

    Configure the resolver and convert the raw HTTP response into the data
    model of the Environment class. The properties of the data model are a
    little different for each resolver.
    """
    for scenario in scenarios:

        # Configure and run
        resolver = scenario["resolvers"]
        resolver._data = scenario["response"].json()
        resolver._geometry = scenario["geometry"]
        result = resolver.convert_data()

        # Test the returned data
        if len(result) > 0:
            for item in result:
                # Top level keys
                assert item._data.keys() == empty_environment_data_model.keys()
                # dataSource keys and values
                assert item._data["dataSource"]["identifier"] == scenario["identifier"]
                assert (
                    item._data["dataSource"]["resolver"] == resolver.__class__.__name__
                )
                # dateCreated key and value
                assert item._data["dateCreated"] is not None
                # properties keys and values
                for key, value in item._data["properties"].items():
                    assert key in item._data["properties"].keys()
                    assert item._data["properties"][key] is not None
                # envoTerms are not yet populated
                assert isinstance(item._data["envoTerms"], list)
                assert len(item._data["envoTerms"]) == 0
        else:
            assert result == []
