# -*- coding: utf-8 -*-
# @Time    : 5/25/2018 7:53 PM
# @Author  : sunyonghai
# @File    : check_label.py
# @Software: ZJ_AI
import argparse
import json
import os
import xml.etree.ElementTree as ET

import config
from utils.io_utils import copy, mkdir


def search(data_path, label_name):

    search_result = []

    print('Parsing annotation files')
    annot_path = os.path.join(data_path, 'Annotations')
    annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
    for annot in annots:
        try:
            et = ET.parse(annot)
            element = et.getroot()

            element_objs = element.findall('object')

            # count = len(element_objs)
            # if count == 1:
            for element_obj in element_objs:
                node = element_obj.find('name')
                # print(node.text)
                class_name = node.text.strip()

                if class_name ==  label_name :

                    fname, ext = os.path.splitext(os.path.basename(annot))
                    print(annot, class_name)
                    search_result.append(fname)


            # if len(search_result) > 10:
            #     break

        except Exception as e:
            print('Exception in pascal_voc_parser: {}'.format(e))
            continue

    return search_result


def copy_file(src, dst, name):
    image_src_path = os.path.join(src, 'JPEGImages', name+'.jpg')
    dst_dir = os.path.join(dst, 'JPEGImages')
    mkdir(dst_dir)
    copy(image_src_path, dst_dir)


    anno_src_path = os.path.join(src, 'Annotations', name+'.xml')
    dst_dir = os.path.join(dst, 'Annotations')
    mkdir(dst_dir)

    copy(anno_src_path, dst_dir)


parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-d', '--data_dir',help='the folder of data', default='/home/syh/train_data/data/all_train_data_resize2')
parser.add_argument('-s', '--save_path',help='the folder of data', default='/home/syh/train_data/data/all_train_data_resize2')
parser.add_argument('-id', '--label_name',help='the folder of data', default='wrong')
args = parser.parse_args()

if __name__ == '__main__':
    input_path = args.data_dir

    label_name = args.label_name
    save_path = args.save_path

    save_path = '{}_{}'.format(args.save_path, label_name)

    mkdir(save_path)
    ids =  search(input_path, label_name)
    for id in ids:
        copy_file(input_path, save_path, id)
