from pathlib import Path

from geodataset.datasets import GeoImageDataset


def preprocess(images, labels, tile_size, saving_folder):
    dataset = GeoImageDataset(image_dataset=images,
                              shp_dataset=labels)

    dataset.clip_dataset(tile_size, output_directory=saving_folder)


def main():
    images = Path("data/images")
    labels = Path("data/labels")
    saving_folder = Path("cleaned/")
    saving_folder.mkdir()

    tile_size = 1024
    preprocess(images, labels, tile_size, saving_folder)


if __name__ == '__main__':
    main()
