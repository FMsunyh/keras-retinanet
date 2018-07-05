# -*- coding: utf-8 -*-
# @Time    : 5/30/2018 2:26 PM
# @Author  : sunyonghai
# @File    : six2one2.py
# @Software: ZJ_AI
import argparse
import itertools
import json
import logging
import os
import random
from xml.dom.minidom import parseString
import cv2
import numpy as np
from PIL import Image
from lxml.etree import Element, SubElement, tostring

import config
import io_utils

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def _read_class_mapping(path):
    with open(path, 'r') as f:
        # names_to_labels
        data = json.load(f)
    return data

def names_to_labels():
    result = _read_class_mapping(config.LABEL_MAPPING_PATH)
    return result

voc_classes = names_to_labels()
classes  = voc_classes
labels = {}
for key, value in classes.items():
    labels[value] = key

def num_classes():
    return len(classes)

def name_to_label(name):
    return int(classes[name])

def label_to_name(label):
    return labels[label]

def resize_image(img, grid_width=100, grid_height=100):
    if img == None or grid_width <=0 or grid_height <=0:
        return
    img = np.asarray(img)
    (w, h, _) = img.shape
    scale = random.random()
    scale = 0.5 if scale < 0.5 else scale
    try:
        while (w > grid_width or h > grid_height):
            img = cv2.resize(img, (int(w*scale), int(h*scale)))
            (h, w, _) = img.shape
    except Exception as ex:
        logger.error('{}'.format(ex))

    return img

def read_image_rgb(path):
    try:
        image = Image.open(path)
    except Exception as ex:
        logger.error('{}'.format(path))

    return image.copy()

def load_bg(path):
    return read_image_rgb(path)

def load_image(image_index):
    path = labels_images_paths[image_index][1]
    return read_image_rgb(path)

def load_image_group(group):
    return [load_image(image_index) for image_index in group]

def labels_image_paths(labels_images_dir):
    labels_image_paths ={}
    try:
        for f in os.listdir(labels_images_dir):
            sub_folder = os.path.join(labels_images_dir, f)
            for label_img in os.listdir(sub_folder):
                key = '{}:{}'.format(f, label_img)
                value = os.path.join(labels_images_dir, sub_folder, label_img)
                labels_image_paths[key] = value
    except Exception as ex :
        logging.info('labels_image_paths convert error:\n{}'.format(ex))
    return sorted(labels_image_paths.items(), key=lambda item: item[0])

def background(bg_dir):
    bg_paths=[]
    try:
        for bg_file in os.listdir(bg_dir):
            bg_path = os.path.join(bg_dir, bg_file)
            bg_paths.append(bg_path)
    except Exception as ex:
        logger.info('{}'.format(ex))

    return bg_paths

def group_images(lenght):
    order = list(range(lenght))
    random.shuffle(order)
    # divide into groups, one group = one batch
    groups = [[order[x % len(order)] for x in range(i, i + batch_size)] for i in range(0, len(order), batch_size)]

    return groups

def preprocess_image(image):
    return image

def random_transform(image):
    return image

def preprocess_group_entry(image):
    # preprocess the image
    image = preprocess_image(image)

    # randomly transform image and annotations
    image = random_transform(image)

    return image

def preprocess_group(image_group):
    for index, image in enumerate(image_group):
        # preprocess a single group entry
        image = preprocess_group_entry(image)

        # copy processed data back to group
        image_group[index]  = image

    return image_group

def calu_box(image, xmin, ymin):
    box = np.zeros((1, 5),dtype=np.int)

    xmax = xmin + image.size[0]
    ymax = ymin + image.size[1]
    box[0, 0] = int(xmin)
    box[0, 1] = int(ymin)
    box[0, 2] = int(xmax)
    box[0, 3] = int(ymax)

    return box

def fusion(bg_img, image_group, group):

    if bg_img == None:
        return None, None

    fusion_img = bg_img.copy()
    boxes = np.zeros((0, 5), dtype=np.int)
    grid_width, grid_height = fusion_img.size[0]//(batch_size//2), fusion_img.size[1]//2

    row, col = 0, 0
    for idx, image in enumerate(image_group):
        img = resize_image(image, grid_width * ratio, grid_height* ratio)
        xmin = grid_width * col + grid_width * (1 - ratio)
        ymin = grid_height * row + grid_height * (1 - ratio)

        img = Image.fromarray(img)
        box = calu_box(img, xmin, ymin)

        class_name = labels_images_paths[group[idx]][0]
        label = name_to_label(class_name.split(':')[0])
        box[0, 4] = label

        temp_box = [box[0,0],box[0,1]]
        fusion_img.paste(img, temp_box)

        boxes = np.append(boxes, box, axis=0)
        col+=1
        if(col == batch_size//2):
            row+=1
            col=0

    return fusion_img, boxes

def next_group():
    global group_index
    if group_index == 0:
        # shuffle groups at start of epoch
        random.shuffle(groups)
    group = groups[group_index]
    group_index = (group_index + 1) % len(groups)
    return group

def next_bg():
    curr_bg = next(bg_paths_cycle)
    return curr_bg

def next_fusion_name():
    global  name
    str_name = "fusion" + "_" + '2018-05-31' + "_" + str(name)
    name+=1
    return str_name

def print_name(i):
    print(next_fusion_name())

# save data(image and annotations)
def save_image(name, image):
    try:
        path =os.path.join(output,'JPEGImages', name+".jpg")
        image.save(path, 'jpeg')
    except Exception as ex:
        logger.error('{}\n{}'.format(ex, path))

def save_annotations(name, size, annotations):
    dom = create_xml(name, size, annotations)
    write_xml(name, dom)

def check_border(bbox, width, height):
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

def create_xml(name, size, annotations):
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'JPEGImages'
    node_filename = SubElement(node_root, 'filename')
    filename = name + ".jpg"
    node_filename.text = filename

    node_path = SubElement(node_root, 'path')
    node_path.text = ''

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(size[0])

    node_height = SubElement(node_size, 'height')
    node_height.text = str(size[1])

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = str(3)

    node_segmented = SubElement(node_root, 'segmented')
    node_segmented.text = '0'

    for box in annotations:

        check_border(box, size[0],size[1])

        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        caption = labels[box[4]]
        node_name.text = caption

        node_pose = SubElement(node_object, 'pose')
        node_pose.text = 'Unspecified'

        node_truncated = SubElement(node_object, 'truncated')
        node_truncated.text = '0'

        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'

        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(int(box[0]))

        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(int(box[1]))

        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(int(box[2]))

        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(int(box[3]))

    xml = tostring(node_root, pretty_print=True)
    dom = parseString(xml)

    return dom

def write_xml(name, dom):
    filename = name + '.xml'
    xml_path = os.path.join(output, 'Annotations', filename)
    with open(xml_path, 'w+') as f:
        dom.writexml(f, addindent='', newl='', encoding='utf-8')


def process():
    # load bg
    bg_image = load_bg(next_bg())

    # load group(six label image)
    group = next_group()
    image_group = load_image_group(group)

    # start preprocess
    image_group = preprocess_group(image_group)

    # fusion
    fusion_img, boxes = fusion(bg_image,image_group, group)

    if fusion_img is not None and boxes is not None:
        # save image
        name = next_fusion_name()
        save_image(name, fusion_img)

        # save annotations
        save_annotations(name, fusion_img.size, boxes)

        # finish
        logger.info('{} save successfully'.format(name))

    else:
        logger.info('{}'.format('bag bg'))

def single_process():
    global steps, Epochs
    for _ in range(Epochs):
        for _ in range(steps):
            process()


parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-b', '--bg',help='directory of data path', default= '/home/syh/train_data/fusion/background_1333-800')
parser.add_argument('-c', '--crop_commdity',help='txt of path', default= '/home/syh/train_data/data/crop_commdity')
parser.add_argument('-o', '--output',help='output diretory', default='/home/syh/train_data/fusion/fusion_train_data')

# # Test data
# parser.add_argument('-b', '--bg',help='directory of data path', default= '/home/syh/train_data/fusion_test/background')
# parser.add_argument('-c', '--crop_commdity',help='txt of path', default= '/home/syh/train_data/fusion_test/crop_commdity')
# parser.add_argument('-o', '--output',help='output diretory', default='/home/syh/train_data/fusion_test/fusion_train_data')

args = parser.parse_args()

ratio = 0.9
bg_index = 0
group_index = 0
batch_size = 4
name = 80000
counter = 0
labels_images_dir = args.crop_commdity
bg_dir = args.bg
bg_paths = background(bg_dir)
bg_paths_cycle = itertools.cycle(bg_paths)

labels_images_paths = labels_image_paths(labels_images_dir)
groups = group_images(len(labels_images_paths))
output= args.output

Epochs = 1
steps = len(bg_paths)

def main():

    JPEGImages_dir = os.path.join(output, 'JPEGImages')
    Annotations_dir = os.path.join(output, 'Annotations')

    if os.path.exists(JPEGImages_dir):
        # io_utils.remove_all(JPEGImages_dir)
        pass
    else:
        io_utils.mkdir(JPEGImages_dir)

    if os.path.exists(Annotations_dir):
        # io_utils.remove_all(Annotations_dir)
        pass
    else:
        io_utils.mkdir(Annotations_dir)

    single_process()

if __name__ == '__main__':
    main()