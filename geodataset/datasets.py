import os
from pathlib import Path
from typing import Union

import numpy as np
import slidingwindow as sw
from rasterio.transform import guard_transform

from geodataset.GeoFile import GeoShpFile
from geodataset.fileutils.parse_directory import filter_files, get_parents_folder, create_empty_folder
from geodataset.image import GeoImage

AnyPath = Union[Path, str, os.PathLike]


class GeoImageDataset:
    """Image data class"""

    def __init__(self,
                 image_dataset: AnyPath,
                 shp_dataset: AnyPath,
                 supported_image_formats=('.tiff', '.tif',),
                 supported_gt_formats=('.shp',)
                 ):

        image_dataset, shp_dataset = Path(image_dataset), Path(shp_dataset)
        self.images: list[Path] = filter_files(folder=image_dataset, supported_formats=supported_image_formats)
        self.shp_dataset: list[Path] = get_parents_folder(folder=shp_dataset, supported_formats=supported_gt_formats)
        self.check_consistency()

    def check_consistency(self):
        """Check that shp dataset consists from folders and name of folders matches with image names"""
        pass

    def __len__(self):
        return len(self.images)

    def clip_dataset(self, clip_size: int, output_directory: Path):
        counter = 0

        if not output_directory.is_dir():
            output_directory.mkdir()

        image_crop_path = output_directory / "images"
        shp_crop_path = output_directory / "labels"

        create_empty_folder(image_crop_path)
        create_empty_folder(shp_crop_path)

        iter_list = enumerate(zip(sorted(self.images), sorted(self.shp_dataset)))
        for ii, (image_path, shp_path) in iter_list:
            image_name = image_path.stem
            image = GeoImage(image_path)
            transform = guard_transform(image.get_transform())
            shp_file = GeoShpFile(shp_path, transform=transform)

            windows = sw.generate(data=np.empty(shape=image.shape()),
                                  dimOrder=sw.DimOrder.ChannelHeightWidth,
                                  maxWindowSize=clip_size,
                                  overlapPercent=0.0)

            for window in windows:
                image_clip_path = image_crop_path / f"{image_name}_clip={counter}.tif"
                shp_clip_path = shp_crop_path / f"{image_name}_clip={counter}"  # A folder with clipped .shp/.prj files
                box = window.getRect()
                image.save_crop(box, saving_path=image_clip_path)
                shp_file.save_clip(box, saving_folder=shp_clip_path)

                counter += 1
