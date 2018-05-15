#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 4/3/2018 11:15 AM 
# @Author : sunyonghai 
# @File : create_all_data.py 
# @Software: ZJ_AI
# =========================================================

import os
# import sys
# sys.path.append('/home/syh/RetinaNet/')
# curDir = os.getcwd()
# print(curDir)

from config import TRAIN_DATA
from io_utils import copy_dir, mkdir, remove_all

src_train_data = os.path.join(TRAIN_DATA, 'sub_train_data')

def copy_JPEGImages(dir, dest_dir):
    copy_dir(dir, dest_dir)

def copy_Annotations(dir, dest_dir):
    copy_dir(dir, dest_dir)


def copy_JPEGImagess(dirs, dest_dir):
    data_paths = [os.path.join(src_train_data, s) for s in dirs]
    for data_dir in data_paths:
        jpegimages = os.path.join(data_dir, 'JPEGImages')
        copy_JPEGImages(jpegimages, dest_dir)

def copy_Annotationss(dirs, dest_dir):
    data_paths = [os.path.join(src_train_data, s) for s in dirs]
    for data_dir in data_paths:
        annotations = os.path.join(data_dir, 'Annotations')
        print("numbers of Annotations:{}".format(len(os.listdir(annotations))))
        # count += len(os.listdir(annotations))
        copy_Annotations(annotations, dest_dir)

def copy_all(dirs, tar_dir):
    dest_im_dir = os.path.join(tar_dir, 'JPEGImages')
    dest_anno_dir = os.path.join(tar_dir, 'Annotations')

    mkdir(dest_anno_dir)
    remove_all(dest_anno_dir)
    copy_Annotationss(dirs, dest_anno_dir)
    print("numbers of Annotations:{}".format(len(os.listdir(dest_anno_dir))))

    mkdir(dest_im_dir)
    remove_all(dest_im_dir)
    copy_JPEGImagess(dirs, dest_im_dir)
    print("numbers of JPEGImages:{}".format(len(os.listdir(dest_im_dir))))

def append_all_data(dirs, tar_dir):
    dest_im_dir = os.path.join(tar_dir, 'JPEGImages')
    dest_anno_dir = os.path.join(tar_dir, 'Annotations')

    copy_Annotationss(dirs, dest_anno_dir)
    print("numbers of Annotations:{}".format(len(os.listdir(dest_anno_dir))))

    copy_JPEGImagess(dirs, dest_im_dir)
    print("numbers of JPEGImages:{}".format(len(os.listdir(dest_im_dir))))


if __name__ == '__main__':
    dirs = ['data/train_data-2018-03-07', 'data/train_data-2018-03-16', 'data/train_data-2018-03-19',
            'data/train_data-2018-03-29', 'data/train_data-2018-03-30', 'data/train_data-2018-04-02',
            'data/train_data-2018-04-09', 'data/train_data-2018-04-09-2','data/train_data-2018-04-11',
            'data/train_data-2018-04-11-2','data/train_data-2018-04-12']
    tar_dir = os.path.join(ROOT_HOME, 'data/all_data/')
    copy_all(dirs, tar_dir)


# if __name__ == '__main__':
#     dirs = ['data_52/train_data-2018-04-18', 'data_52/train_data-2018-04-19']
#
#     tar_dir = os.path.join(ROOT_HOME, 'data_52/all_data/')
#     copy_all(dirs, tar_dir)