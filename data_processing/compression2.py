# -*- coding: utf-8 -*-
# @Time    : 5/22/2018 6:08 PM
# @Author  : sunyonghai
# @File    : compression2.py
# @Software: ZJ_AI

import argparse
import os

import io_utils
from zip_utils import zip_list

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-i', '--data_path',help='directory to zip', default='/home/syh/train_data/data/sub_train_data')
parser.add_argument('-o', '--output',help='output diretory', default='/home/syh/train_data/data/sub_train_data/zip')
args = parser.parse_args()

def _compression(dir, output):
    if dir and output:
        JPEGImages_dir = os.path.join(dir, 'JPEGImages')
        Annotations_dir = os.path.join(dir, 'Annotations')
        images_paths = [os.path.join(JPEGImages_dir, s) for s in os.listdir(JPEGImages_dir)]
        annos_paths = [os.path.join(Annotations_dir, s) for s in os.listdir(Annotations_dir)]

        save_dir = output
        io_utils.mkdir(save_dir)

        save_path = os.path.join(save_dir, '{}{}'.format(os.path.basename(dir), '.zip'))
        zip_list(images_paths, save_path)
        zip_list(annos_paths, save_path, mode='a')


def main(data_path, output):
    if data_path and output:
        data_paths = [os.path.join(data_path, s) for s in os.listdir(data_path)]
        for data_path in data_paths:
            _compression(data_path, output)


if __name__ == '__main__':
    if args.data_path and args.output:
        main(args.data_path, args.output)
    else:
        print('error')


"""
cd /home/syh/RetinaNet/data_processing
python compression.py -i /home/syh/train_data/data/sub_train_data -o /home/syh/train_data/data/sub_train_data/zip
"""