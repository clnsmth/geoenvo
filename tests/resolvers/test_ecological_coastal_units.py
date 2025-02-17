"""Test the EcologicalCoastalUnits resolver"""

import pytest

from geoenvo.geometry import Geometry
from geoenvo.resolvers import EcologicalCoastalUnits
from tests.conftest import load_geometry


def test_init():
    """Test the Resolver class initialization"""
    resolver = EcologicalCoastalUnits()
    assert resolver._buffer is None


def test_resolve_with_buffer(use_mock):

    if use_mock:
        pytest.skip("Skipping test when use_mock is False")

    resolver = EcologicalCoastalUnits()
    geometry = Geometry(load_geometry("point_on_land_expands_to_coast"))

    # Normally polygon_on_land_and_ocean geometry doesn't resolve to anything
    # because the polygon centroid is over the ocean.
    result = resolver.resolve(geometry)
    assert result == []

    # However, when the grid size is set, the polygon is converted to a series
    # of points that are then resolvable to the WorldTerrestrialEcosystems
    # data source.
    resolver._buffer = 0.5
    result = resolver.resolve(geometry)
    assert len(result) == 1


def test_buffer(scenarios):
    for scenario in scenarios:
        if scenario.get("resolvers") == EcologicalCoastalUnits():
            # Get
            resolver = scenario["resolvers"]
            assert resolver.buffer is None
            # Set
            buffer = 0.5
            resolver.buffer = buffer
            assert resolver.buffer == buffer
