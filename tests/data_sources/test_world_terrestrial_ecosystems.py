"""Test the WorldTerrestrialEcosystems data source"""

from json import loads

import pytest
from geoenvo.geometry import Geometry
from tests.conftest import load_response, load_geometry
from geoenvo.data_sources import WorldTerrestrialEcosystems


def test_init():
    """Test the DataSource class initialization"""
    data_source = WorldTerrestrialEcosystems()
    assert data_source.grid_size is None


def test_resolve_with_grid_size(use_mock):

    if use_mock:
        pytest.skip("Skipping test when use_mock is False")

    data_source = WorldTerrestrialEcosystems()
    geometry = Geometry(load_geometry("polygon_on_land_and_ocean"))

    # Normally polygon_on_land_and_ocean geometry doesn't resolve to anything
    # because the polygon centroid is over the ocean.
    result = data_source.resolve(geometry)
    assert result == []

    # However, when the grid size is set, the polygon is converted to a series
    # of points that are then resolvable to the WorldTerrestrialEcosystems
    # data source.
    data_source.grid_size = 0.5
    result = data_source.resolve(geometry)
    assert len(result) == 1


def test_grid_size(scenarios):
    for scenario in scenarios:
        if scenario.get("data_source") == WorldTerrestrialEcosystems():
            # Get
            data_source = scenario["data_sources"]
            assert data_source.grid_size is None
            # Set
            grid_size = 0.5
            data_source.grid_size = grid_size
            assert data_source.grid_size == grid_size
