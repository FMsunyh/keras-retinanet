# -*- coding: utf-8 -*-
# @Time    : 5/25/2018 7:53 PM
# @Author  : sunyonghai
# @File    : check_label.py
# @Software: ZJ_AI
import json
import os
import xml.etree.ElementTree as ET

import config


def read_xml_label(data_path):
    print('Parsing annotation files')
    annot_path = os.path.join(data_path, 'Annotations')
    annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
    for annot in annots:
        try:
            et = ET.parse(annot)
            element = et.getroot()

            element_objs = element.findall('object')

            for element_obj in element_objs:
                node = element_obj.find('name')
                # print(node.text)
                class_name = element_obj.find('name').text

                if class_name not in label_mapping:
                    print(annot, class_name)

        except Exception as e:
            print('Exception in pascal_voc_parser: {}'.format(e))
            continue


def read_label_mapping(path):
    with open(path, 'r') as f:
        # names_to_labels
        data = json.load(f)
        # pprint('mapping info:', labels_to_names)
    return data

if __name__ == '__main__':
    label_mapping = read_label_mapping(config.LABEL_MAPPING_PATH)
    input_path = '/home/syh/train_data/data/all_train_data2'
    read_xml_label(input_path)
    # if 'yd-ydwtkxt-hz-rdsgw-32g' in label_mapping_d:
    #     print('yes')
