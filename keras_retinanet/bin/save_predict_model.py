# -*- coding: utf-8 -*-
# @Time    : 5/16/2018 2:16 PM
# @Author  : sunyonghai
# @File    : save_predict_model.py
# @Software: ZJ_AI
# =========================================================
import argparse
import keras
import os
import tensorflow as tf
import keras_retinanet.models
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

keras.backend.tensorflow_backend.set_session(get_session())

def save_model(path):
    model.save(path)
    logger.info('save the model to :{}'.format(path))

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-m', '--weight_file', help='weight path', default='/home/syh/RetinaNet/snapshots/resnet50_pascal_03.h5')
parser.add_argument('-p', '--model_path', help='model path', default='')
parser.add_argument('-n', '--name', help='name path', default='predict_model.h5')
args = parser.parse_args()

path = args.weight_file
model = keras_retinanet.models.load_model(path, backbone_name='resnet50', convert=True, nms=True)

if __name__ == '__main__':

    h5_file = os.path.join('/home/syh/RetinaNet/model_h5', args.name)
    logger.info('read the model to :{}'.format(h5_file))

    save_model(h5_file)
    del model


"""
cd /home/syh/RetinaNet/data_processing
python /home/syh/RetinaNet/keras_retinanet/bin/save_predict_model.py -m /home/syh/RetinaNet/snapshots/resnet50_pascal_03.h5
"""