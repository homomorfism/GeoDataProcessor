import shutil
import unittest
from pathlib import Path

from geodataset.datasets import GeoImageDataset


class TestClipGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.image_path = Path("examples/data/images")
        self.shp_dataset = Path('examples/data/labels')
        self.saving_folder = Path("examples/cleaned")
        print(f"Saving folder: {self.saving_folder.resolve()}")
        self.clip_size = 256

        if not self.saving_folder.is_dir():
            self.saving_folder.mkdir()

    def test_clip_generation(self):

        dataset = GeoImageDataset(image_dataset=self.image_path,
                                  shp_dataset=self.shp_dataset)

        dataset.clip_dataset(clip_size=self.clip_size,
                             output_directory=self.saving_folder)

        clip_image_folder = self.saving_folder / 'images'
        clip_shp_folder = self.saving_folder / 'labels'

        self.assertEqual(len(list(clip_image_folder.glob("**/*"))), 713)
        self.assertEqual(len(list(clip_shp_folder.glob("*"))), 713)

    def tearDown(self) -> None:
        if self.saving_folder.is_dir():
            shutil.rmtree(self.saving_folder)
