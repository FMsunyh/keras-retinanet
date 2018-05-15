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
import zipfile

import zip_utils
from io_utils import mkdir, remove_all
import time
#
# def un_zip(file_name, output):
#     """unzip zip file"""
#     zip_file = zipfile.ZipFile(file_name)
#     if os.path.isdir(output):
#         pass
#     else:
#         mkdir(output)
#     for names in zip_file.namelist():
#         zip_file.extract(names, output)
#     zip_file.close()
#
# def un_zip_all(file_name, output):
#     """unzip zip file"""
#     # if not mkdir(output):
#     #     remove_all(output)
#
#     try:
#         zip_file = zipfile.ZipFile(file_name)
#         zip_file.extractall(output)
#         zip_file.close()
#         print('extract data to {} directory.'.format(output))
#     except Exception as ex:
#         print(ex)
#
# def zip_list(file_list=[], save_path='', note=''):
#     if len(file_list)<=0 or save_path=='':
#         return
#
#     zfile = zipfile.ZipFile(save_path, 'w+')
#     for tar in file_list:
#         zfile.write(tar,os.path.basename(tar))# tar -->file
#         zfile.close()
#     print('save zip file to', save_path)
#
# def createZip(filePath, savePath, note = ''):
#     '''''
#     zip folder。
#     :param filePath:  to zip folder
#     :param savePath: save path
#     :param note: note
#     :return:
#     '''
#     today = time.strftime('%Y%m%d')
#     # now = time.strftime('%H%M%S')
#     fileList=[]
#     if not os.path.exists(today):
#         os.mkdir(today)
#         print('mkdir successful')
#     if len(note) == 0:
#         target = savePath + os.sep + today + '.zip'
#     else:
#         target = savePath + os.sep + today + '_' + note + '.zip'
#     newZip = zipfile.ZipFile(target,'w')
#     for dirpath,dirnames,filenames in os.walk(filePath):
#         for filename in filenames:
#             fileList.append(os.path.join(dirpath,filename))
#     for tar in fileList:
#         newZip.write(tar,tar[len(filePath):])# tar -->file，tar[len(filePath)] --> file name
#     newZip.close()
#     print('save zip file to', target)

# parser = argparse.ArgumentParser(description='Get the data info')
# parser.add_argument('-i', '--input',help='directory of zip or file of zip', default='')
# parser.add_argument('-o', '--output',help='output diretory', default='')
# args = parser.parse_args()

def unzip_dir(input, output):
    if output=='':
        output = input

    if input:
        # file_paths = [os.path.join(input, s) for s in os.listdir(input)]
        file_paths = [os.path.join(input, s) for s in glob.glob(os.path.join(input,'*.zip'))]
        # file = '/home/syh/ftp/train_data-2018-04-23.zip'
        append_dirs=[]
        for file in file_paths:
            filename = os.path.basename(file)
            name = filename.split('.')[0]
            output_path = os.path.join(output,name)

            if not os.path.exists(output_path):
                zip_utils.un_zip_all(file, output_path)
                append_dirs.append(name)
            else:
                print('{} is existed'.format(output_path))

    return append_dirs
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
"""