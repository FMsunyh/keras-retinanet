# -*- coding: utf-8 -*-
# @Time    : 4/26/2018 11:03 AM
# @Author  : sunyonghai
# @File    : compression.py
# @Software: ZJ_AI

import argparse
import os

import io_utils
from zip_utils import zip_list

# parser = argparse.ArgumentParser(description='Get the data info')
# parser.add_argument('-i', '--dir',help='directory to zip', default='/home/syh/RetinaNet/data_52/test')
# parser.add_argument('-o', '--output',help='output diretory', default='/home/syh/RetinaNet/data_52/test')
# args = parser.parse_args()


def _compression_without_anno(dir, output):
    if dir and output:
        JPEGImages_dir = os.path.join(dir, 'JPEGImages')
        images_paths = [os.path.join(JPEGImages_dir, s) for s in os.listdir(JPEGImages_dir)]
        images_paths.sort()
        save_dir = os.path.join(output, 'zip')
        io_utils.mkdir(save_dir)
        batch_size = 100
        image_batchs = [images_paths[i:i + batch_size] for i in range(0, len(images_paths), batch_size)]

        for idx, image_batch in enumerate(image_batchs):
            save_path = os.path.join(save_dir,'{}{}{}'.format(os.path.basename(output), '-{}'.format(idx), '.zip'))
            zip_list(image_batch, save_path)

def _compression_with_anno(dir, output):
    if dir and output:
        JPEGImages_dir = os.path.join(dir, 'JPEGImages')
        Annotations_dir = os.path.join(dir, 'Annotations')
        images_paths = [os.path.join(JPEGImages_dir, s) for s in os.listdir(JPEGImages_dir)]
        annos_paths = [os.path.join(Annotations_dir, s) for s in os.listdir(Annotations_dir)]

        images_paths.sort()
        annos_paths.sort()

        save_dir = os.path.join(output, 'zip')
        io_utils.mkdir(save_dir)

        batch_size = 200
        image_batchs = [images_paths[i:i + batch_size] for i in range(0, len(images_paths), batch_size)]
        anno_batchs = [annos_paths[i:i + batch_size] for i in range(0, len(annos_paths), batch_size)]

        for idx, (image_batch, anno_batch) in enumerate(zip(image_batchs, anno_batchs)):
            save_path = os.path.join(save_dir, '{}{}{}'.format(os.path.basename(output), '-{}'.format(idx), '.zip'))
            zip_list(image_batch, save_path)
            zip_list(anno_batch, save_path, mode='a')


def zip_batch(dir, output):
    if dir and output:
        JPEGImages_dir = os.path.join(dir, 'JPEGImages')
        Annotations_dir = os.path.join(dir, 'Annotations')

        if os.path.exists(Annotations_dir) and os.path.exists(JPEGImages_dir) and len(os.listdir(Annotations_dir)) >0:
            _compression_with_anno(dir, output)
        else:
            _compression_without_anno(dir, output)

if __name__ == '__main__':
    if args.dir and args.output:
        zip_batch(args.dir, args.output)
    else:
        print('error')


"""
cd /home/syh/RetinaNet/data_processing
python compression.py -i /home/syh/RetinaNet/data_52/test_zip -o /home/syh/RetinaNet/data_52/test_zip/
"""