#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 4/3/2018 4:08 PM 
# @Author : sunyonghai 
# @File : predict_vedio.py 
# @Software: ZJ_AI
# =========================================================

import time

import keras
import numpy as np
import tensorflow as tf

from config import MODEL_PATH, ROOT_HOME
from data_processing.io_utils import *
from keras_retinanet.models.resnet import custom_objects
from keras_retinanet.utils.colors import label_color
from keras_retinanet.utils.image import preprocess_image, resize_image
from keras_retinanet.utils.label import labels_to_names
from keras_retinanet.utils.visualization import draw_box, draw_caption
from moviepy.editor import VideoFileClip

DATA_DIR = 'data/train_data-2018-04-02'
# DATA_DIR = 'data/train_data-2018-03-30'
TEST_DATA_DIR = os.path.join(ROOT_HOME, DATA_DIR, 'JPEGImages/')
TEST_RESULT_DIR = os.path.join(ROOT_HOME,DATA_DIR, 'results/')
TEST_ANNOTATION_DIR = os.path.join(ROOT_HOME,DATA_DIR, 'Annotations/')

Debug = True
def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

keras.backend.tensorflow_backend.set_session(get_session())

project_video_output = './project_video_output.mp4'
clip1 = VideoFileClip("./project_video.mp4")

model = keras.models.load_model(MODEL_PATH, custom_objects=custom_objects)

# load label to names mapping for visualization purposes
labels_to_names = labels_to_names()


def predict(image):
    image = preprocess_image(image)
    image, scale = resize_image(image)

    # process image
    start = time.time()
    _, _, detections = model.predict_on_batch(np.expand_dims(image, axis=0))
    print("processing time: ", str(1000 * (time.time() - start)) + " ms")

    # compute predicted labels and scores
    predicted_labels = np.argmax(detections[0, :, 4:], axis=1)
    scores = detections[0, np.arange(detections.shape[1]), 4 + predicted_labels]

    # correct for image scale
    detections[0, :, :4] /= scale

    return predicted_labels, scores, detections


def visualize(draw, predicted_labels, scores, detections):
    for idx, (label, score) in enumerate(zip(predicted_labels, scores)):
        if score < 0.7:
            continue

        color = label_color(label)

        b = detections[0, idx, :4].astype(int)
        draw_box(draw, b, color=color)

        caption = "{} {:.3f}".format(labels_to_names[label], score)
        draw_caption(draw, b, caption)

    return draw


if __name__ == '__main__':
    pass