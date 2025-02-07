"""Test the EcologicalCoastalUnits resolver"""

import pytest

from spinneret.geometry import Geometry
from spinneret.resolvers.ecological_coastal_units import EcologicalCoastalUnits
from tests.conftest import load_geometry


def test_init():
    """Test the Resolver class initialization"""
    resolver = EcologicalCoastalUnits()
    assert resolver._buffer is None


def test_resolve_with_buffer(use_mock, mocker):

    # if use_mock:
    #     pytest.skip("Skipping test when use_mock is False")

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
