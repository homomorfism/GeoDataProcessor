import datetime
import json
import logging
import sys
from pathlib import Path

from shapely.geometry import Polygon

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

    def add_annotation(self, image_id: int, polygons: list[Polygon]):
        pass

    def save_data(self, path: Path):
        assert path.parent.is_dir()

        with open(path, 'w') as file:
            file.write(json.dumps(self.data))

        logging.info(f"Successfully saved file to {str(path)}...")
