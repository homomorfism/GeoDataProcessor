Basic geo large images to coco clipped coco dataset

Feature(bug):

- clipping is made with overlap due to output fix size tiles

```python
import numpy as np
import slidingwindow as sw

a = np.zeros(shape=(1, 512, 713))
sw.generate(data=a, dimOrder=sw.DimOrder.ChannelHeightWidth, maxWindowSize=512, overlapPercent=0)
# Returns: [(0,0,512,512), (201,0,512,512)]
```