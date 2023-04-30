import numpy
import random
import logging

from transforms.base_transform import BaseTransform
import time


# TransformA is an example transform
class TransformA(BaseTransform):

    def do_transform(self, tile_data):
        logging.debug("A")
        time.sleep(0.01)
        return numpy.zeros(tile_data.shape), random.choice([True, False])
