Basic geo large images to coco clipped coco dataset

Example of usage:

```python

from geodataset.datasets import GeoImageDataset
from pathlib import Path
import json

dataset = GeoImageDataset(image_dataset="images", shp_dataset="labels")
clipped_dataset = dataset.clip_dataset(clip_size=512, output_directory="clipped") # Here would be stored image and shp clips (coordinate systems are preserved)
coco_json = clipped_dataset.generate_coco()

with open("coco_annotations.json") as file:
    file.write(json.dumps(coco_json))


```


