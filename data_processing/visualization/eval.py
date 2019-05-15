"""
Copyright 2017-2018 Fizyr (https://fizyr.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import print_function

import json

import numpy as np
import os

import cv2
import pickle

from visualization.visualization import draw_annotations


def _compute_input(generator, index):
    raw_image = generator.load_image(index)
    image = generator.preprocess_image(raw_image.copy())
    image, scale = generator.resize_image(image)

    return raw_image, image, scale, raw_image.shape[0:2]

def draw(generator, save_path=None):
    for i in range(generator.size()):
        raw_image = generator.load_image(i)
        draw_annotations(raw_image, generator.load_annotations(i), label_to_name=generator.label_to_name)
        cv2.imwrite(os.path.join(save_path, '{}.png'.format(str(i).zfill(4))), raw_image)

        print('{}/{}'.format(i, generator.size()), end='\r')

if __name__ == '__main__':
    draw(generator, save_path=None)
