#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/28/2018 5:54 PM 
# @Author : sunyonghai 
# @File : config.py 
# @Software: ZJ_AI
# =========================================================
import os

ROOT_HOME =  os.path.expanduser('~/RetinaNet/')
# LABEL_MAPPING_PATH = os.path.join(ROOT_HOME,'mapping_54.json')
# LABEL_MAPPING_PATH = os.path.join(ROOT_HOME,'mapping_all.json')
LABEL_MAPPING_PATH = os.path.join(ROOT_HOME,'name_to_label.json')
# LABEL_MAPPING_PATH = os.path.join(ROOT_HOME,'mapping_300.json')
# LABEL_MAPPING_PATH = os.path.join(ROOT_HOME,'mapping_11.json')
MODEL_PATH =os.path.join(ROOT_HOME,'model','resnet101_pascal_01.h5')

TRAIN_DATA = '/disk2/train'

class Phase(object):
    def __init__(self,class_num):
        self.class_num = class_num

# TEST_DATA_DIR = os.path.join(ROOT_HOME,'data/test/images/')
# TEST_RESULT_DIR = os.path.join(ROOT_HOME,'data/test/results/')
# TEST_ANNOTATION_DIR = os.path.join(ROOT_HOME,'data/test/annotations/')


# DATA_DIR = 'data/train_data-2018-03-30'
# TEST_DATA_DIR = os.path.join(ROOT_HOME, DATA_DIR, 'JPEGImages/')
# TEST_RESULT_DIR = os.path.join(ROOT_HOME,DATA_DIR, 'results/')
# TEST_ANNOTATION_DIR = os.path.join(ROOT_HOME,DATA_DIR, 'Annotations/')