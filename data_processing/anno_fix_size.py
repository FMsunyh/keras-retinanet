#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 4/13/2018 5:35 PM 
# @Author : sunyonghai 
# @File : anno_fix_size.py 
# @Software: ZJ_AI
# =========================================================

import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2
import io_utils
from config import ROOT_HOME
from xml_utils import write_xml


def read_data(data_paths):
    print('Parsing annotation files')
    for data_path in data_paths:
        annot_path = os.path.join(data_path, 'Annotations')
        imgs_path = os.path.join(data_path, 'JPEGImages')

        annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
        for annot in annots:
            try:
                et = ET.parse(annot)
                element = et.getroot()

                element_filename = element.find('filename').text
                image_width = int(element.find('size').find('width').text)
                image_height = int(element.find('size').find('height').text)
                img_path = os.path.join(imgs_path, element_filename)

                image = cv2.imread(img_path)
                # print(img_path)

                flag = False
                if image_width != image.shape[1]:
                    print('width： anno %d, img %d' % (image_width, image.shape[1]))
                    node = element.find('size').find('width')
                    node.text = str(image.shape[1])
                    flag = True

                if image_height != image.shape[0]:
                    print('height：anno %d, img %d' % (image_height, image.shape[0]))
                    node = element.find('size').find('height')
                    node.text = str(image.shape[0])
                    flag = True

                if flag:
                    write_xml(et, annot)
                    flag = False
                    print(annot)

            except Exception as e:
                print('Exception in pascal_voc_parser: {}'.format(e))

                continue

if __name__ == '__main__':
    input_path = os.path.join(ROOT_HOME, 'data')
    # data_paths = [os.path.join(input_path, s) for s in ['all_data']]
    # dirs = ['train_data-2018-03-07', 'train_data-2018-03-16', 'train_data-2018-03-19',
    #         'train_data-2018-03-29', 'train_data-2018-03-30', 'train_data-2018-04-02','train_data-2018-04-09']

    dirs = ['train_data-2018-04-11']
    data_paths = [os.path.join(input_path, s) for s in dirs]
    imgs = read_data(data_paths)