from pathlib import Path

from shapely.geometry import Polygon

"""
Clipping polygons
https://hatarilabs.com/ih-en/how-to-clip-polygon-layers-with-python-fiona-and-shapely-tutorial
"""


class GeoShpFile:

    def __init__(self, shp_file: Path):
        assert shp_file.is_file()

        self.shp_file = shp_file

    def clip_polygons(self, x, y, h, w) -> list[Polygon]:
        pass
