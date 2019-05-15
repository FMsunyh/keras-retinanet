import argparse
import cv2
import numpy as np
import os

def rotate(imgs_path):
    images = [os.path.join(imgs_path, s) for s in os.listdir(imgs_path)]
    count = 0
    for image_file in images:
        # image_file = os.path.join(imgs_path, os.path.join(imgs_path, 'train_data_2019-04-18_z10_10057.jpg'))
        try:
            img = cv2.imread(image_file)
            width = img.shape[1]
            height = img.shape[0]
            if width < height:
                image = np.array(np.rot90(img, 1))
                image = image.copy()
                cv2.imwrite(image_file, image)
                count = count + 1
                print(image_file)

        except Exception as e:
            print('Exception in pascal_voc_parser: {}'.format(e))
            continue

    print('total:', count)

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-p', '--parent_dir',help='the parent folder of image', default='/home/syh/train_data/C300_SUN/train_data_yj_300c_outdoor')
parser.add_argument('-j', '--JPEGImages',help='the folder of image', default='JPEGImages')
parser.add_argument('-a', '--Annotations',help='the folder of annotation', default='Annotations')
args = parser.parse_args()

if __name__ == '__main__':
    JPEGImages_dir = os.path.join(args.parent_dir, args.JPEGImages)
    rotate(JPEGImages_dir)