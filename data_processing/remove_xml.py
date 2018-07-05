# -*- coding: utf-8 -*-
# @Time    : 5/29/2018 10:42 AM
# @Author  : sunyonghai
# @File    : remove_xml.py
# @Software: ZJ_AI
import argparse
import os

def remove_xml(data_path):
    JPEGImages_path = os.path.join(data_path, 'JPEGImages')
    Annotations_path = os.path.join(data_path, 'Annotations')

    images = [os.path.splitext(file)[0] for file in os.listdir(JPEGImages_path)]
    annos = [os.path.splitext(file)[0] for file in os.listdir(Annotations_path)]

    s_images = set(images)
    # print(s_images)
    s_annos = set(annos)

    # print(s_annos)

    print(s_annos - s_images)
    print(s_images - s_annos)

parser = argparse.ArgumentParser(description='Get the data info')
# parser.add_argument('-d', '--datadir',help='the folder of data', default='/home/syh/train_data/test')
parser.add_argument('-d', '--datadir',help='the folder of data', default='/home/syh/train_data/data/all_train_data')
args = parser.parse_args()
if __name__ == '__main__':
    if args.datadir:
        #data_path = '../data/train_data-2018-04-11'
        data_path = args.datadir
        remove_xml(data_path)