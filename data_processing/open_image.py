# -*- coding: utf-8 -*-
# @Time    : 5/10/2018 11:53 AM
# @Author  : sunyonghai
# @File    : open_image.py
# @Software: ZJ_AI

import numpy as np
import time
from PIL import Image
import os

def read_image_bgr(path):
    try:
        image = np.asarray(Image.open(path).convert('RGB'))
        if image is None:
            raise Exception("Invalid image!", path)
    except Exception as ex:
        print(path)
        print(ex)
    return image[:, :, ::-1].copy()


if __name__ == '__main__':
    # data_path = '/home/syh/all_train_data/JPEGImages'
    data_path = '/home/syh/train_data/data02-04/JPEGImages'

    for files in os.listdir(data_path):
        path = os.path.join(data_path,files)
        st = time.time()
        read_image_bgr(path)
        end = time.time()

        str_info = "{}: read time:{} ms".format(files, str(1000 * (end - st)))
        print(str_info)
#
# if __name__ == '__main__':
#     data_path = '/home/syh/all_train_data/JPEGImages'
#
#     count = 0
#     for _ in range(0, 100):
#         path = '/home/syh/all_train_data/JPEGImages/train_20180409_1654.jpg'
#         st = time.time()
#         read_image_bgr(path)
#         end = time.time()
#         str_info = "read time:{} ms".format(str(1000 * (end - st)))
#         print(str_info)
#
#         count += 1000 * (end - st)
#
#     print("total:{}".format(count // 100))