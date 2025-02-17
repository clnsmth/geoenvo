"""Test the EcologicalCoastalUnits data source"""

import pytest

from geoenvo.geometry import Geometry
from geoenvo.data_sources import EcologicalCoastalUnits
from tests.conftest import load_geometry


def test_init():
    """Test the DataSource class initialization"""
    data_source = EcologicalCoastalUnits()
    assert data_source._buffer is None


def test_resolve_with_buffer(use_mock):

    if use_mock:
        pytest.skip("Skipping test when use_mock is False")

    data_source = EcologicalCoastalUnits()
    geometry = Geometry(load_geometry("point_on_land_expands_to_coast"))

    # Normally polygon_on_land_and_ocean geometry doesn't resolve to anything
    # because the polygon centroid is over the ocean.
    result = data_source.resolve(geometry)
    assert result == []

    # However, when the grid size is set, the polygon is converted to a series
    # of points that are then resolvable to the WorldTerrestrialEcosystems
    # data source.
    data_source._buffer = 0.5
    result = data_source.resolve(geometry)
    assert len(result) == 1


def test_buffer(scenarios):
    for scenario in scenarios:
        if scenario.get("data_source") == EcologicalCoastalUnits():
            # Get
            data_source = scenario["data_source"]
            assert data_source.buffer is None
            # Set
            buffer = 0.5
            data_source.buffer = buffer
            assert data_source.buffer == buffer
