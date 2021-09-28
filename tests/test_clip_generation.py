import unittest
from pathlib import Path

import temppathlib

from geodataset.datasets import GeoImageDataset


class TestClipGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.image_path = Path("tests/test_data/images")
        self.shp_dataset = Path('tests/test_data/labels')
        self.clip_size = 100

    def test_clip_generation(self):
        with temppathlib.TemporaryDirectory() as saving_folder:
            dataset = GeoImageDataset(image_dataset=self.image_path,
                                      shp_dataset=self.shp_dataset)

            dataset.clip_dataset(clip_size=self.clip_size,
                                 output_directory=saving_folder.path)

            clip_image_folder = saving_folder.path / 'images'
            clip_shp_folder = saving_folder.path / 'labels'

            # self.assertEqual(len(list(clip_image_folder.glob("*"))), 12)
            # self.assertEqual(len(list(clip_shp_folder.glob("*"))), 12)
