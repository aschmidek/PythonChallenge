import ctypes.util
import math
import os
import numpy as np
import time

dll_path = ctypes.util.find_library("libopenslide-0.dll")
_dll_directory, _ = os.path.split(os.path.abspath(dll_path))

with os.add_dll_directory(_dll_directory):
    import openslide


def open_wsi(path):
    return openslide.OpenSlide(path)


def get_max_level(im):
    return im.level_count - 1  # return maximal level, level 0 is base level (full res), level 1 is half res, etc.


def get_dimensions(im):
    return im.dimensions  # <width, height> tuple for level 0


def read_region(im, level, row, col, num_rows, num_cols):
    region = np.asarray(im.read_region((col, row), level, (num_cols, num_rows)))
    return region[:, :, :3]


# level is the requested level - 0 is base (full res)
# tile_row is the 0-based index of the tile row
def read_tile(im, level, tile_row, tile_col, tile_size=512):
    row = tile_row * tile_size
    col = tile_col * tile_size
    return read_region(im, level, row, col, tile_size, tile_size)


# process_data method is a place-holder for a processing function that will be implemented
def process_data(data):
    sz = data.shape
    time.sleep(sz[0] * sz[1] / 100000)
    return data[:, ::-1, 1]


def get_tile_count(im, tile_size):
    h_dimension, v_dimension = get_dimensions(im)
    horizontal_tile_count = math.ceil(h_dimension / tile_size)
    vertical_tile_count = math.ceil(v_dimension / tile_size)
    return horizontal_tile_count, vertical_tile_count


if __name__ == '__main__':
    wsi = open_wsi(r"C:\Users\User\Desktop\MyProjects\PythonChallange\AF0177-21-HE-13__20210623_130738.tiff")
    width, height = get_dimensions(wsi)
    print('max level is', get_max_level(wsi), ', width=', width, ', height=', height)
    t0 = time.time()
    reg = read_tile(wsi, 0, 10, 20)
    reg = process_data(reg)
    print('Tile shape is:', reg.shape)
    print('overall time to read and process tile:', time.time() - t0)
    t1 = time.time()
    reg = read_region(wsi, 2, 75000, 75000, 4, 7)
    reg = process_data(reg)
    print('region size is', reg.shape, '\n', 'Pixels:\n', reg)
    print('overall time to read and process region:', time.time() - t1)
