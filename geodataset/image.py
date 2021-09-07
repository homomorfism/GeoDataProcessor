import logging
import sys
from pathlib import Path
from rasterio.windows import Window

import rasterio

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class GeoImage:
    def __init__(self, image_path: Path):
        assert image_path.is_file()
        self.image = image_path
        self.logger = logging.getLogger()

    @property
    def shape(self):
        """
        :return: (channels, height, width) of image
        """
        with rasterio.open(self.image) as file:
            return file.read().shape

    def save_crop(self, x: int, y: int, h: int, w: int, saving_path: Path):
        if saving_path.is_file():
            self.logger.info(f"Removing {str(saving_path)}...")
            saving_path.unlink()

        with rasterio.open(self.image) as src:
            window = Window(x, y, h, w)
            transform = src.window_transform(window)

            profile = src.profile
            profile.update({
                "height": h,
                'width': w,
                'transform': transform
            })

            with rasterio.open(saving_path, 'w', **profile) as dst:
                crop = src.read(window=window)
                dst.write(crop)


if __name__ == '__main__':
    image_path = Path("/home/shamil/PycharmProjects/GeoDataset/tests/dataset/images/"
                      "4326_cheremshan_16-30-27-(191-i)_cofp.tif")
    saving_path = Path("/home/shamil/PycharmProjects/GeoDataset/tests/dataset/0.tif")
    image = GeoImage(image_path)
    image.save_crop(5502, 3556, 256, 256, saving_path=saving_path)

