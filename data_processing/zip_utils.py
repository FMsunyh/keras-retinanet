# -*- coding: utf-8 -*-
# @Time    : 4/26/2018 11:00 AM
# @Author  : sunyonghai
# @File    : zip_utils.py
# @Software: ZJ_AI

import argparse
import os
import zipfile
from io_utils import mkdir, remove_all
import time

def un_zip(file_name, output):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(output):
        pass
    else:
        mkdir(output)
    for names in zip_file.namelist():
        zip_file.extract(names, output)
    zip_file.close()

def un_zip_dir(dir, output):
    file_paths = [os.path.join(dir, s) for s in os.listdir(dir)]
    # file = '/home/syh/ftp/train_data-2018-04-23.zip'
    for file in file_paths:
        un_zip_all(file, output)

def un_zip_all(file_name, output):
    """unzip zip file"""
    # if not mkdir(output):
    #     remove_all(output)

    try:
        zip_file = zipfile.ZipFile(file_name)
        zip_file.extractall(output)
        zip_file.close()
        print('extract data to {} directory.'.format(output))
    except Exception as ex:
        print(ex)

def zip_list(file_list=[], save_path='', mode='w', note=''):
    if len(file_list)<=0 or save_path=='':
        return

    zfile = zipfile.ZipFile(save_path, mode)
    for tar in file_list:
        tars = tar.split(os.sep)
        arcname = os.path.join(tars[-2], tars[-1])
        zfile.write(tar,arcname)# tar -->file， arcname->file name in zip

    zfile.close()
    print('save zip file to', save_path)

def createZip(filePath, savePath, note = ''):
    '''''
    zip folder。
    :param filePath:  to zip folder
    :param savePath: save path
    :param note: note
    :return:
    '''
    today = time.strftime('%Y%m%d')
    # now = time.strftime('%H%M%S')
    fileList=[]
    if not os.path.exists(today):
        os.mkdir(today)
        print('mkdir successful')
    if len(note) == 0:
        target = savePath + os.sep + today + '.zip'
    else:
        target = savePath + os.sep + today + '_' + note + '.zip'
    newZip = zipfile.ZipFile(target,'w')
    for dirpath,dirnames,filenames in os.walk(filePath):
        for filename in filenames:
            fileList.append(os.path.join(dirpath,filename))
    for tar in fileList:
        name = tar[len(filePath):]
        newZip.write(tar,name)# tar -->file，tar[len(filePath)] --> file name
    newZip.close()
    print('save zip file to', target)