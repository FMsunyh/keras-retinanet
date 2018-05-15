#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/29/2018 9:33 AM 
# @Author : sunyonghai 
# @File : before_label.py 
# @Software: ZJ_AI
# =========================================================
import os
import cv2
import io_utils
import numpy as np
import datetime
import argparse

def _rot90(parent_dir, image_dir):
    imgs_path = os.path.join(parent_dir, image_dir)
    imgs_out_path = os.path.join(parent_dir, '{}{}'.format(image_dir, '_with_rot90'))
    io_utils.delete_file_folder(imgs_out_path)
    io_utils.mkdir(imgs_out_path)

    images = [os.path.join(imgs_path, s) for s in os.listdir(imgs_path)]
    for image_file in images:
        try:
            img = cv2.imread(image_file)
            width = img.shape[0]
            height = img.shape[1]
            if width > height:
                image = np.array(np.rot90(img, 1))
                image = image.copy()
            else:
                image = img
            name = image_file.split('/')[-1]
            save_path = os.path.join(imgs_out_path, name)

            # don't need resize
            # image = cv2.resize(image, (int(image.shape[1] * 0.5), int(image.shape[0]*0.5)), interpolation=cv2.INTER_CUBIC)
            # print('resize:{}'.format(image.shape))

            cv2.imwrite(save_path, image)

            print(save_path)
        except Exception as e:
            print('Exception in pascal_voc_parser: {}'.format(e))
            continue

    return imgs_out_path

def _rename_image(parent_dir, image_dir_name, str_date):
    # image_dir_name = 'JPEGImages'
    data_dir = os.path.join(parent_dir, image_dir_name)
    data_rename_dir = os.path.join(parent_dir, '{}_rename'.format(image_dir_name))

    io_utils.delete_file_folder(data_rename_dir)
    io_utils.mkdir(data_rename_dir)
    prefix = 'train'
    idx = 1000
    cur_date = datetime.datetime.now()
    # str_date = '{year}{month}{day}'.format(year=cur_date.year, month=cur_date.month, day=cur_date.day)
    for s in os.listdir(data_dir):
        old = os.path.join(data_dir, s)
        new = os.path.join(data_rename_dir, '{}_{}_{}.jpg'.format(prefix, str_date, idx))
        io_utils.copy(old,new)
        idx = idx+1

    return data_rename_dir

def _copy_to_JPEGImages(parent_dir, src_dir):
    target_dir = os.path.join(parent_dir, 'JPEGImages/')
    io_utils.mkdir(target_dir)
    io_utils.remove_all(target_dir)
    for s in os.listdir(src_dir):
        file = os.path.join(src_dir, s)
        io_utils.copy(file, target_dir)

def _rename(src_name,dest_name):
    # target_dir = os.path.join(parent_dir, 'JPEGImages/')
    io_utils.rename(src_name, dest_name)



def before_label_process(parent_dir, folder_name, str_date):
    if parent_dir and folder_name and str_date:
        new_dir = _rot90(parent_dir, folder_name)
        rename_dir = _rename_image(parent_dir, new_dir, str_date)
        # _copy_to_JPEGImages(parent_dir, rename_dir)
        dest_dir = os.path.join(parent_dir, 'JPEGImages/')
        _rename(rename_dir, dest_dir)
    else:
        print('args error')

# parser = argparse.ArgumentParser(description='Get the data info')
# parser.add_argument('-p', '--parent_dir',help='the parent folder of image', default='')
# parser.add_argument('-d', '--folder_name',help='the folder of image', default='origin')
# parser.add_argument('-s', '--str_date',help='{  year}{month}{day}', default='')
# args = parser.parse_args()
# str_date = '{year}{month}{day}'.format(year='2018', month='04', day='12')

if __name__  == '__main__':
    if args.parent_dir and args.folder_name and args.str_date:
        before_label_process(args.parent_dir, args.folder_name ,args.str_date)
    else:
        print('args error')


    # parent_dir = '/home/syh/RetinaNet/data_63/2018-04-28'
    # dest_dir = os.path.join(parent_dir, 'JPEGImages_/')
    # src_name = '/home/syh/RetinaNet/data_63/2018-04-28/2018-04-28_with_rot90_rename'
    # _rename(src_name, dest_dir)



    # if args.parent_dir and args.folder_name and args.str_date:
    #     str_date = args.str_date
    #     new_dir = _rot90(args.parent_dir, args.folder_name)
    #     rename_dir = _rename_image(args.parent_dir, new_dir)
    #     _copy_to_JPEGImages(rename_dir)
    # else:
    #     print('args error')


"""
run:
python before_label.py -p /home/syh/RetinaNet/data/train_data-2018-04-12/ -s 20180412
run this script,then run the test.py to create Annotations file
"""