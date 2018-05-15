#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 4/12/2018 6:13 PM 
# @Author : sunyonghai 
# @File : copy_marked.py 
# @Software: ZJ_AI
# =========================================================
import argparse
import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2

import io_utils
from config import ROOT_HOME
from xml_utils import write_xml


def copy_marked(data_path):

    if not os.path.isdir(data_path):
        print('input_path is not a dir: {}'.format(data_path))
        return

    # for data_path in input_path:
    annot_path = os.path.join(data_path, 'Annotations')
    imgs_path = os.path.join(data_path, 'JPEGImages')
    imgs_out_path = os.path.join(data_path, 'JPEGImages_marked')
    io_utils.mkdir(imgs_out_path)

    annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
    for annot in annots:
        try:
            et = ET.parse(annot)
            element = et.getroot()
            element_filename = element.find('filename').text
            filepath = os.path.join(imgs_path, element_filename)
            io_utils.copy(filepath, imgs_out_path)
        except Exception as e:
            print('Exception in pascal_voc_parser: {}'.format(e))
            continue

def rename_image(data_path):

    if not os.path.isdir(data_path):
        print('input_path is not a dir: {}'.format(data_path))
        return

    # for data_path in input_path:
    annot_path = os.path.join(data_path, 'Annotations')
    imgs_path = os.path.join(data_path, 'JPEGImages')
    imgs_out_path = os.path.join(data_path, 'JPEGImages_marked')
    io_utils.mkdir(imgs_out_path)

    annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
    for annot in annots:
        try:
            et = ET.parse(annot)
            element = et.getroot()
            node = element.find('filename')
            element_filename = element.find('filename').text
            # a = element_filename[-3:]
            # print(a)
            if '.' in element_filename:
                pass
            else:
                node.text = element_filename[:-3]+'.'+'jpg'
                print(annot)
                print(node.text)
                write_xml(et, annot)

        except Exception as e:
            print('Exception in pascal_voc_parser: {}'.format(e))
            continue

parser = argparse.ArgumentParser(description='Get the data info')
# parser.add_argument('-d', '--datadir',help='the folder of data', default='../data/train_data-2018-04-11')
parser.add_argument('-d', '--datadir',help='the folder of data', default='train_data-2018-04-12')
args = parser.parse_args()

if __name__ == '__main__':
    if args.datadir:
    # input_path = '../data/train_data-2018-04-11'
        train_data_dir = os.path.join(ROOT_HOME, 'data', args.datadir)
        copy_marked(train_data_dir)

"""
cd /home/syh/RetinaNet/data_processing
python copy_marked.py -d train_data-2018-04-12
"""