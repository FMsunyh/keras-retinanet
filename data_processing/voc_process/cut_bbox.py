# -*- coding: utf-8 -*-
# @Time    : 5/10/2018 11:53 AM
# @Author  : CarrieChen
# @File    : cut_bbox.py
# @Software: ZJ_AI
# this code is for cut out bbox images and put the same kind of labels into a folder.
import argparse
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

from utils import io_utils
from utils.io_utils import *
from PIL import Image
import matplotlib.pyplot as plt

def dict_init(input_path):
    annot_path = os.path.join(input_path, 'Annotations')
    count = {}
    annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
    list=[]
    img_name_list=[]
    for annot in annots: #read a xml
        try:
            et = ET.parse(annot)
            element = et.getroot()
            element_objs = element.findall('object')
            img_name = element.find('filename').text
            for element_obj in element_objs:
                class_name = element_obj.find('name').text  #find label
                if class_name in list:  #judge is important
                    if img_name in img_name_list:
                        count[class_name][img_name] = count[class_name][img_name] + 1
                    else:
                        count[class_name][img_name]=0
                else:
                    count[class_name]={}
                    count[class_name][img_name] = 0
                    list.append(class_name)

        except Exception as e:
            print('Exception in pascal_voc_parser: {}'.format(e))
            continue
    return count

def count_and_cut(input_path,count):
    annot_path = os.path.join(input_path, 'Annotations')
    img_path = os.path.join(input_path, 'JPEGImages')
    save_folder = os.path.join(input_path, 'label_bbox')
    io_utils.mkdir(save_folder)
    io_utils.remove_all(save_folder)
    annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
    for annot in annots:  # read a xml
        try:
            et = ET.parse(annot)
            element = et.getroot()
            element_objs = element.findall('object')
            img_name = element.find('filename').text

            new_img_path = os.path.join(img_path, img_name)
            for element_obj in element_objs:
                class_name = element_obj.find('name').text  # find label
                count[class_name][img_name] = count[class_name][img_name] + 1
                save_path =  os.path.join(save_folder, class_name)
                save_name = img_name.split('.')[0] + '-' + str(count[class_name][img_name]) + '.jpg'
                io_utils.mkdir(save_path)
                xmin = int(element_obj.find("bndbox").find("xmin").text)  # find bbox boundary
                ymin = int(element_obj.find("bndbox").find("ymin").text)
                xmax = int(element_obj.find("bndbox").find("xmax").text)
                ymax = int(element_obj.find("bndbox").find("ymax").text)
                box = (xmin, ymin, xmax, ymax)
                img = Image.open(new_img_path)
                region = img.crop(box)
                region.save( os.path.join(save_path, save_name))
        except Exception as e:
            print('Exception: {}'.format(e))
            continue

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-d', '--datadir',help='the parent folder of data', default='/home/syh/train_data/data/')
args = parser.parse_args()

if __name__=="__main__":
    input_path = args.datadir
    null_dict=dict_init(input_path)
    count_and_cut(input_path,null_dict)