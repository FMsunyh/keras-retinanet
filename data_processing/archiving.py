#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 4/16/2018 3:07 PM 
# @Author : sunyonghai 
# @File : archiving.py
# @Software: ZJ_AI
# =========================================================
import argparse
import glob
import os
import zip_utils

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-i', '--input',help='directory of zip or file of zip', default='')
parser.add_argument('-o', '--output',help='output diretory', default='')
args = parser.parse_args()

def unzip_dir(input, output):
    if output=='':
        output = input

    if input:
        file_paths = [os.path.join(input, s) for s in glob.glob(os.path.join(input,'*.zip'))]
        for file in file_paths:
            filename = os.path.basename(file)
            name = filename.split('.')[0]
            output_path = os.path.join(output,name)

            if not os.path.exists(output_path):
                zip_utils.un_zip_all(file, output)
            else:
                print('{} is existed'.format(output))

def unzip_file(input, output):

    if output=='':
        output = os.path.basename(input)

    if input:
        zip_utils.un_zip_all(input, output)

if __name__ == '__main__':

    if os.path.isdir(args.input):
        unzip_dir(args.input, args.output)
    else:
        unzip_file(args.input, args.output)



"""
cd /home/syh/RetinaNet/data_processing
python archiving.py -i /home/syh/RetinaNet/data_52/test -o /home/syh/RetinaNet/data_52/test
python archiving.py -i /home/syh/RetinaNet/data_52/test-0.zip -o /home/syh/RetinaNet/data_52/test-0

python archiving.py -i /data/train_data -o /home/syh/train_data/data/sub_train_data
python archiving.py -i /data/train_data2 -o /home/syh/train_data/data/sub_train_data2
python archiving.py -i /data/predict_data/ -o /home/syh/train_data/predict
"""