import WSI_api
import logging


# BaseTransform is a base class for the various tile transforms
class BaseTransform:
    def __init__(self, wsi, level, row, column, lock):
        self.__wsi = wsi
        self.__level = level
        self.__row = row
        self.__column = column
        self.__lock = lock

    def do_transform(self, tile_data):
        """
        Transform and analyze an already loaded tile
        :param tile_data: the loaded tile
        :return: a tuple of the changed data and an indication boolean
        """
        # To be implemented by the subclasses
        raise NotImplementedError("Must override doTransform")

    def transform(self):
        """
         The transform method reads a tile, performs some changes on it and analyzes it
        :return: a boolean specifying is an indication was found on the tile
        """
        try:
            if self.__lock:
                self.__lock.acquire()
            tile = WSI_api.read_tile(self.__wsi, self.__level, self.__row, self.__column)
            transformed_tile, indication_found = self.do_transform(tile)
            # in a real scenario we may want to write/save this transformation, skipping this for now
            return indication_found

        except MemoryError as ex:
            logging.error("Out of Memory")
            return None
        finally:
            if self.__lock:
                self.__lock.release()
