import numpy as np
from shapely.geometry import Polygon


def segmentation_to_polygon(segmentation: list[float]) -> Polygon:
    polygon = np.asarray(segmentation).reshape((-1, 2))
    return Polygon(polygon)


def polygon_to_segmentation(polygon: Polygon) -> list[float]:
    np_polygon = np.asarray(polygon.exterior.coords).reshape((-1, 1))
    return np_polygon.tolist()
