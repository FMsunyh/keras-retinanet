#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 4/8/2018 6:35 PM 
# @Author : sunyonghai 
# @File : commdity_load_model.py 
# @Software: ZJ_AI
# =========================================================

import keras
import shutil
from keras import Model
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

from config import MODEL_PATH, ROOT_HOME
from keras_retinanet.models.resnet import custom_objects
import tensorflow as tf
import os
import sys
from keras import backend as K

tf.app.flags.DEFINE_integer('model_version', 1, 'version number of the model.')
FLAGS = tf.app.flags.FLAGS

signature_key = 'predict'
input_key = 'image'
output_key = 'detections'

export_path_base = 'deploy/serving_model'
export_path = os.path.join(
    tf.compat.as_bytes(ROOT_HOME),
    tf.compat.as_bytes(export_path_base),
    tf.compat.as_bytes(str(FLAGS.model_version)))

with K.get_session() as sess:
    meta_graph_def = tf.saved_model.loader.load(sess,  [tf.saved_model.tag_constants.SERVING], export_path)
    # 从meta_graph_def中取出SignatureDef对象
    signature = meta_graph_def.signature_def

    # 从signature中找出具体输入输出的tensor name
    x_tensor_name = signature[signature_key].inputs[input_key].name
    y_tensor_name = signature[signature_key].outputs[output_key].name

    # 获取tensor 并inference
    x = sess.graph.get_tensor_by_name(x_tensor_name)
    y = sess.graph.get_tensor_by_name(y_tensor_name)

    # _x 实际输入待inference的data
    # sess.run(y, feed_dict={x:_x})
