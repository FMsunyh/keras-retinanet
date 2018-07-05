# -*- coding: utf-8 -*-
# @Time    : 7/2/2018 3:44 PM
# @Author  : sunyonghai
# @File    : fix_label.py
# @Software: ZJ_AI
import xml_utils
import os
import xml.etree.ElementTree as ET

def modify_label_name(input_path):
    print('Parsing annotation files')
    annot_path = os.path.join(input_path, 'Annotations')
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
                if class_name == 'ly-hlydhp-hz-yw-138g':     # 1
                    node.text = 'hly-hlydhp-hz-yw-138g'
                    print(annot)

            xml_utils.write_xml(et, annot)
        except Exception as e:
            print('Exception in pascal_voc_parser: {}'.format(e))
            continue

if __name__ == '__main__':
    input_path = '/home/syh/train_data/data/aug-all_train_data'
    modify_label_name(input_path)