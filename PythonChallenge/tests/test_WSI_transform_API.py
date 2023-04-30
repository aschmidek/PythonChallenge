import logging
import unittest
from unittest.mock import patch
from WSI_transform_API import WSITransformAPIError, WSITransformAPI

WSI_PATH = r"C:\Users\User\Desktop\MyProjects\PythonChallenge\AF0177-21-HE-13__20210623_130738.tiff"


logging.getLogger().setLevel(logging.ERROR)


# A Test class to measure the performance of the WSI_transform_API
# Currently covers testing of the public methods
# I would also add some Mocked tests for the logic of the private methods
# but did not cover those.
class TestWSITransformAPI(unittest.TestCase):

    def test_transform_none_existing_file(self):
        with self.assertRaises(WSITransformAPIError):
            WSITransformAPI().transform("no_such_path", "genericTissue", 1, None)

    def test_transform_level_0(self):
        result = WSITransformAPI().transform(WSI_PATH, "genericTissue", 0, None)
        self.assertEqual(result, 30096)

    @patch('WSI_transform_API.TILE_SIZE', 1500)
    def test_transform_level_0_tile_size_1500(self):
        result = WSITransformAPI().transform(WSI_PATH, "genericTissue", 0, None)
        self.assertEqual(result, 3588)

    def test_transform_timeout_reached(self):
        with self.assertRaises(WSITransformAPIError):
            WSITransformAPI().transform(WSI_PATH, "genericTissue", 0, 1)

    def test_handle_results_full(self):
        input_iterator = [True, False, True].__iter__()
        result = WSITransformAPI().handle_results(input_iterator)
        self.assertEqual(result, 3)

    def test_handle_results_empty(self):
        result = WSITransformAPI().handle_results([].__iter__())
        self.assertEqual(result, 0)

    def test_handle_results_none(self):
        with self.assertRaises(WSITransformAPIError):
            WSITransformAPI().handle_results(None)


if __name__ == '__main__':
    unittest.main()