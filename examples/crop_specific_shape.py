from pathlib import Path

from geodataset.GeoFile import GeoShpFile
from geodataset.image import GeoImage


def clip_image(image_path, label_path, box):
    image = GeoImage(image_path)
    transform = image.get_transform()
    label = GeoShpFile(label_path, transform)
    image.save_crop(box, saving_path=Path("../tests/test_data/images/image-1024-720.tif"))
    label.save_clip(box, saving_folder=Path("../tests/test_data/labels/shp-1024-720"))


def main():
    image_path = Path("data/images/buildings_train.tif")
    label_path = Path("data/labels/buildings_train")
    box = (0, 0, 1024, 712)

    clip_image(image_path, label_path, box)


if __name__ == '__main__':
    main()
