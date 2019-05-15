# -*- coding: utf-8 -*-
# @Time    : 5/10/2018 11:53 AM
# @Author  : sunyonghai
# @File    : open_image.py
# @Software: ZJ_AI
import argparse
import multiprocessing.pool

import numpy as np
import time
from PIL import Image
import os

import io_utils


def read_image_bgr(path):
    try:
        image = np.asarray(Image.open(path).convert('RGB'))
    except Exception as ex:
        print(path)
        io_utils.delete_file_folder(path)
        return None

    return image[:, :, ::-1].copy()

def get_data(data_path):
    for files in os.listdir(data_path):
        path = os.path.join(data_path,files)
        yield path

def process(path):
    st = time.time()
    read_image_bgr(path)
    end = time.time()

    str_info = "Image ID:{} --- read time:{} ms".format(os.path.basename(path), str(1000 * (end - st)))
    print(str_info)

def main(data_path):
    generator = get_data(data_path)
    # cpus = os.cpu_count()
    cpus = 2
    p = multiprocessing.pool.Pool(cpus)
    p.map_async(process, generator)

    p.close()
    p.join()

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-i', '--input',help='path of data', default='/home/syh/train_data/test')
args = parser.parse_args()

if __name__ == '__main__':
    # data_path = '/home/syh/all_train_data/JPEGImages'
    data_path =  os.path.join( args.input, 'JPEGImages' )
    # data_path =  '/home/syh/train_data/fusion/background_1333-800'
    st = time.time()
    main(data_path)
    end = time.time()
    str_info = "read time:{} minutes".format(str((end - st) / 60))
    print(str_info)


# if __name__ == '__main__':
#     # data_path = '/home/syh/all_train_data/JPEGImages'
#     data_path =  os.path.join( args.input, 'JPEGImages' )
#     st = time.time()
#     for files in os.listdir(data_path):
#         path = os.path.join(data_path,files)
#
#         read_image_bgr(path)
#
#     end = time.time()
#     str_info = "{}: read time:{} minutes".format(files, str((end - st) / 60))
#     print(str_info)

"""
cd /home/syh/RetinaNet/data_processing
python open_image.py -i /home/syh/train_data/data/sub_train_data/train_data-2018-05-10
"""