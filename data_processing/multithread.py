# -*- coding: utf-8 -*-
# @Time    : 5/15/2018 2:42 PM
# @Author  : sunyonghai
# @File    : multithread.py
# @Software: ZJ_AI
import random
import threading
import queue
import numpy as np
import time
from PIL import Image
import os

class Generator(object):
    def __init__(self):
        self.q = queue.Queue(maxsize=5)
        p = threading.Thread(target=self.producer, args=())
        # c = threading.Thread(target=self.consumer, args=())
        p.start()
        # c.start()
        self.count=0

    def read_image_bgr(self,path):
        try:
            image = np.asarray(Image.open(path).convert('RGB'))
            if image is None:
                raise Exception("Invalid image!", path)
        except Exception as ex:
            print(path)
            print(ex)
        return image[:, :, ::-1].copy()

    # self.q = self.manager.Queue(maxsize=3)
    def producer(self):
        while True:
            try:
                path = '/home/syh/train_data/all_train_data/JPEGImages/train_2018329_1552.jpg'
                value = self.read_image_bgr(path)
                self.q.put((2,3))
                # print(self.q.qsize())
                time.sleep(random.randrange(3))
            except Exception as ex:
                print(ex)

    def consumer(self):
        try:
            # print('-1')
            value = self.q.get(True)
            # print(self.count)
            time.sleep(random.randrange(4))
            return value
        except Exception as ex:
            print(ex)

    def next(self):
        value= self.consumer()
        print(value)
        return value

    def fun(self):
        return 2,3
if __name__ == '__main__':
    gen = Generator()
    while True:
        a = gen.fun()
        gen.next()
