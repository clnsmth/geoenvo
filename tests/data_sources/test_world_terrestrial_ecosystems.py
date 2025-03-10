"""Test the WorldTerrestrialEcosystems data source"""

from importlib.resources import files
import pytest
from tests.conftest import load_geometry
from geoenvo.geometry import Geometry
from geoenvo.data_sources import WorldTerrestrialEcosystems
from geoenvo.data_sources.world_terrestrial_ecosystems import create_attribute_table


def test_init():
    """Test the DataSource class initialization"""
    data_source = WorldTerrestrialEcosystems()
    assert data_source.grid_size is None


def test_get_environment_with_grid_size(use_mock):
    """Test the get_environment method with grid_size set"""

    if use_mock:
        pytest.skip("Skipping test when use_mock is False")

    data_source = WorldTerrestrialEcosystems()
    geometry = Geometry(load_geometry("polygon_on_land_and_ocean"))

    # Normally polygon_on_land_and_ocean geometry doesn't get_environment to
    # anything because the polygon centroid is over the ocean.
    result = data_source.get_environment(geometry)
    assert not result

    # However, when the grid size is set, the polygon is converted to a series
    # of points that are then resolvable to the WorldTerrestrialEcosystems
    # data source.
    data_source.grid_size = 0.5
    result = data_source.get_environment(geometry)
    assert len(result) == 1


def test_grid_size(scenarios):
    """Test the grid_size attribute of the WorldTerrestrialEcosystems data
    source."""
    for scenario in scenarios:
        if scenario.get("data_source") == WorldTerrestrialEcosystems():
            # Get
            data_source = scenario["data_sources"]
            assert data_source.grid_size is None
            # Set
            grid_size = 0.5
            data_source.grid_size = grid_size
            assert data_source.grid_size == grid_size


def test_attribute_tables(use_mock, tmp_path):
    """Test the attribute table of data sources. These need to be checked
    against the real data source to ensure that the attribute tables are
    up-to-date.
    """
    if use_mock:
        pytest.skip("Skipping test when use_mock is False")

    # Get attribute table from the data source and compare against the local
    # copy.
    create_attribute_table(output_directory=tmp_path)
    for file in tmp_path.iterdir():
        with open(file, "r", encoding="utf-8") as f:
            print(file.name)
            content = f.read()
            with open(
                files("geoenvo.data.data_source_attributes").joinpath(
                    "wte_attribute_table.json"
                ),
                "r",
                encoding="utf-8",
            ) as attribute_table:
                fixture_content = attribute_table.read()
                assert content == fixture_content
