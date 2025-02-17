"""The geometry module"""

import json
from io import StringIO, BytesIO
from json import loads, dumps
import geopandas as gpd
from shapely import Polygon, Point
import numpy as np


class Geometry:
    def __init__(self, geometry: dict):
        self._data = geometry

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, geometry: dict):
        self._data = geometry

    def is_supported(self) -> bool:
        # If self.data is a GeoJSON object with the top level "type" property
        # having a value of "Point" or "Polygon", then it is valid.
        if self.data.get("type") in ["Point", "Polygon"]:
            return True
        return False

    def to_esri(self) -> dict:
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

    def geometry_type(self) -> str:  # TODO deprecate in favor of self.data.get('type')
        return self.data.get("type")

    def point_to_polygon(self, buffer=None):

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

    def polygon_to_points(self, grid_size):
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


def grid_sample_polygon(polygon, grid_size):
    """
    Generates a set of representative points within a polygon using grid-based sampling.

    Args:
        polygon: A Shapely Polygon object.
        grid_size: The size of the grid cells in the same units as the polygon's coordinates.

    Returns:
        A GeoSeries of Shapely Point objects representing the sample points.
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
