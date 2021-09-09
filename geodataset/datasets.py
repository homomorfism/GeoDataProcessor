from pathlib import Path

import slidingwindow as sw

from geodataset.image import GeoImage
from geodataset.io.parse_directory import filter_files


class GeoImageDataset:
    """Image data class"""

    def __init__(self,
                 image_dataset: Path,
                 shp_dataset: Path,
                 supported_image_formats=('.tiff', '.tif',),
                 supported_gt_formats=('.shp',)
                 ):
        self.images: list[Path] = filter_files(folder=image_dataset, supported_formats=supported_image_formats)
        self.shp_dataset: list[Path] = filter_files(folder=shp_dataset, supported_formats=supported_gt_formats)

    def check_consistency(self):
        pass

    def __len__(self):
        return len(self.images)

    def clip_dataset(self, clip_size: int, output_directory: Path):
        counter = 0

        if not output_directory.is_dir():
            output_directory.mkdir()

        crop_path = output_directory / "images"
        crop_path.mkdir(exist_ok=True)

        for ii, (image, shp) in enumerate(zip(sorted(self.images), sorted(self.shp_dataset))):
            image = GeoImage(image)

            windows = sw.generate(data=image,
                                  dimOrder=sw.DimOrder.ChannelHeightWidth,
                                  maxWindowSize=clip_size,
                                  overlapPercent=0.0)

            for window in windows:
                image_path = output_directory / f"{counter}.tif"
                image_name = image_path.name
                x, y, h, w = window.getRect()


if __name__ == '__main__':
    images = Path("/home/shamil/PycharmProjects/GeoDataset/tests/dataset/images")
    shp = Path("/home/shamil/PycharmProjects/GeoDataset/tests/dataset/shp_files")

    dataset = GeoImageDataset(image_dataset=images, shp_dataset=shp)

    dataset.clip_dataset(clip_size=256, output_directory=Path(""))
