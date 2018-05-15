#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 4/8/2018 1:52 PM 
# @Author : sunyonghai 
# @File : commdity_save_model.py 
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

tf.app.flags.DEFINE_integer('training_iteration', 1000,
                            'number of training iterations.')
tf.app.flags.DEFINE_integer('model_version', 1, 'version number of the model.')
tf.app.flags.DEFINE_string('work_dir', '/tmp', 'Working directory.')
FLAGS = tf.app.flags.FLAGS

model = keras.models.load_model(MODEL_PATH, custom_objects=custom_objects)
if (model.uses_learning_phase):
        raise ValueError('Model using learning phase.')

print('******************************model.input*******************************')
print(model.input)
print('******************************model.output*******************************')
print(model.output)

# config = model.get_config()
# weights = model.get_weights()
# new_model = Model.from_config(config)
# new_model.set_weights(weights)

# print(model.summary())
# print('-------------------------')
# print(model.output)


# export_path_base = sys.argv[-1]
export_path_base = 'deploy/serving_model'
export_path = os.path.join(
    tf.compat.as_bytes(ROOT_HOME),
    tf.compat.as_bytes(export_path_base),
    tf.compat.as_bytes(str(FLAGS.model_version)))
print('Exporting trained model to', export_path)
if os.path.isdir(os.path.join(ROOT_HOME,export_path_base)):
    shutil.rmtree(os.path.join(ROOT_HOME,export_path_base))

builder = tf.saved_model.builder.SavedModelBuilder(export_path)
legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')

init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())

signature = predict_signature_def(inputs={'image': model.input},
                                  outputs={'detections': model.output[2]})

with K.get_session() as sess:
    sess.run(init_op)

    builder.add_meta_graph_and_variables(
        sess, [tf.saved_model.tag_constants.SERVING],
        signature_def_map={'predict': signature},
        legacy_init_op=legacy_init_op)
    builder.save(True)

print('Finished export', export_path)
