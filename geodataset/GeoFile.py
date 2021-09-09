from pathlib import Path

import fiona
from shapely.geometry import Polygon, shape

"""
Clipping polygons
https://hatarilabs.com/ih-en/how-to-clip-polygon-layers-with-python-fiona-and-shapely-tutorial
"""


class GeoShpFile:

    def __init__(self, path: Path):
        assert path.is_file()

        self.shp_file = fiona.open(path)

    def get_pixel_polygons(self, window: tuple[int, int, int, int]) -> list[Polygon]:
        x, y, h, w = window

        for el in self.shp_file:
            geopolygon = shape(el['geometry'])
            # TODO(Convert geo coordinates to pixels)

        pass
