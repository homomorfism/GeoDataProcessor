from typing import Union

from affine import Affine
from rasterio.windows import Window
from shapely.geometry import Polygon, box

"""
https://shapely.readthedocs.io/en/stable/manual.html
https://pypi.org/project/affine/
"""


class GeoTransform:
    def __init__(self, transform: Affine):
        assert isinstance(transform, Affine), f"{type(transform)}"
        self.transform: Affine = transform

    def get_geo_window_polygon(self, pixel_window: tuple[float, float, float, float]) -> Polygon:
        x, y, w, h = pixel_window

        left_down_corner = x, y
        top_right_corner = x + w, y + h

        bottom_left_corner = self.transform * left_down_corner
        top_right_corner = self.transform * top_right_corner

        return box(*bottom_left_corner, *top_right_corner)

    def geo2pixel_polygon(self, geopolygon: Polygon):
        pixel_coords = [~self.transform * coord for coord in geopolygon.exterior.coords]
        return Polygon(pixel_coords)

    def pixel2geo_polygon(self, polygon: Polygon):
        pixel_coords = [self.transform * coord for coord in polygon.exterior.coords]
        return Polygon(pixel_coords)


def window2polygon(window: Union[Window, tuple]) -> Polygon:
    x, y, w, h = window

    bottom_left_corner = x, y
    top_right_corner = x + w, y + h

    return box(*bottom_left_corner, *top_right_corner)
