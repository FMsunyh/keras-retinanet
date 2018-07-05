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
from io_utils import copy_dir, mkdir, remove_all



def copy_JPEGImages(dir, dest_dir):
    copy_dir(dir, dest_dir)

def copy_Annotations(dir, dest_dir):
    copy_dir(dir, dest_dir)

def copy_JPEGImagess(data_paths, dest_dir):
    for data_dir in data_paths:
        jpegimages = os.path.join(data_dir, 'JPEGImages')
        copy_JPEGImages(jpegimages, dest_dir)

def copy_Annotationss(data_paths, dest_dir):
    for data_dir in data_paths:
        annotations = os.path.join(data_dir, 'Annotations')
        print("numbers of Annotations:{}".format(len(os.listdir(annotations))))
        copy_Annotations(annotations, dest_dir)

def copy_all(dirs, tar_dir):
    dest_im_dir = os.path.join(tar_dir, 'JPEGImages')
    dest_anno_dir = os.path.join(tar_dir, 'Annotations')

    mkdir(dest_anno_dir)
    # remove_all(dest_anno_dir)
    copy_Annotationss(dirs, dest_anno_dir)
    print("numbers of Annotations:{}".format(len(os.listdir(dest_anno_dir))))

    # mkdir(dest_im_dir)
    # remove_all(dest_im_dir)
    # copy_JPEGImagess(dirs, dest_im_dir)
    # print("numbers of JPEGImages:{}".format(len(os.listdir(dest_im_dir))))

def append_all_data(dirs, tar_dir):
    dest_im_dir = os.path.join(tar_dir, 'JPEGImages')
    dest_anno_dir = os.path.join(tar_dir, 'Annotations')

    copy_Annotationss(dirs, dest_anno_dir)
    print("numbers of Annotations:{}".format(len(os.listdir(dest_anno_dir))))

    copy_JPEGImagess(dirs, dest_im_dir)
    print("numbers of JPEGImages:{}".format(len(os.listdir(dest_im_dir))))


parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-a', '--all_train_data', help='data folder of all train data', default='/home/syh/train_data/data/all_train_data')
parser.add_argument('-s', '--sub_train_data', help='data folder of sub train data', default='/home/syh/train_data/data/sub_train_data')
args = parser.parse_args()

if __name__ == '__main__':
    src_train_data = args.sub_train_data
    all_train_data_dir = args.all_train_data

    dirs = [os.path.join(src_train_data, s) for s in os.listdir(src_train_data)]
    copy_all(dirs, all_train_data_dir)


# if __name__ == '__main__':
#     dirs = ['data_52/train_data-2018-04-18', 'data_52/train_data-2018-04-19']
#
#     tar_dir = os.path.join(ROOT_HOME, 'data_52/all_data/')
#     copy_all(dirs, tar_dir)