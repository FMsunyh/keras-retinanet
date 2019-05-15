# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 8/14/2018 9:00 AM
# @Author  : sunyonghai
# @Software: ZJ_AI
# -----------------------------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import json

path = '/home/syh/RetinaNet/class_mapping/mapping_all.json'
out_path = '/home/syh/RetinaNet/class_mapping/mapping_300.json'

def _read_class_mapping(path):
    with open(path, 'r') as f:
        # names_to_labels
        data = json.load(f)
        # pprint('mapping info:', labels_to_names)
    return data

def _append(data):
    if isinstance(data,dict):
        a = len(data)
        while a < 300:
            data.setdefault('class_'+str(a), a)
            a=a+1

def _write_class_mapping(path, data):
    with open(path, 'w+') as f:
        json.dump(data, f, sort_keys=True)
        print('save the classs mapping.')

if __name__ == '__main__':
    data = _read_class_mapping(path)
    _append(data)
    _write_class_mapping(out_path,data)
    print(data)

