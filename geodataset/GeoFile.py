from pathlib import Path

import fiona
import numpy as np
from affine import Affine
from shapely.affinity import affine_transform
from shapely.geometry import Polygon, shape
from shapely.geometry import box

"""
Clipping polygons
https://hatarilabs.com/ih-en/how-to-clip-polygon-layers-with-python-fiona-and-shapely-tutorial
"""


class GeoShpFile:

    def __init__(self, path: Path, transform: Affine):
        assert path.is_dir()
        assert type(transform) == Affine

        # https://gis.stackexchange.com/questions/380357/affine-tranformation-matrix-shapely-asks-6-coefficients-but-rasterio-delivers
        self.transform = [element for array in transform.column_vectors for element in array]
        self.shp_file = fiona.open(path)

    def save_clip(self, window: tuple[int, int, int, int], saving_folder: Path) -> None:
        x, y, w, h = window
        window_box: Polygon = box(x, y, x + w, y + h)
        window_geo = affine_transform(window_box, self.transform)

        geopolygons = self.read_geopolygons()

        filtered_polygons = []
        for geopolygon in geopolygons:
            if geopolygon.intersects(window_geo):
                intersection = geopolygon.intersection(window_geo)
                # Intersection could return MultiPolygon - we can split it
                # into polygons, reference:
                # https://stackoverflow.com/questions/55106744/how-do-you-convert-shapely-multipolygon-to-polygon
                if intersection.boundary == 'MultiPolygon':
                    for polygon in intersection.geoms:
                        filtered_polygons.append(polygon)
                else:
                    filtered_polygons.append(intersection)

        # Drawing polygons in shp file, reference:
        # https://hatarilabs.com/ih-en/how-to-create-a-pointlinepolygon-shapefile-with-python-and-fiona-tutorial
        schema = {
            'geometry': 'Polygon',
            'properties': [('Name', "str")]
        }
        print(f"Saving clip: {saving_folder}")
        with fiona.open(
                saving_folder,
                mode='w',
                driver="ESRI Shapefile",
                schema=schema
        ) as file:
            for polygon in filtered_polygons:
                # Intersection could return MultiPolygon - we can split it
                # into polygons, reference:
                # https://stackoverflow.com/questions/55106744/how-do-you-convert-shapely-multipolygon-to-polygon
                if polygon.geom_type == 'MultiPolygon':
                    for poly in polygon.geoms:
                        file.write(self.generate_row_dictionary(poly))
                else:
                    file.write(self.generate_row_dictionary(polygon))

    def read_geopolygons(self) -> list[Polygon]:
        polygons = []

        for el in self.shp_file:
            geopolygon = shape(el['geometry'])
            polygons.append(geopolygon)

        return polygons

    def close(self):
        self.shp_file.close()

    @staticmethod
    def generate_row_dictionary(polygon: Polygon):
        array_polygon = np.array(polygon.exterior.coords)
        row_dict = {
            "geometry": {
                "type": "Polygon",
                'coordinates': [array_polygon]
            },
            'properties': {
                "Name": "segment"
            }
        }
        return row_dict
