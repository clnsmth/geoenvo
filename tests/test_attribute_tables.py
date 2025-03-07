"""Test the data source attribute tables"""

import pytest
from importlib.resources import files
from geoenvo.data_sources.world_terrestrial_ecosystems import write_raster_attribute_table


def test_attribute_tables(use_mock, tmp_path):
    """Test the attribute table of data sources. These need to be checked
    against the real data source to ensure that the attribute tables are
    up-to-date.
    """
    if use_mock:
        pytest.skip("Skipping test when use_mock is False")

    # Get attribute table from the data source and compare against the local
    # copy.
    write_raster_attribute_table(output_directory=tmp_path)
    for file in tmp_path.iterdir():
        with open(file, "r", encoding="utf-8") as f:
            print(file.name)
            content = f.read()
            with open(files("src.geoenvo.data.data_source_attributes").joinpath("WTE_raster_attribute_table.json"), "r", encoding="utf-8") as meow:
                fixture_content = meow.read()
                assert content == fixture_content
