"""Test the environment module."""

from spinneret.environment import Environment


def test_environment_init():
    """Test Environment class initialization has the expected attributes."""
    environment = Environment()
    assert isinstance(environment.data(), dict)
    assert len(environment.data()) == 0
