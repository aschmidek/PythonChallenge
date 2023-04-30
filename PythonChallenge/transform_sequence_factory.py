from multiprocessing import Lock

from transforms.transform_A import TransformA
from transforms.transform_B import TransformB


# The TransformSequenceFactory (a singleton) is in charge of returning the corresponding
# transforms for a given tile according to its wsi_type and level

class TransformSequenceFactory:

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance


    def get_transform_sequence(self, wsi_type, wsi, level, row, column):
        """
        The get_transform_sequence method returns a list of transforms relevant
        to a specific scenario according to the parameters:
        :param wsi_type: The type of the image
        :param wsi: Whole slide image to transform
        :param level: The wsi level
        :param row: The tile row
        :param column: The tile column
        :return: a list of BaseTransform objects
        """

        # creating a lock to be passed to the relevant transforms, in case they need to change the tile
        # or wait for a tile change
        lock = Lock()

        # In a real scenario will consult with an external mapping to determine which transforms
        # to return for the specific scenario
        return [TransformA(wsi, level, row, column, lock),
                TransformB(wsi, level, row, column, lock)]
