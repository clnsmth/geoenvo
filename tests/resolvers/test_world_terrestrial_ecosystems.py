"""Test the WorldTerrestrialEcosystems resolver"""

from json import loads

import pytest
from geoenvo.geometry import Geometry
from tests.conftest import load_response, load_geometry
from geoenvo.resolvers.world_terrestrial_ecosystems import WorldTerrestrialEcosystems


def test_init():
    """Test the Resolver class initialization"""
    resolver = WorldTerrestrialEcosystems()
    assert resolver._grid_size is None


def test_resolve_with_grid_size(use_mock):

    if use_mock:
        pytest.skip("Skipping test when use_mock is False")

    resolver = WorldTerrestrialEcosystems()
    geometry = Geometry(load_geometry("polygon_on_land_and_ocean"))

    # Normally polygon_on_land_and_ocean geometry doesn't resolve to anything
    # because the polygon centroid is over the ocean.
    result = resolver.resolve(geometry)
    assert result == []

    # However, when the grid size is set, the polygon is converted to a series
    # of points that are then resolvable to the WorldTerrestrialEcosystems
    # data source.
    resolver._grid_size = 0.5
    result = resolver.resolve(geometry)
    assert len(result) == 1

def test_grid_size(scenarios):
    for scenario in scenarios:
        if scenario.get("resolvers") == WorldTerrestrialEcosystems():
            # Get
            resolver = scenario["resolvers"]
            assert resolver.grid_size is None
            # Set
            grid_size = 0.5
            resolver.grid_size = grid_size
            assert resolver.grid_size == grid_size

