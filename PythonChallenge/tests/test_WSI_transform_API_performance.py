import logging
import timeit
import unittest
from unittest.mock import patch
from WSI_transform_API import WSITransformAPI

WSI_PATH = r"C:\Users\User\Desktop\MyProjects\PythonChallenge\AF0177-21-HE-13__20210623_130738.tiff"

logging.getLogger().setLevel(logging.INFO)


# A Test class to measure the performance of the WSI_transform_API
class TestWSITransformAPIPerformance(unittest.TestCase):


    @patch('WSI_transform_API.THREAD_COUNT', 10)
    @patch('WSI_transform_API.TILE_SIZE', 512)
    def test_transform_thread_count_10(self):
        self.assertEquals(self.__measure_transform(), 50)

    @patch('WSI_transform_API.THREAD_COUNT', 8)
    @patch('WSI_transform_API.TILE_SIZE', 512)
    def test_transform_thread_count_8(self):
        self.assertEquals(self.__measure_transform(), 50)

    @patch('WSI_transform_API.THREAD_COUNT', 6)
    @patch('WSI_transform_API.TILE_SIZE', 512)
    def test_transform_thread_count_6(self):
        self.assertEquals(self.__measure_transform(), 50)

    @patch('WSI_transform_API.THREAD_COUNT', 4)
    @patch('WSI_transform_API.TILE_SIZE', 512)
    def test_transform_thread_count_4(self):
        self.assertEquals(self.__measure_transform(), 50)

    @patch('WSI_transform_API.THREAD_COUNT', 1)
    @patch('WSI_transform_API.TILE_SIZE', 512)
    def test_transform_thread_count_1(self):
        self.assertEquals(self.__measure_transform(), 50)

    @staticmethod
    def __measure_transform():
        start_time = timeit.default_timer()
        WSITransformAPI().transform(WSI_PATH, "genericTissue", 0, None)
        end_time = timeit.default_timer()
        return end_time-start_time

if __name__ == '__main__':
    unittest.main()