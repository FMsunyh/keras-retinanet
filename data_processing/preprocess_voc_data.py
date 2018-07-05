import argparse
import json
import logging
import multiprocessing.pool
import os
import cv2
import numpy as np
import six
from PIL import Image
import config
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString

import io_utils

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description='Get the data info')
# parser.add_argument('-d', '--datadir', help='path in server', default='/home/syh/train_data/all_train_data')
parser.add_argument('-d', '--datadir', default='/home/syh/train_data/test')
parser.add_argument('-o', '--destdir', default='/home/syh/train_data/test_resize')
parser.add_argument('-t', '--txt', default='trainval_test')
args = parser.parse_args()

def _read_class_mapping(path):
    with open(path, 'r') as f:
        # names_to_labels
        data = json.load(f)
    return data

def names_to_labels():
    result = _read_class_mapping(config.LABEL_MAPPING_PATH)
    return result

voc_classes = names_to_labels()

data_dir             = args.datadir
dest_dir             = args.destdir
set_name             = args.txt
classes              = voc_classes
index                = 0
image_names          = [l.strip().split(None, 1)[0] for l in open(os.path.join(data_dir, 'ImageSets', 'Main', set_name + '.txt')).readlines()]
image_extension      = '.jpg'
skip_truncated       = False
skip_difficult       = False
labels = {}

for key, value in classes.items():
    labels[value] = key

def read_image_rgb(path):
    try:
        image = np.asarray(Image.open(path).convert('RGB'))
    except Exception as ex:
        logger.error('{}'.format(path))

    return image.copy()

def resize_image(img, min_side=800, max_side=1333):
    (rows, cols, _) = img.shape

    smallest_side = min(rows, cols)

    # rescale the image so the smallest side is min_side
    scale = min_side / smallest_side

    # check if the largest side is now greater than max_side, which can happen
    # when images have a large aspect ratio
    largest_side = max(rows, cols)
    if largest_side * scale > max_side:
        scale = max_side / largest_side

    # resize the image with the computed scale
    img = cv2.resize(img, None, fx=scale, fy=scale)

    return img, scale


def _findNode(parent, name, debug_name = None, parse = None):
    if debug_name is None:
        debug_name = name

    result = parent.find(name)
    if result is None:
        raise ValueError('missing element \'{}\''.format(debug_name))
    if parse is not None:
        try:
            return parse(result.text)
        except ValueError as e:
            six.raise_from(ValueError('illegal value for \'{}\': {}'.format(debug_name, e)), None)
    return result

def size():
    return len(image_names)

def num_classes():
    return len(classes)

def name_to_label(name):
    return classes[name]

def label_to_name(label):
    return labels[label]

def load_image(image_index):
    path = os.path.join(data_dir, 'JPEGImages', image_names[image_index] + image_extension)
    return read_image_rgb(path)

def __parse_annotation(element):
    truncated = _findNode(element, 'truncated', parse=int)
    difficult = _findNode(element, 'difficult', parse=int)

    class_name = _findNode(element, 'name').text
    if class_name not in classes:
        raise ValueError('class name \'{}\' not found in classes: {}'.format(class_name, list(classes.keys())))

    box = np.zeros((1, 5))
    box[0, 4] = name_to_label(class_name)

    bndbox    = _findNode(element, 'bndbox')
    box[0, 0] = _findNode(bndbox, 'xmin', 'bndbox.xmin', parse=float) + 1
    box[0, 1] = _findNode(bndbox, 'ymin', 'bndbox.ymin', parse=float) + 1
    box[0, 2] = _findNode(bndbox, 'xmax', 'bndbox.xmax', parse=float) - 1
    box[0, 3] = _findNode(bndbox, 'ymax', 'bndbox.ymax', parse=float) - 1

    return truncated, difficult, box

def __parse_annotations(xml_root):
    size_node = _findNode(xml_root, 'size')
    width     = _findNode(size_node, 'width',  'size.width',  parse=float)
    height    = _findNode(size_node, 'height', 'size.height', parse=float)

    boxes = np.zeros((0, 5))
    for i, element in enumerate(xml_root.iter('object')):
        try:
            truncated, difficult, box = __parse_annotation(element)
        except ValueError as e:
            six.raise_from(ValueError('could not parse object #{}: {}'.format(i, e)), None)

        if truncated and skip_truncated:
            continue
        if difficult and skip_difficult:
            continue
        boxes = np.append(boxes, box, axis=0)

    return boxes, width, height

def load_annotations(image_index):
    filename = image_names[image_index] + '.xml'
    try:
        tree = ET.parse(os.path.join(data_dir, 'Annotations', filename))
        return __parse_annotations(tree.getroot())
    except ET.ParseError as e:
        six.raise_from(ValueError('invalid annotations file: {}: {}'.format(filename, e)), None)
    except ValueError as e:
        six.raise_from(ValueError('invalid annotations file: {}: {}'.format(filename, e)), None)

def save_image(image_index,img):
    try:
        path = os.path.join(dest_dir, 'JPEGImages', image_names[image_index] + image_extension)
        if not os.path.exists(path):
            image = Image.fromarray(img)
            image.save(path, 'jpeg')
        else:
            print("Exist:{}".format(path))
    except Exception as ex:
        logger.error('{}\n{}'.format(ex,path))

def save_annotations(image_index, size, annotations):
    dom = create_xml(image_index, size, annotations)
    write_xml(image_index, dom)

def create_xml(image_index, size, annotations):
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'JPEGImages'
    node_filename = SubElement(node_root, 'filename')
    filename = image_names[image_index] + ".jpg"
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

def write_xml(image_index, dom):
    filename = image_names[image_index] + '.xml'
    xml_path = os.path.join(dest_dir, 'Annotations', filename)
    with open(xml_path, 'w+') as f:
        dom.writexml(f, addindent='', newl='', encoding='utf-8')

def preprocess_image(image):
    return image

def random_transform(image, annotations):
    return image, annotations

def preprocess(image, annotations):
    # preprocess the image
    image = preprocess_image(image)

    # randomly transform image and annotations
    image, annotations = random_transform(image, annotations)

    # resize image
    image, image_scale = resize_image(image)

    # apply resizing to annotations too
    annotations[:, :4] *= image_scale

    return image, annotations

def process(image_index):

    # load data(image and annotations)
    img = load_image(image_index)
    annotations, width, height = load_annotations(image_index)

    # start preprocess
    image, annos = preprocess(img, annotations)

    # save data(image and annotations)
    save_image(image_index, image)
    save_annotations(image_index, (width, height), annos)

    logger.info("{} process successfully.".format(image_names[image_index]))

def multi_process():
    cpus = os.cpu_count()-2
    # cpus = 3
    p = multiprocessing.pool.Pool(cpus)
    p.map_async(process, range(size()))
    p.close()
    p.join()

def single_process():
    for idx in range(size()):
        process(idx)

if __name__ == '__main__':
    JPEGImages_path = os.path.join(args.destdir, 'JPEGImages')
    Annotations_path = os.path.join(args.destdir, 'Annotations')
    io_utils.mkdir(JPEGImages_path)
    io_utils.mkdir(Annotations_path)

    # single_process()
    multi_process()


"""
python /home/syh/RetinaNet/data_processing/preprocess_voc_data.py -d /home/syh/train_data/test -o /home/syh/train_data/test_resize
python /home/syh/RetinaNet/data_processing/preprocess_voc_data.py -d /home/syh/train_data/data/all_train_data -o /home/syh/train_data/data/all_train_data_resize


parser.add_argument('-d', '--datadir', default='/home/syh/train_data/test')
parser.add_argument('-o', '--destdir', default='/home/syh/train_data/test_resize')
"""