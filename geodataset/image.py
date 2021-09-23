import logging
import sys
from pathlib import Path

import rasterio
from affine import Affine
from rasterio.windows import Window

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class GeoImage:
    def __init__(self, image_path: Path):
        self.image = rasterio.open(image_path)
        self.affine_transform = self.image.transform
        self.logger = logging.getLogger()

    def shape(self):
        """
        :return: (channels, height, width) of image
        """
        return self.image.read().shape

    def save_crop(self, window: tuple[int, int, int, int], saving_path: Path):
        x, y, w, h = window
        rasterio_window = Window(*window)
        transform = self.image.window_transform(rasterio_window)

        profile = self.image.profile.copy()
        profile.update({
            "height": h,
            'width': w,
            'transform': transform
        })

        with rasterio.open(saving_path, 'w', **profile) as dst:
            crop = self.image.read(window=rasterio_window)
            dst.write(crop)

    def get_transform(self) -> Affine:
        return self.image.transform

    def close(self):
        self.image.close()
