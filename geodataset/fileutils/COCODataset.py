import datetime
import json
import logging
import sys
from pathlib import Path

from shapely.geometry import Polygon

from geodataset.fileutils.polygons import polygon_to_segmentation

logging.basicConfig(format="[COCODataset] %(message)s", stream=sys.stdout, level=logging.INFO)


class COCODataset:
    def __init__(self, category=1, version="1.0", contributor="", description=""):
        self.logger = logging.getLogger()
        self.data = {

            "info": [
                {
                    "description": description,
                    "url": "",
                    "version": version,
                    "contributor": contributor,
                }
            ],
            "licence": [
                {
                    "id": category,
                    "name": "",
                    "url": ""
                }
            ],
            "categories": [
                {
                    "id": 1,
                    "name": "item",
                    "supercategory": 'items'
                }
            ],
            "images": [],
            "annotations": []
        }

    def add_image(self, image_id: int, file_name: str, height: int, width: int):
        assert image_id != 0

        image_data = {
            "id": image_id,
            "file_name": file_name,
            "width": width,
            "height": height,
            'date_captured': str(datetime.datetime.now()),
            'licence': 1,
            'coco_url': "",
            'flickr_url': ''
        }

        self.data['images'].append(image_data)

    def add_annotation(self, image_id: int, pixel_polygons: list[Polygon]):
        """
        Here we have as input the polygons in pixel coordinates, not geo.
        """

        metadata: dict = list(filter(lambda x: x['id'] == image_id, self.data['images']))[0]
        height, width = metadata['height'], metadata['width']

        for ii, polygon in enumerate(pixel_polygons):
            segm = polygon_to_segmentation(polygon)

            segmentation = {
                'id': ii + 1,
                'image_id': image_id,
                'category_id': 1,
                'iscrown': 0,
                'area': int(polygon.area),
                'bbox': [],
                'segmentation': segm,
                'width': width,
                'height': height,
            }

            self.data['annotations'].append(segmentation)

    def save_data(self, path: Path):
        assert path.parent.is_dir()

        with open(path, 'w') as file:
            file.write(json.dumps(self.data))

        logging.info(f"Successfully saved file to {str(path)}...")
