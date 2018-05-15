#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/28/2018 6:29 PM 
# @Author : sunyonghai 
# @File : label.py 
# @Software: ZJ_AI
# =========================================================
import json
from config import LABEL_MAPPING_PATH

def _write_class_mapping(path):
    with open(path, 'w+') as f:
        json.dump(labels_to_names, f, sort_keys=True)
        print('save the classs mapping.')

def _read_class_mapping(path):
    with open(path, 'r') as f:
        # names_to_labels
        data = json.load(f)
        # pprint('mapping info:', labels_to_names)
    return data

def names_to_labels():
    result = _read_class_mapping(LABEL_MAPPING_PATH)
    return result

def labels_to_names():
    labels_to_names = _read_class_mapping(LABEL_MAPPING_PATH)
    result = {value:key for key, value in labels_to_names.items()}
    return result