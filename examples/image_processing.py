#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/23/2018 2:40 PM 
# @Author : sunyonghai 
# @File : image_processing.py 
# @Software: ZJ_AI
# =========================================================
import cv2

from keras_retinanet.utils.image import resize_image

if __name__ == '__main__':
    img = cv2.imread('train_20180319_1424.jpg')
    img,_ = resize_image(img)
    cv2.imwrite('train_20180319_1424_resize.jpg', img)