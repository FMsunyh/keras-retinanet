
from __future__ import print_function

# This is a placeholder for a Google-internal import.

import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
import grpc.beta.implementations
from grpc._cython import cygrpc
import PIL
import numpy as np
import cv2
import keras

tf.app.flags.DEFINE_string('server', '0.0.0.0:9000','PredictionService host:port')
tf.app.flags.DEFINE_string('image', '/home/syh/RetinaNet/data/train_data-2018-03-30/JPEGImages/train_20180330_1018.jpg', 'path to image in JPEG format')
FLAGS = tf.app.flags.FLAGS


def read_image_bgr(path):
    im = PIL.Image.open(path)
    im_rgb = im.convert('RGB')
    image = np.asarray(im_rgb)
    return image[:, :, ::-1].copy() # RGB  ->BGR

def preprocess_image(x):
    # mostly identical to "https://github.com/fchollet/keras/blob/master/keras/applications/imagenet_utils.py"
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
    print(img.shape)
    smallest_side = min(rows, cols)

    # rescale the image so the smallest side is min_side
    scale = min_side*1.0 / smallest_side

    # check if the largest side is now greater than max_side, wich can happen
    # when images have a large aspect ratio
    largest_side = max(rows, cols)
    if largest_side * scale > max_side:
        scale = max_side*1.0 / largest_side

    # resize the image with the computed scale
    img = cv2.resize(img, None, fx=scale, fy=scale)

    return img, scale

def visualize(predicted_labels, scores, detections):
    for idx, (label, score) in enumerate(zip(predicted_labels, scores)):
        if score < 0.3:
            continue
        b = detections[0, idx, :4].astype(int)

        print(b)
        print(label)


def insecure_channel(host, port):
        channel = grpc.insecure_channel(
            target=host if port is None else '%s:%d' % (host, port),
            options=[(cygrpc.ChannelArgKey.max_send_message_length, -1),
                     (cygrpc.ChannelArgKey.max_receive_message_length, -1)])
        return grpc.beta.implementations.Channel(channel)

def main(_):
  host, port = FLAGS.server.split(':')
  print(host)
  print(port)
  channel = insecure_channel(host, int(port))
  stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
  # Send request
  image = read_image_bgr(FLAGS.image)
  image = preprocess_image(image)
  image, scale = resize_image(image)
  image = np.expand_dims(image, axis=0)
  print(image.shape)
  # See prediction_service.proto for gRPC request/response details.
  request = predict_pb2.PredictRequest()
  request.model_spec.name = 'tt'
  request.model_spec.signature_name = 'predict'
  # request.inputs['image'].CopyFrom(tf.contrib.util.make_tensor_proto(data, shape=[1]))
  request.inputs['image'].CopyFrom(tf.contrib.util.make_tensor_proto(image))
  result = stub.Predict(request, 10.0)  # 10 secs timeout
  # predicted_labels = np.argmax(result[0, :, 4:], axis=1)
  detections = tf.make_ndarray(result.outputs['detections'])

  predicted_labels = np.argmax(detections[0, :, 4:], axis=1)
  scores = detections[0, np.arange(detections.shape[1]), 4 + predicted_labels]
  # correct for image scale
  detections[0, :, :4] /= scale*1.0

  # return predicted_labels, scores, detections
  visualize(predicted_labels, scores, detections)
  # print(predicted_labels)




if __name__ == '__main__':
  tf.app.run()

"""
https://stackoverflow.com/questions/46753508/tensorflow-serving-response
"""