import logging
import WSI_api
from concurrent.futures import ThreadPoolExecutor
from openslide import OpenSlideUnsupportedFormatError
from transform_sequence_factory import TransformSequenceFactory

THREAD_COUNT = 25
TILE_SIZE = 512


# The primary class for executing the transform logic

class WSITransformAPI:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self):
        logging.info("THREAD_COUNT: %d", THREAD_COUNT)
        self.__thread_pool = ThreadPoolExecutor(THREAD_COUNT)

    def transform(self, image_path, image_type, level, timeout):
        """
        The transform method runs all transformations of all tiles and returns
        consolidated data
        :param image_path: The tff file path of the whole slide image
        :param image_type: A string representing what type of image is to be transformed
        :param level: The wsi level to transform
        :param timeout: how long to wait for all transformations to finish
        :return: currently returns the count of results from the various transformations
        """
        try:
            wsi = WSI_api.open_wsi(image_path)
            logging.info("TILE_SIZE: %d", TILE_SIZE)
            horizontal_tile_count, vertical_tile_count = WSI_api.get_tile_count(wsi, TILE_SIZE)
            transforms = self.__create_transforms(image_type, wsi, level,
                                                  horizontal_tile_count, vertical_tile_count)
            results = self.__execute_transforms(transforms, timeout)
            return WSITransformAPI.handle_results(results)

        except OpenSlideUnsupportedFormatError:
            logging.error("Could not open slide image")
            raise WSITransformAPIError("Could not open slide image")

        except TimeoutError:
            logging.error("Timeout reached")
            raise WSITransformAPIError("Timeout reached")

    @staticmethod
    def __create_transforms(image_type, wsi, level,
                            horizontal_tile_count, vertical_tile_count):
        # Create all transforms for this wsi, while consulting with the TransformSequenceFactory
        all_wsi_transforms = []
        for i in range(0, horizontal_tile_count):
            for j in range(0, vertical_tile_count):
                transform_sequence = TransformSequenceFactory().get_transform_sequence(image_type, wsi, level, i, j)
                for transform in transform_sequence:
                    all_wsi_transforms.append(transform)
        logging.info("Transform Count is: %d", len(all_wsi_transforms))
        return all_wsi_transforms

    def __execute_transforms(self, transforms, timeout):
        # Execute transformation asynchronously while using the thread pool
        return self.__thread_pool.map(lambda t: t.transform(), transforms,
                                      timeout=timeout)

    @staticmethod
    def handle_results(results):
        """
        The handle_results method consolidates all tile transform results to one result
        :param results: transform results iterator
        :return: currently returns the number of results
        """
        try:
            result_count = len(list(results))
            logging.info("Number of results: %d", result_count)
            return result_count
        except TypeError:
            logging.error("Unexpected transformation results")
            raise WSITransformAPIError("Unexpected transformation results")


class WSITransformAPIError(Exception):
    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    WSITransformAPI().transform(
        r"C:\Users\User\Desktop\MyProjects\PythonChallenge\AF0177-21-HE-13__20210623_130738.tiff", "GeneralType", 0,
        None)
