"""Test the environment module."""

from geoenvo.environment import Environment

from tests.conftest import load_response


def test_environment_init():
    """Test Environment class initialization has the expected attributes."""
    environment = Environment()
    assert isinstance(environment.data, dict)
    assert len(environment.data) == 0


def test_data():
    geometry = Environment({"type": "Environment"})
    # Get
    assert geometry.data is not None
    # Set
    default_value = geometry.data
    geometry.data = {"type": "Different Environment"}
    assert geometry.data != default_value