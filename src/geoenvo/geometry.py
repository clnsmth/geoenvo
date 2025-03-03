"""
geometry.py
===========

This module defines the ``Geometry`` class, which manages and processes
spatial geometries. It provides utility methods for verifying geometry types,
transforming between representations, and performing spatial operations such
as buffering and grid-based sampling.

Key functionalities of this module include:

- Managing GeoJSON geometries and their transformations.
- Verifying geometry support for the resolver.
- Converting between GeoJSON and Esri-compatible formats.
- Generating representative points within polygons for spatial sampling.
"""

import json
from io import StringIO
from json import loads, dumps
import geopandas as gpd
import shapely
from shapely import Polygon, Point
import numpy as np


class Geometry:
    """
    The Geometry class manages spatial geometries in GeoJSON format and
    provides utilities for transformation and spatial processing.
    """

    def __init__(self, geometry: dict):
        """
        Initializes a Geometry object with the given GeoJSON geometry.

        :param geometry: A dictionary representing a GeoJSON geometry.
        """
        self._data = geometry

    @property
    def data(self) -> dict:
        """
        Retrieves the stored geometry data.

        :return: A dictionary representing the GeoJSON geometry.
        """
        return self._data

    @data.setter
    def data(self, geometry: dict):
        """
        Updates the geometry data.

        :param geometry: A dictionary representing a new GeoJSON geometry.
        """
        self._data = geometry

    def is_supported(self) -> bool:
        """
        Checks if the stored geometry is supported by the resolver.
        A valid geometry must be a GeoJSON object with a top-level ``type`` of
        either "Point" or "Polygon".

        :return: ``True`` if the geometry is supported, otherwise ``False``.
        """
        if self.data.get("type") in ["Point", "Polygon"]:
            return True
        return False

    def to_esri(self) -> dict:
        """
        Converts the GeoJSON geometry to an Esri-compatible format.

        :return: A dictionary representing the Esri-formatted geometry.
        """
        if self.data["type"] == "Point":
            x, y, *z = self.data["coordinates"]
            geometry = {
                "x": x,
                "y": y,
                "z": z[0] if z else None,
                "spatialReference": {"wkid": 4326},
            }
            geometry_type = "esriGeometryPoint"
            return {"geometry": geometry, "geometryType": geometry_type}
        elif self.data["type"] == "Polygon":
            geometry = {
                "rings": self.data["coordinates"],
                "spatialReference": {"wkid": 4326},
            }
            geometry_type = "esriGeometryPolygon"
            return {"geometry": geometry, "geometryType": geometry_type}
        else:
            raise ValueError("Invalid geometry type")

    def geometry_type(self) -> str:
        """
        Retrieves the type of the stored geometry (e.g., "Point" or "Polygon").

        :return: A string representing the geometry type.
        """
        return self.data.get("type")

    def point_to_polygon(self, buffer=None) -> dict:
        """
        Converts a ``Point`` geometry into a ``Polygon`` by buffering it.

        :param buffer: The buffer distance used to create the polygon
            (optional).
        :return: A dictionary representing the buffered polygon in GeoJSON
            format.
        """
        if self.geometry_type() != "Point" or buffer is None:
            return self.data

        point = gpd.GeoSeries.from_file(StringIO(dumps(self.data)))
        point = point.to_crs(32634)  # A CRS in units of meters
        expanded_point = point.geometry.buffer(buffer * 1000)  # buffer to meters
        expanded_point = expanded_point.to_crs(4326)  # Convert back to EPSG:4326
        bounds = expanded_point.bounds
        polygon = {
            "type": "Polygon",
            "coordinates": [
                [
                    [bounds.minx[0], bounds.miny[0]],
                    [bounds.maxx[0], bounds.miny[0]],
                    [bounds.maxx[0], bounds.maxy[0]],
                    [bounds.minx[0], bounds.maxy[0]],
                    [bounds.minx[0], bounds.miny[0]],
                ]
            ],
        }
        return polygon

    def polygon_to_points(self, grid_size) -> list[dict]:
        """
        Converts a ``Polygon`` geometry into a set of representative points
        using grid-based sampling.

        :param grid_size: The size of the grid cells used for sampling.
        :return: A list of dictionaries representing sampled points in GeoJSON
            format.
        """
        if self.data.get("type") != "Polygon":
            return self.data

        # Get points from within the polygon
        polygon = gpd.GeoSeries.from_file(StringIO(dumps(self.data)))
        representative_points = polygon.apply(grid_sample_polygon, args=(grid_size,))
        points = []
        for item in representative_points.items():
            geojson = json.loads(gpd.GeoSeries(item[1]).to_json())
            result = geojson["features"][0]["geometry"]
            points.append(result)

        # Get points from the vertices of the polygon
        coords = list(polygon[0].exterior.coords)
        polygon_vertices = gpd.GeoSeries([Point(x, y) for x, y in coords])
        polygon_vertices = polygon_vertices.drop_duplicates()
        for item in polygon_vertices.items():
            geojson = json.loads(gpd.GeoSeries(item[1]).to_json())
            result = geojson["features"][0]["geometry"]
            points.append(result)

        return points


def grid_sample_polygon(polygon: shapely.Polygon, grid_size: float) -> gpd.GeoSeries:
    """
    Generates a set of representative points within a polygon using grid-based
    sampling.

    :param polygon: A Shapely Polygon object.
    :param grid_size: The size of the grid cells in the same units as the
        polygon's coordinates.
    :return: A GeoSeries of Shapely Point objects representing the sample
        points.
    """

    min_x, min_y, max_x, max_y = polygon.bounds
    cols = np.arange(min_x, max_x + grid_size, grid_size)
    rows = np.arange(min_y, max_y + grid_size, grid_size)

    grid_cells = []
    for x in cols:
        for y in rows:
            grid_cell = Polygon(
                [
                    (x, y),
                    (x + grid_size, y),
                    (x + grid_size, y + grid_size),
                    (x, y + grid_size),
                ]
            )
            grid_cells.append(grid_cell)

    grid_gdf = gpd.GeoDataFrame(geometry=grid_cells)
    intersecting_cells = grid_gdf[grid_gdf.intersects(polygon)]

    sample_points = intersecting_cells.centroid
    sample_points = sample_points[sample_points.within(polygon)]

    return sample_points
