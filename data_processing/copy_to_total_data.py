#!/usr/bin/python3

"""
Copyright 2018-2019  Firmin.Sun (fmsunyh@gmail.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# -----------------------------------------------------
# @Time    : 5/6/2019 3:22 PM
# @Author  : Firmin.Sun (fmsunyh@gmail.com)
# @Software: ZJ_AI
# -----------------------------------------------------
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 4/3/2018 11:15 AM
# @Author : sunyonghai
# @File : create_all_data.py
# @Software: ZJ_AI
# =========================================================
import argparse
import os
# import sys
# sys.path.append('/home/syh/RetinaNet/')
# curDir = os.getcwd()
# print(curDir)

from config import TRAIN_DATA
from utils.io_utils import copy_dir, mkdir, remove_all


def copy_JPEGImages(dir, dest_dir):
    copy_dir(dir, dest_dir)

def copy_Annotations(dir, dest_dir):
    copy_dir(dir, dest_dir)

def copy_JPEGImagess(data_paths, dest_dir):
    for data_dir in data_paths:
        jpegimages = os.path.join(data_dir, 'JPEGImages')
        print("{}:{}".format(jpegimages,len(os.listdir(jpegimages))))

        copy_JPEGImages(jpegimages, dest_dir)

def copy_Annotationss(data_paths, dest_dir):
    for data_dir in data_paths:
        annotations = os.path.join(data_dir, 'Annotations')
        print("{}:{}".format(annotations, len(os.listdir(annotations))))
        copy_Annotations(annotations, dest_dir)

def copy_all(dirs, tar_dir):
    dest_im_dir = os.path.join(tar_dir, 'JPEGImages')
    dest_anno_dir = os.path.join(tar_dir, 'Annotations')

    mkdir(dest_anno_dir)
    # remove_all(dest_anno_dir)
    copy_Annotationss(dirs, dest_anno_dir)
    print("total {}:{}".format(dest_anno_dir, len(os.listdir(dest_anno_dir))))

    mkdir(dest_im_dir)
    # remove_all(dest_im_dir)
    copy_JPEGImagess(dirs, dest_im_dir)
    print("total {}:{}".format(dest_im_dir, len(os.listdir(dest_im_dir))))

def append_all_data(dirs, tar_dir):
    dest_im_dir = os.path.join(tar_dir, 'JPEGImages')
    dest_anno_dir = os.path.join(tar_dir, 'Annotations')

    copy_Annotationss(dirs, dest_anno_dir)
    print("numbers of Annotations:{}".format(len(os.listdir(dest_anno_dir))))

    copy_JPEGImagess(dirs, dest_im_dir)
    print("numbers of JPEGImages:{}".format(len(os.listdir(dest_im_dir))))


parser = argparse.ArgumentParser(description='Get the data info')
# parser.add_argument('-r', '--root_path', help='data folder of all train data', default='/home/syh/train_data/C300_SUN')
# parser.add_argument('-d', '--total_data', help='data folder of all train data', default='total_data')
# parser.add_argument('-s', '--sub_train_data', help='data folder of sub train data', type=str, default=['test_data_2019-04-26',
#                                                                                                        'all_train_data_resize2_wt-wtcyl-gz-nm-310ml',
#                                                                                                        'train_data_2019-05-06_worksite',
#                                                                                                        'train_data_yj_300c_outdoor',
#                                                                                                        'train_data_yj_300c_outdoor2',
#                                                                                                        'train_data_yj_300c_outdoor3',
#                                                                                                        'train_data_yj_300c_showroom',
#                                                                                                        'train_data_yj_300c_showroom4',
#                                                                                                        'train_data_yj_300c_UAshop'
#                                                                                                        ])


parser.add_argument('-r', '--root_path', help='data folder of all train data', default='/home/syh/train_data/C1000')
parser.add_argument('-d', '--total_data', help='data folder of all train data', default='total_data')
parser.add_argument('-s', '--sub_train_data', help='data folder of sub train data', type=str, default=['UA+_train_data_1000c_1_resize',
                                                                                                       'UA+_train_data_1000c_2_resize'
                                                                                                       ])

args = parser.parse_args()

if __name__ == '__main__':
    total_data_path = os.path.join(args.root_path, args.total_data)
    # src_train_data = os.path.join(args.root_path, args.sub_train_data)

    # dirs = [os.path.join(src_train_data, s) for s in os.listdir(src_train_data)]
    dirs = [os.path.join(args.root_path, s) for s in args.sub_train_data]
    copy_all(dirs, total_data_path)


# if __name__ == '__main__':
#     dirs = ['data_52/train_data-2018-04-18', 'data_52/train_data-2018-04-19']
#
#     tar_dir = os.path.join(ROOT_HOME, 'data_52/all_data/')
#     copy_all(dirs, tar_dir)