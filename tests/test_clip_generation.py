import unittest
from pathlib import Path

from geodataset.image import GeoImage


class TestClipGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.image_path = Path("dataset/images/image1.tif")
        self.saving_path = Path('outputs/1.tif')
        self.window = (0, 0, 2000, 2000)

    def test_clip_generation(self):
        image = GeoImage(self.image_path)
        image.save_crop(window=self.window, saving_path=self.saving_path)

        self.assertTrue(self.saving_path.is_file())
        image.close()

    # def tearDown(self) -> None:
    #     if self.saving_path.is_file():
    #         rasterio.shutil.delete(self.saving_path)
