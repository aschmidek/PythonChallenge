import time
import numpy
import logging
import random
from transforms.base_transform import BaseTransform


# TransformB is an example transform
class TransformB(BaseTransform):

    def do_transform(self, tile_data):
        logging.debug("B")
        time.sleep(0.001)
        return numpy.ones(tile_data.shape), random.choice([True, False])
