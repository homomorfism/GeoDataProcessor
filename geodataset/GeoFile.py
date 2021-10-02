import logging
import sys
from pathlib import Path

import fiona
import numpy as np
from affine import Affine
from shapely.affinity import affine_transform
from shapely.errors import TopologicalError
from shapely.geometry import Polygon, shape
from shapely.geometry import box

logging.basicConfig(stream=sys.stdout, format="[GeoShpFile] %(message)s")


class GeoShpFile:

    def __init__(self, path: Path, transform: Affine):
        assert path.is_dir()
        assert type(transform) == Affine

        # https://gis.stackexchange.com/questions/380357/affine-tranformation-matrix-shapely-asks-6-coefficients-but-rasterio-delivers
        self.transform = [element for array in transform.column_vectors for element in array]
        self.shp_file = fiona.open(path)
        self.logger = logging.getLogger()

    def save_clip(self, window: tuple[int, int, int, int], saving_folder: Path) -> None:
        x, y, w, h = window
        window_box: Polygon = box(x, y, x + w, y + h)
        window_geo = affine_transform(window_box, self.transform)

        geopolygons = self.read_geopolygons()

        filtered_polygons = []
        for geopolygon in geopolygons:
            if geopolygon.intersects(window_geo):
                try:
                    intersection = geopolygon.intersection(window_geo)
                except TopologicalError:
                    self.logger.info("topological error, skipping...")
                    continue

                geom_type = intersection.geom_type
                assert geom_type in ['Polygon', 'MultiPolygon', 'GeometryCollection', 'LineString']

                if geom_type == 'Polygon':
                    filtered_polygons.append(intersection)

                elif geom_type == 'MultiPolygon':
                    for polygon in intersection.geoms:
                        filtered_polygons.append(polygon)

                elif geom_type == 'GeometryCollection':
                    for obj in intersection.geoms:
                        if obj.geom_type == 'Polygon':
                            filtered_polygons.append(obj)

                elif geom_type == 'LineString':
                    pass

                else:
                    self.logger.info(f"Geometry: {geom_type} is not supported! Skipping...")

        # Converting polygons into shp file
        schema = {
            'geometry': 'Polygon',
            'properties': [('Name', "str")]
        }
        with fiona.open(
                saving_folder,
                mode='w',
                driver="ESRI Shapefile",
                schema=schema
        ) as file:
            for polygon in filtered_polygons:
                assert polygon.geom_type != 'MultiPolygon'
                if polygon.geom_type == 'GeometryCollection':
                    for obj in polygon.geoms:
                        print(obj)
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
