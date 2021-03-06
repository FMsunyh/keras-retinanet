#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/10/2018 11:14 AM 
# @Author : sunyonghai 
# @File : draw_bbox.py 
# @Software: ZJ_AI
# =========================================================
import argparse
import os
import xml.etree.ElementTree as ET
import cv2
from utils import io_utils

def read_data(data_path):
    all_imgs = []

    print('Parsing annotation files')

    annot_path = os.path.join(data_path, 'Annotations')
    imgs_path = os.path.join(data_path, 'JPEGImages')
    imgs_out_path = os.path.join(data_path, 'JPEGImages_with_bbox')
    io_utils.delete_file_folder(imgs_out_path)
    io_utils.mkdir(imgs_out_path)

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
                annotation_data = {'filepath': os.path.join(imgs_path, element_filename),
                                   'file_out_path': os.path.join(imgs_out_path, element_filename),
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

            image = cv2.imread(annotation_data['filepath'])

            for bbox in annotation_data['bboxes']:
                cv2.rectangle(image, (bbox['x1'], bbox['y1']), (bbox['x2'], bbox['y2']), (55,255,155),5)
                # 各参数依次是：照片/添加的文字/左上角坐标/字体/字体大小/颜色/字体粗细
                cv2.putText(image, bbox['class'], (bbox['x1']-5, bbox['y1']-5), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 0), 3)
            print(annotation_data['file_out_path'])
            cv2.imwrite(annotation_data['file_out_path'], image)
        except Exception as e:
            print('Exception in pascal_voc_parser: {}'.format(e))
            continue

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-d', '--train_data',help='path to train data', default='')
args = parser.parse_args()

if __name__ == "__main__":
    """
    将标注框画出来，保存在JPEGImages_with_bbox目录下
    """
    input_path = args.train_data
    read_data(input_path)

"""
python voc_process/draw_bbox.py -d ~/train_data/VOC2007
"""