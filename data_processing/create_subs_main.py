# -*- coding: utf-8 -*-
# @Time    : 5/29/2018 3:35 PM
# @Author  : sunyonghai
# @File    : create_subs_main.py
# @Software: ZJ_AI
import random
import os
from data_processing.io_utils import mkdir

def _create_Main(path):
    '''
    create the trainval.txt and test.txt for train.
    trainval data : test data = 5:1
    :param path:
    :return:
    '''
    scale = 10
    image_dir = os.path.join(path, 'JPEGImages')
    anno_dir = os.path.join(path, 'Annotations')
    ImageSets_path = os.path.join(path, 'ImageSets')
    main_dir = os.path.join(ImageSets_path, 'Main')

    mkdir(main_dir)

    imgs = os.listdir(image_dir)
    random.shuffle(imgs)

    trainval_test_images = []
    trainval_images = []
    test_images = []

    for i in range(len(imgs)):
        s = imgs[i]
        trainval_test_images.append(s.split('.')[0] + '\n')

    for i in range(len(imgs)//scale, len(imgs)):
        s = imgs[i]
        trainval_images.append(s.split('.')[0] + '\n')

    for i in range(len(imgs)//scale):
        s = imgs[i]
        test_images.append(s.split('.')[0] + '\n')

    with open(main_dir+'/trainval_test.txt','w+') as f:
        f.writelines(trainval_test_images)
        print("{}, numbers:{}".format(main_dir + '/trainval_test.txt', len(trainval_test_images)))

    with open(main_dir+'/trainval.txt','w+') as f:
        f.writelines(trainval_images)
        print("{}, numbers:{}".format(main_dir + '/trainval.txt', len(trainval_images)))
    with open(main_dir+'/test.txt','w+') as f:
        f.writelines(test_images)
        print("{}, numbers:{}".format(main_dir + '/test.txt', len(test_images)))

    print('total: {}'.format(len(imgs)))
    print('step: {}'.format(len(trainval_images)//2+1))

    return trainval_test_images, trainval_images, test_images

def create_txt(data_dir):
    return _create_Main(data_dir)

def create_txts(data_dirs):
    trainval_tests = []
    trainvals = []
    tests = []
    for data_dir in data_dirs:
        a, b, c =  create_txt(data_dir)
        trainval_tests.append(a)
        trainvals.append(b)
        tests.append(c)

    return trainval_tests, trainvals, tests

def save_subs(trainval_tests, trainvals, tests):
    path = '/home/syh/RetinaNet/data_processing/ImageSets/Main'
    mkdir(path)

    trainval_test_path = os.path.join(path, 'trainval_test.txt')
    trainval_path = os.path.join(path, 'trainval.txt')
    test_path = os.path.join(path, 'test.txt')
    with open(trainval_test_path, 'w+') as f:
        for item in trainval_tests:
            f.writelines(item)
        print("{}".format(trainval_test_path))

    with open(trainval_path, 'w+') as f:
        for item in trainvals:
            f.writelines(item)
        print("{}".format(trainval_path))

    with open(test_path, 'w+') as f:
        for item in tests:
            f.writelines(item)
        print("{}".format(test_path))


if __name__ == "__main__":
    # data_dir = '/home/syh/disk/train/all_train_data'

    base_dir = '/home/syh/train_data/data/sub_train_data'
    # data_folders = ['train_data-2018-05-02'
    #     , 'train_data-2018-05-03'
    #     , 'train_data-2018-05-04'
    #     , 'train_data-2018-05-07'
    #     , 'train_data-2018-05-08'
    #     , 'train_data-2018-05-10'
    #     , 'train_data-2018-05-11'
    #     , 'train_data-2018-05-14'
    #     , 'train_data-2018-05-15']

    # data_folders = ['train_data-2018-03-07'
    #     , 'train_data-2018-03-16'
    #     , 'train_data-2018-03-19'
    #     , 'train_data-2018-03-30'
    #     , 'train_data-2018-04-02'
    #     , 'train_data-2018-04-09'
    #     , 'train_data-2018-04-11'
    #     , 'train_data-2018-04-12'
    #     , 'train_data-2018-04-18'
    #     , 'train_data-2018-04-19'
    #     , 'train_data-2018-04-20'
    #     , 'train_data-2018-04-21'
    #     , 'train_data-2018-04-25'
    #     , 'train_data-2018-04-26'
    #     , 'train_data-2018-04-27'
    #     , 'train_data-2018-05-15'
    #     ]

    data_folders = [
        'train_data-2018-05-04'
        , 'train_data-2018-05-07'
        , 'train_data-2018-05-08'
        , 'train_data-2018-05-10'
        , 'train_data-2018-05-11'
        , 'train_data-2018-05-14'
        , 'train_data-2018-05-15']

    data_dirs = [os.path.join(base_dir, folder) for folder in data_folders]
    # data_dir = '/home/syh/all_train_data'
    a,b,c =  create_txts(data_dirs)
    save_subs(a,b,c)

"""
cd ~/RetinaNet/data_processing
python create_subs_main.py -d /home/syh/train_data/data/sub_train_data/train_data-2018-05-11

cp -r /home/syh/RetinaNet/data_processing/ImageSets/*  ~/train_data/data/all_train_data/ImageSets/

"""