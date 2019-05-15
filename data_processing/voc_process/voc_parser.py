#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/30/2018 2:01 PM 
# @Author : sunyonghai 
# @File : voc_parser.py 
# @Software: ZJ_AI
# =========================================================
import argparse
import json
import os
import pprint

import cv2
import xml.etree.ElementTree as ET
import numpy as np
import csv

from csv_utils import createDictCSV, createListCSV2


def get_data(data_path):
    '''
    读取pascal voc 数据
    1)基本信息设置
    2)读取XML文件
    3)是否显示图片
    :param input_path: 只需要给定到VOC所在的文件夹，不需要知道给定到具体的版本
    如：input_path = 'F:/study_files/faster_rcnn/training_data/VOCdevkit'
    :return:
    '''
    '''
    图片的高度，宽度，路径，和所处训练集和框。
    其中bboxes: 其是一个list,每一条信息是以字典形式存储包含了一个box的所有信息。
    有难度，类别，上下两点的坐标。下面是一个示列:
    [{'height': 500, 
    'imageset': 'trainval',
    'width': 486, 
    'filepath':'data/VOC2012/JPEGImages/2007_000027.jpg',
    'bboxes': [
                {
                    'x1': 174，
                    'x2': 349, 
                    'y1': 101, 
                    'y2': 351,
                    'class': 'person', 
                    'difficult':False,
                    }，
                    {
                    'x1': 174，
                    'x2': 349, 
                    'y1': 101, 
                    'y2': 351,
                    'class': 'person', 
                    'difficult':False,
                }
               ]
    }]
    '''
    all_imgs = []  # 其是一个list,每一条信息是以字典形式存储包含了一张图片的所有信息。

    classes_count = {}  # classes_count:是一个字典，其存储类别和其对应的总个数。比如：{'person': 12, 'horse': 21}

    class_mapping = {}  # 是一个字典，其对应每一个类别对应的编号，one-hot {'person': 0, 'horse': 1}

    visualise = False

    # train VOC2012
    # data_paths = [os.path.join(input_path,s) for s in ['VOC2012']]
    # data_paths = [os.path.join(input_path, s) for s in ['VOC2007', 'VOC2012']]
    # 如果有新的数据集，只需要添加到列表即可


    print('Parsing annotation files')
    #
    # for data_path in data_paths:

    annot_path = os.path.join(data_path, 'Annotations')
    imgs_path = os.path.join(data_path, 'JPEGImages')
    imgsets_path_trainval = os.path.join(data_path, 'ImageSets/Main/trainval.txt')
    imgsets_path_test = os.path.join(data_path, 'ImageSets/Main/test.txt')

    # 得到训练与测试集图片文件的名称，这是为以后判断图片是属于哪个集而准备的
    # 犹豫没有测试，和交叉检验，所以这个暂时没起到作用
    trainval_files = []
    test_files = []
    try:
        with open(imgsets_path_trainval) as f:
            for line in f:
                trainval_files.append(line.strip() + '.jpg')
    except Exception as e:
        print(e)

    try:
        with open(imgsets_path_test) as f:
            for line in f:
                test_files.append(line.strip() + '.jpg')
    except Exception as e:
        if data_path[-7:] == 'VOC2012':
            # this is expected, most pascal voc distibutions dont have the test.txt file
            pass
        else:
            print(e)

    annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
    idx = 0
    for annot in annots:
        try:
            idx += 1

            et = ET.parse(annot)
            element = et.getroot()  # 得到xml的根

            element_objs = element.findall('object')
            element_filename = element.find('filename').text
            element_width = int(round(float(element.find('size').find('width').text)))
            element_height = int(round(float(element.find('size').find('height').text)))

            if len(element_objs) > 0:
                # annotation format 封装后的注释格式
                annotation_data = {'filepath': os.path.join(imgs_path, element_filename),
                                   'width': element_width,
                                   'height': element_height,
                                   'bboxes': []}

                if element_filename in trainval_files:
                    annotation_data['imageset'] = 'trainval'
                elif element_filename in test_files:
                    annotation_data['imageset'] = 'test'
                else:
                    annotation_data['imageset'] = 'trainval'

            for element_obj in element_objs:

                ## 做分类用的
                # class_label = element_obj.find('name').text
                # if class_label != 'other':
                #     class_name = class_label.split('-')[2]
                # else:
                #     class_name = class_label # 'other'
                #     continue # 不要other类框

                ## 直接目标检测
                class_name = element_obj.find('name').text

                if class_name not in classes_count:
                    classes_count[class_name] = 1
                else:
                    classes_count[class_name] += 1

                if class_name not in class_mapping:
                    class_mapping[class_name] = len(class_mapping)

                obj_bbox = element_obj.find('bndbox')
                x1 = int(round(float(obj_bbox.find('xmin').text)))
                y1 = int(round(float(obj_bbox.find('ymin').text)))
                x2 = int(round(float(obj_bbox.find('xmax').text)))
                y2 = int(round(float(obj_bbox.find('ymax').text)))
                difficulty = int(element_obj.find('difficult').text) == 1
                # annotation format of bounding box 矩形框的封装格式
                annotation_data['bboxes'].append(
                    {'class': class_name,
                     'x1': x1,
                     'x2': x2,
                     'y1': y1,
                     'y2': y2,
                     'difficult': difficulty})
            all_imgs.append(annotation_data)

            if visualise:
                img = cv2.imread(annotation_data['filepath'])
                for bbox in annotation_data['bboxes']:
                    cv2.rectangle(img, (bbox['x1'], bbox['y1']), (bbox['x2'], bbox['y2']), (0, 0, 255))
                cv2.imshow('img', img)
                cv2.waitKey(0)

        except Exception as e:
            print('Exception in pascal_voc_parser: {}\n{}'.format(e,annot))
            continue
    return all_imgs, classes_count, class_mapping




def sort_by_value(d):
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort()
    return [backitems[i][1] for i in range(0, len(backitems))]

def save_mapping(fileName="", class_mapping=[]):
    # with open('/home/syh/RetinaNet/mapping_54.json', 'w+') as f:
    with open(fileName, 'w+') as f:
        json.dump(class_mapping, f,sort_keys=True)
        print('save the class mapping to ', fileName)

# predefined_classes.txt
def save_predefined_classes(fileName="", classes_count=[]):
    a = sorted(classes_count.items(), key=lambda item: item[0])
    with open(fileName,'w+') as f:
        for idx in range(len(a)):
            f.write(a[idx][0]+'\n')

    print("save data to '%s'" % fileName)

def save_string_list(fileName="", classes_count=[]):
    a = sorted(classes_count.items(), key=lambda item: item[0])
    with open(fileName,'w+') as f:
        for idx in range(len(a)):
            f.write("\"{}\",".format(a[idx][0]))

    print("save data  string_list to '%s'" % fileName)

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-p', '--parent_data',help='the parent folder of data', default='/home/syh/train_data/data/')
parser.add_argument('-d', '--datadir',help='the folder of data', default='all_train_data_resize2')
args = parser.parse_args()

if __name__ == '__main__':
    if args.parent_data and args.datadir:
        data_path = os.path.join(args.parent_data, args.datadir)
        all_imgs, classes_count, class_mapping = get_data(data_path)

        if not os.path.exists(os.path.join(data_path, 'infos')):
            os.makedirs(os.path.join(data_path, 'infos'))

        save_mapping(os.path.join(data_path, 'infos/name_to_label.json'), class_mapping)

        class_mapping_sorted = sorted(class_mapping.items(), key=lambda item:item[1])
        createListCSV2(os.path.join(data_path, 'infos/mapping.csv') , class_mapping_sorted)

        createDictCSV(os.path.join(data_path, 'infos/classes_count.csv'), classes_count)

        save_predefined_classes(os.path.join(data_path, 'infos/predefined_classes.txt') , classes_count)

        save_string_list(os.path.join(data_path,'infos/string_list_classes.txt') , classes_count)

'''
cd /home/syh/RetinaNet/data_processing
python voc_process/voc_parser.py -p /home/syh/train_data/data/ -d aug-all_train_data
'''