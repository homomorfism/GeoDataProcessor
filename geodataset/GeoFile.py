from pathlib import Path

import fiona
from affine import Affine
from shapely.affinity import affine_transform
from shapely.geometry import Polygon, shape

"""
Clipping polygons
https://hatarilabs.com/ih-en/how-to-clip-polygon-layers-with-python-fiona-and-shapely-tutorial
"""


class GeoShpFile:

    def __init__(self, path: Path, transform: Affine):
        assert path.is_dir()
        assert isinstance(transform, Affine)

        # TODO (fails on next line)
        # Find the way how to extract Affine transform from the image
        self.transform = Affine(transform)
        self.shp_file = fiona.open(path)

        polygon = Polygon([(1, 1), (2, 1), (2, 2)])
        new_polygon = affine_transform(polygon, self.transform)

        print(123)

    def save_clip(self, window: tuple[int, int, int, int], saving_folder: Path) -> None:
        pass

    def get_pixel_polygons(self, pixel_window: tuple[int, int, int, int] = None) -> list[Polygon]:
        polygons = []

        if pixel_window is None:
            for el in self.shp_file:
                geopolygon = shape(el['geometry'])
                pixel_polygon = self.transform.geo2pixel_polygon(geopolygon)
                polygons.append(pixel_polygon)

        else:
            proj_window = self.transform.get_geo_window_polygon(pixel_window)

            for el in self.shp_file:
                geopolygon: Polygon = shape(el['geometry'])
                intersection = geopolygon.intersection(proj_window)

                if intersection.area > 0:
                    pixel_polygon = self.transform.geo2pixel_polygon(intersection)
                    polygons.append(pixel_polygon)

        return polygons

    def close(self):
        self.shp_file.close()
