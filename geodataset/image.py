import logging
import sys
from pathlib import Path

import rasterio
from rasterio.io import DatasetReader
from rasterio.windows import Window

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class GeoImage:
    def __init__(self, image: DatasetReader):
        self.image = image
        self.logger = logging.getLogger()

    @property
    def shape(self):
        """
        :return: (channels, height, width) of image
        """
        return self.image.read().shape

    def save_crop(self, window: tuple[int, int, int, int], saving_path: Path):
        x, y, w, h = window
        projected_window = Window(*window)
        transform = self.image.window_transform(projected_window)

        profile = self.image.profile.copy()
        profile.update({
            "height": h,
            'width': w,
            'transform': transform
        })

        with rasterio.open(saving_path, 'w', **profile) as dst:
            crop = self.image.read(window=projected_window)
            dst.write(crop)
