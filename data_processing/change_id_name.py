# -*- coding: utf-8 -*-
# @Time    : 7/11/2018 9:48 AM
# @Author  : sunyonghai
# @File    : change_id_name.py
# @Software: ZJ_AI
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import io_utils
import xml_utils


# data_path = '/home/syh/Desktop/AugMix_0709/rest_goods' #10000-29999
#data_path = '/home/syh/Desktop/AugMix_0709/same' #30000-49999
data_path = '/home/syh/Desktop/AugMix_0709/diff'         #50000-69999
JPEGImages_dir = os.path.join(data_path, 'JPEGImages')
annotations_dir = os.path.join(data_path, 'Annotations')

data_new_path = '/home/syh/train_data/data/aug_train_data2/'
JPEGImages_new_dir = os.path.join(data_new_path, 'JPEGImages')
annotations_new_dir = os.path.join(data_new_path, 'Annotations')

def get_xml_by_imagename():
    id = 50000
    for image_file in os.listdir(JPEGImages_dir):
        image_name = os.path.splitext(image_file)[0]
        for annot_xml in os.listdir(annotations_dir):
            xml_name = os.path.splitext(annot_xml)[0]
            if image_name == xml_name:

                new_id = '{}{}'.format('fusion_2018-07-11_', id)
                xml = os.path.join(annotations_new_dir, new_id+'.xml')
                image = os.path.join(JPEGImages_new_dir, new_id+'.jpg')
                io_utils.copy(os.path.join(annotations_dir, annot_xml), xml)
                io_utils.copy(os.path.join(JPEGImages_dir, image_file), image)
                id+=1
                break

def get_imagenamge_by_label(input_path):
    annot_path = os.path.join(input_path, 'Annotations')
    annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
    for annot in annots:
        try:
            et = ET.parse(annot)
            element = et.getroot()
            node = element.find('filename')
            name = os.path.splitext(os.path.basename(annot))[0]
            node.text =name+'.jpg'
            xml_utils.write_xml(et, annot)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    # get_xml_by_imagename()
    get_imagenamge_by_label(data_new_path)