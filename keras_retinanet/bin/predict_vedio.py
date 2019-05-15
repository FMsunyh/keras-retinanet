#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/26/2018 11:56 AM
# @Author : sunyonghai
# @File : test.py
# @Software: ZJ_AI
# =========================================================
import argparse
import json
import os
from pprint import pprint

import cv2
import tensorflow as tf
import keras
import time
import numpy as np
from PIL import Image

import keras_retinanet.models
from keras_retinanet.utils.label import labels_to_names

from keras_retinanet.utils.colors import label_color
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from data_processing.io_utils import *
from keras_retinanet.utils.visualization import draw_box, draw_caption
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString


from config import MODEL_PATH, ROOT_HOME

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-m', '--model_file',help='model path', default='')
args = parser.parse_args()

MODEL_PATH = args.model_file

threshold = 0.5

Debug = True
def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

keras.backend.tensorflow_backend.set_session(get_session())


# load label to names mapping for visualization purposes
labels_to_names = labels_to_names()

def load_model(load=False):
    if load:
        try:
            print('loading the model...............')
            model = keras_retinanet.models.load_model(MODEL_PATH, backbone_name='resnet50',convert=True)
            image_path = '/home/syh/commdity_recognition/development/server/static/download/train_20180307_1725.jpg'
            image = read_image_bgr(image_path)
            image = preprocess_image(image)
            image, scale = resize_image(image)
            model.predict_on_batch(np.expand_dims(image, axis=0))
            print('finished load the model...............')

            # print(model.summary())
        except ImportError as ex:
            print("Can't load the model: %s" % ex)
    else:
        return None

    return model

model = load_model(load=True)

def predict(image):
    image = preprocess_image(image)
    image, scale = resize_image(image)

    # process image
    start = time.time()
    boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
    # print("processing time: ", str(1000 * (time.time() - start)) + " ms")

    # correct for image scale
    boxes /= scale

    return boxes, scores, labels


def visualize(draw, boxes, scores, labels):
    for box, score, label in zip(boxes[0], scores[0], labels[0]):
        # scores are sorted so we can break
        if score < threshold:
            break

        color = label_color(label)

        draw_box(draw, box, color=color)

        caption = "{} {:.3f}".format(labels_to_names[label], score)
        draw_caption(draw, box, caption)

    return draw

    # return True
def pipeline(image):
    boxes, scores, labels = predict(image)
    draw = image.copy()
    draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
    image_draw = visualize(draw, boxes, scores, labels)
    return image_draw

def main():
    count_frame, process_every_n_frame = 0, 4
    # get camera device
    cap = cv2.VideoCapture(0)

    while (True):
        # get a frame
        ret, frame = cap.read()
        count_frame += 1

        # show a frame
        img = cv2.resize(frame, (0, 0), fx=1, fy=1)  # resize image half
        cv2.imshow("Video", img)

        # if running slow on your computer, try process_every_n_frame = 10
        if count_frame % process_every_n_frame == 0:
            img_bbox = pipeline(img)
            # cv2.imshow("BGR", pipeline(img))

            imgcopy = img_bbox[:, :, ::-1].copy()
            cv2.imshow("predict", imgcopy)

        # press keyboard 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()