# -*- coding: utf-8 -*-
# @Time    : 5/16/2018 2:07 PM
# @Author  : sunyonghai
# @File    : model_predict.py
# @Software: ZJ_AI
import json

import cv2
import os

import keras_resnet
import tensorflow as tf
import keras
import time
import numpy as np
from PIL import Image
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import logging

import keras_retinanet.models.retinanet

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# global variables
THRESHOLD = 0.5
MODEL_PATH = '/home/syh/RetinaNet/model_h5/predict_model.h5'
LABEL_MAPPING_PATH = '/home/syh/RetinaNet/mapping_all.json'

DATA_DIR = '/home/syh/train_data/test'
JPEGIMAGES_DIR = os.path.join(DATA_DIR, 'JPEGImages/')
ANNOTATIONS_DIR = os.path.join(DATA_DIR, 'Annotations/')


def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

keras.backend.tensorflow_backend.set_session(get_session())

def _read_class_mapping(path):
    with open(path, 'r') as f:
        # names_to_labels
        data = json.load(f)
        # pprint('mapping info:', labels_to_names)
    return data

def labels_to_names():
    labels_to_names = _read_class_mapping(LABEL_MAPPING_PATH)
    result = {value:key for key, value in labels_to_names.items()}
    return result

def read_image_bgr(path):
    try:
        image = np.asarray(Image.open(path).convert('RGB'))
    except Exception as ex:
        logger.error('{}'.format(path))

    return image[:, :, ::-1].copy()

def preprocess_image(x):
    # except for converting RGB -> BGR since we assume BGR already
    x = x.astype(keras.backend.floatx())
    if keras.backend.image_data_format() == 'channels_first':
        if x.ndim == 3:
            x[0, :, :] -= 103.939
            x[1, :, :] -= 116.779
            x[2, :, :] -= 123.68
        else:
            x[:, 0, :, :] -= 103.939
            x[:, 1, :, :] -= 116.779
            x[:, 2, :, :] -= 123.68
    else:
        x[..., 0] -= 103.939
        x[..., 1] -= 116.779
        x[..., 2] -= 123.68

    return x

def resize_image(img, min_side=800, max_side=1333):
    (rows, cols, _) = img.shape

    smallest_side = min(rows, cols)

    # rescale the image so the smallest side is min_side
    scale = min_side / smallest_side

    # check if the largest side is now greater than max_side, which can happen
    # when images have a large aspect ratio
    largest_side = max(rows, cols)
    if largest_side * scale > max_side:
        scale = max_side / largest_side

    # resize the image with the computed scale
    img = cv2.resize(img, None, fx=scale, fy=scale)

    return img, scale


def check_border(bbox, width, height):
    '''
    Check the bbox
    :param bbox:
    :param width:
    :param height:
    :return:
    '''
    if len(bbox) <4:
        return

    if bbox[0] <= 0.0:
        bbox[0]= 1

    if bbox[1] <= 0.0:
        bbox[1] = 1

    if bbox[2] >= width:
        bbox[2] = width - 1

    if bbox[3] >= height:
        bbox[3] = height - 1

def make_xml(im_info, boxes, scores, labels):
    '''
    Create a annotation xml file base on parameters.
    :param im_info:
    :param boxes:
    :param scores:
    :param labels:
    :return:
    '''
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'JPEGImages'
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = im_info.name + '.' +im_info.image_extension

    node_path = SubElement(node_root, 'path')
    node_path.text = im_info.path

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text =str(im_info.width)

    node_height = SubElement(node_size, 'height')
    node_height.text =str(im_info.height)

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = str(im_info.channel)

    node_segmented = SubElement(node_root, 'segmented')
    node_segmented.text = '0'

    for b, score, label in zip(boxes[0], scores[0], labels[0]):
        if score < THRESHOLD:
            break

        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        caption = "{}".format(labels_to_names[label])
        node_name.text = caption

        node_pose = SubElement(node_object, 'pose')
        node_pose.text = 'Unspecified'

        node_truncated = SubElement(node_object, 'truncated')
        node_truncated.text = '0'

        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'

        check_border(b, im_info.width,im_info.height)

        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(int(b[0]))

        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(int(b[1]))

        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(int(b[2]))

        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(int(b[3]))

    xml = tostring(node_root, pretty_print=True)
    dom = parseString(xml)

    return dom

def save_annotations(save_dir, im_info, boxes, scores, labels):
    '''
    Save all files.
    :param save_dir:
    :param im_info:
    :param boxes:
    :param scores:
    :param labels:
    :return:
    '''
    dom = make_xml(im_info, boxes, scores, labels)
    xml_path = os.path.join(save_dir, im_info.name + '.xml')
    with open(xml_path, 'w+') as f:
        dom.writexml(f, addindent='', newl='', encoding='utf-8')

class ImageInfo(object):
    def __init__(self, name='', path='', image_extension='.jpg', image_bgr=None):
        self.name = name # not include extension
        self.path = path
        self.image_extension = image_extension
        self.image_bgr = image_bgr
        self.width=0
        self.height=0
        self.channel=3


def get_imageinfos(image_dir):
    if image_dir == '':
        return []

    imageinfos =[]

    for s in os.listdir(image_dir):
        name = s.split('.')[0]
        extension = s.split('.')[1]
        path = os.path.join(image_dir, s)
        # im = read_image_bgr(path)
        im = path
        im_info = ImageInfo(name=name, path=path, image_extension=extension, image_bgr=im)
        imageinfos.append(im_info)

    print('Read the images.Finished!')
    return imageinfos


def predict_imageinfo(imageinfos):

    if len(imageinfos)<=0:
        return

    print('start predict.....................')
    for item in imageinfos:
        # image = item.image_bgr
        image = read_image_bgr(item.path)
        item.width = image.shape[1]
        item.height = image.shape[0]
        item.channel = image.shape[2]
        boxes, scores, labels = predict(image)
        save_annotations(ANNOTATIONS_DIR, item, boxes, scores, labels)

def predict(image):
    image = preprocess_image(image)
    image, scale = resize_image(image)

    # process image
    start = time.time()
    boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
    logger.info('processing time: {}'.format(str(1000 * (time.time() - start)) + " ms"))

    # correct for image scale
    boxes /= scale

    return boxes, scores, labels

if __name__ == '__main__':
    # custom_objects = keras_retinanet.models.retinanet.custom_objects.copy()
    #
    # custom_objects.update(keras_resnet.custom_objects)
    #
    model = keras.models.load_model(MODEL_PATH, custom_objects=keras_resnet.custom_objects)
    if model is not None:
        imageinfos = get_imageinfos(DATA_DIR)
        if not os.path.exists(ANNOTATIONS_DIR):
            os.makedirs(ANNOTATIONS_DIR)

        predict_imageinfo(imageinfos)