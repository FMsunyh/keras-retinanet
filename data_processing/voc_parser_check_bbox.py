#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 4/13/2018 1:51 PM 
# @Author : sunyonghai 
# @File : voc_parser_check_bbox.py 
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
    all_imgs = []
    print('Parsing annotation files')

    for data_path in data_paths:
        annot_path = os.path.join(data_path, 'Annotations')
        imgs_path = os.path.join(data_path, 'JPEGImages')

        annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
        for annot in annots:
            try:
                et = ET.parse(annot)
                element = et.getroot()

                element_objs = element.findall('object')
                element_filename = element.find('filename').text
                element_width = int(element.find('size').find('width').text)
                element_height = int(element.find('size').find('height').text)

                if len(element_objs) > 0:
                    # annotation format 封装后的注释格式
                    annotation_data = {'img_path': os.path.join(imgs_path, element_filename),
                                       'anno_path': annot,
                                       'width': element_width,
                                       'height': element_height,
                                       'bboxes': []}

                for element_obj in element_objs:
                    class_name = element_obj.find('name').text
                    obj_bbox = element_obj.find('bndbox')
                    x1 = int(round(float(obj_bbox.find('xmin').text)))
                    y1 = int(round(float(obj_bbox.find('ymin').text)))
                    x2 = int(round(float(obj_bbox.find('xmax').text)))
                    y2 = int(round(float(obj_bbox.find('ymax').text)))
                    # annotation format of bounding box 矩形框的封装格式
                    annotation_data['bboxes'].append(
                        {'class': class_name,
                         'x1': x1,
                         'x2': x2,
                         'y1': y1,
                         'y2': y2})
                all_imgs.append(annotation_data)

            except Exception as e:
                print('Exception in pascal_voc_parser: {}'.format(e))
                continue

    return all_imgs

def bbox_is_4(data_paths):
    print('Parsing annotation files')
    for data_path in data_paths:
        annot_path = os.path.join(data_path, 'Annotations')
        annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
        for annot in annots:
            try:
                et = ET.parse(annot)
                element = et.getroot()
                element_objs = element.findall('object')
                if len(element_objs) > 4:
                    print(annot)
                if len(element_objs) < 4:
                    print(annot)
            except Exception as e:
                print('Exception in pascal_voc_parser: {}'.format(e))
                continue

def read_data2(data_paths):
    all_imgs = []
    print('Parsing annotation files')

    for data_path in data_paths:
        annot_path = os.path.join(data_path, 'Annotations')
        imgs_path = os.path.join(data_path, 'JPEGImages')

        idx=0
        annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
        for annot in annots:
            try:
                et = ET.parse(annot)
                element = et.getroot()

                element_objs = element.findall('object')
                element_filename = element.find('filename').text
                element_width = int(element.find('size').find('width').text)
                element_height = int(element.find('size').find('height').text)
                if len(element_objs) >4:
                    print(annot)
                if len(element_objs) <4:
                    print(annot)
                for element_obj in element_objs:
                    obj_bbox = element_obj.find('bndbox')
                    x1 = (float(obj_bbox.find('xmin').text)) - 1

                    if x1 - 1.82500000e+03 <=0.0000001:
                        print(annot)

                    # print(obj_bbox.find('xmin').text)

                    y1 = int(round(float(obj_bbox.find('ymin').text)))
                    x2 = int(round(float(obj_bbox.find('xmax').text)))
                    y2 = int(round(float(obj_bbox.find('ymax').text)))
                    idx+=1
            except Exception as e:
                print('Exception in pascal_voc_parser: {}'.format(e))
                continue
    print('idx %d' % idx)
    return all_imgs

def check_bbox(imgs):
    if len(imgs)<=0:
        print('no data')
        return None
    errors = []

    error_imgs = []
    for img in imgs:
        assert 'img_path' in img
        assert 'anno_path' in img
        assert 'bboxes' in img
        assert 'width' in img
        assert 'height' in img

        try:
            filepath = img['img_path']
            image = cv2.imread(filepath)
            bboxs =  img['bboxes']
            for bbox in bboxs:
                class_name = bbox['class']
                x1 = bbox['x1']
                x2 = bbox['x2']
                y1 = bbox['y1']
                y2 = bbox['y2']

                # test x2 < x1 | y2 < y1 | x1 < 0 | y1 < 0 | x2 <= 0 | y2 <= 0 | x2 >= image.shape[1] | y2 >= image.shape[0]
                if (
                x2 < x1 or
                y2 < y1 or
                x1 < 0 or
                y1 < 0 or
                x2 <= 0 or
                y2 <= 0 or
                x2 >= image.shape[1] or
                y2 >= image.shape[0]):
                    str_info = 'Contains the invalid boxes in:%s: %s' % (img['anno_path'].split('/')[-1],class_name)
                    # print(str_info)
                    errors.append(str_info)
                    error_imgs.append(img)
        except Exception as ex:
            print('Exception: %s' % filepath)
        else:
            pass
            # print('no Exception')

    return errors,error_imgs

def fix_bbox(imgs):
    if len(imgs)<=0:
        print('no data')
        return None
    errors = []
    for img in imgs:
        assert 'img_path' in img
        assert 'anno_path' in img
        assert 'bboxes' in img
        assert 'width' in img
        assert 'height' in img

        try:
            annot_path = img['anno_path']
            et = ET.parse(annot_path)
            element = et.getroot()
            element_objs = element.findall('object')
            element_width = int(element.find('size').find('width').text)
            element_height = int(element.find('size').find('height').text)

            for element_obj in element_objs:
                class_name = element_obj.find('name').text
                obj_bbox = element_obj.find('bndbox')
                x1 = int(round(float(obj_bbox.find('xmin').text)))
                y1 = int(round(float(obj_bbox.find('ymin').text)))
                x2 = int(round(float(obj_bbox.find('xmax').text)))
                y2 = int(round(float(obj_bbox.find('ymax').text)))


                # test x2 < x1 | y2 < y1 | x1 < 0 | y1 < 0 | x2 <= 0 | y2 <= 0 | x2 >= image.shape[1] | y2 >= image.shape[0]
                if ( x2 < x1 or y2 < y1):
                    pass

                if (x1 < 0):
                    node = obj_bbox.find('xmin')
                    node.text =  '0'

                if y1 < 0:
                    node = obj_bbox.find('ymin')
                    node.text = '0'

                if x2 >= element_width:
                    x2 = element_width - 1
                    node = obj_bbox.find('xmax')
                    node.text = str(x2)

                if y2 >= element_height:
                    y2 = element_height - 1
                    node = obj_bbox.find('ymax')
                    node.text = str(y2)

            str_info = 'Fix the invalid boxes in:%s: %s' % (img['anno_path'].split('/')[-1], class_name)
            print(str_info)
            write_xml(et, annot_path)

                #  or
                # y1 < 0 or
                # x2 <= 0 or
                # y2 <= 0 or
                # x2 >= image.shape[1] or
                # y2 >= image.shape[0]):
                #     str_info = 'Contains the invalid boxes in:%s: %s' % (img['anno_path'].split('/')[-1],class_name)
                #     # print(str_info)
                #     errors.append(str_info)
        except Exception as ex:
            print('Exception: %s' % ex)
        else:
            pass
            # print('no Exception')

    return errors

def save_errors(fileName="", errors=[]):
    with open(fileName, 'w+') as f:
        for idx in range(len(errors)):
            f.write(errors[idx] + '\n')

    print("save data to '%s'" % fileName)

if __name__ == "__main__":
    input_path = os.path.join(ROOT_HOME, 'data')
    out_dir = os.path.join(ROOT_HOME, 'data_processing/errors')
    # data_paths = [os.path.join(input_path, s) for s in ['all_data']]
    data_paths = [os.path.join(input_path, s) for s in ['train_data-2018-04-11']]
    imgs = read_data(data_paths)
    print('Total images: %d' % len(imgs))
    errors, error_imgs = check_bbox(imgs)

    fix_bbox(error_imgs)

    path = os.path.join(out_dir, 'invalid_boxes.txt')
    save_errors(fileName=path, errors=errors)
    print('finished check.')

# if __name__ == '__main__':
#     input_path = os.path.join(ROOT_HOME, 'data')
#     out_dir = os.path.join(ROOT_HOME, 'data_processing/errors')
#     data_paths = [os.path.join(input_path, s) for s in ['train_data-2018-04-09']]
#     imgs = read_data2(data_paths)

# if __name__ == '__main__':
#     input_path = os.path.join(ROOT_HOME, 'data')
#     out_dir = os.path.join(ROOT_HOME, 'data_processing/errors')
#     data_paths = [os.path.join(input_path, s) for s in ['train_data-2018-04-09']]
#     bbox_is_4(data_paths)