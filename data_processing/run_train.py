# -*- coding: utf-8 -*-
# @Time    : 4/28/2018 11:56 AM
# @Author  : sunyonghai
# @File    : run_train.py
# @Software: ZJ_AI
import argparse
import os

import archiving
import config
import create_Main
import create_all_Main
import create_all_data
import ftp_config
import ftp_download

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-p', '--phase', help='data folder', default='')
# parser.add_argument('-dt', '--data', help='data time', default='2018-04-28')
args = parser.parse_args()

class Train_config(object):
    def __init__(self):
        self.ftp_home = ftp_config.ftp_home
        self.ftp_train_data = 'train_data'
        self.remote_train_data = os.path.join(self.ftp_home, self.ftp_train_data)
        self.local_home = config.TRAIN_DATA
        self.zip_train_data = self.remote_train_data
        self.local_train_data = os.path.join(self.local_home, 'sub_train_data')
        self.local_all_train_data = os.path.join(self.local_home, 'all_train_data')

C = Train_config()

def _download():
    if C.remote_train_data and C.local_train_data:
        ftp_download.run_download(C.remote_train_data, C.local_train_data)
    else:
        print('download error')

def _archving():
    if C.zip_train_data and C.local_train_data:
        append_dirs = archiving.unzip_dir(C.zip_train_data, C.local_train_data)
    else:
        print('archiving error')

    return append_dirs
def _create_txt():
    # data_paths =  [os.path.join(C.local_train_data,dir) for dir in  os.listdir(C.local_train_data) if os.path.isdir(os.path.join(C.local_train_data,dir))]
    # create_Main.create_txts(data_paths)
    # create_all_Main.create_all_txts(data_paths, C.local_all_train_data)

    create_Main.create_txt(C.local_all_train_data)

def _copy_train():
    dirs = [os.path.join(args.phase,dir) for dir in  os.listdir(C.local_train_data) if os.path.isdir(os.path.join(C.local_train_data,dir))]

    create_all_data.copy_all(dirs, C.local_all_train_data)

def _append_train(dirs):
    create_all_data.append_all_data(dirs, C.local_all_train_data)

def _start_train():
    os.system('bash /home/syh/RetinaNet/keras_retinanet/bin/ens.sh')

"""
1. download the train data
2. archving
3. create train and valid dateset
4. start train
"""

if __name__ == '__main__':
    _download()
    # append_dirs = _archving()
    # _copy_train()

    append_dirs = ['train_data-2018-04-27']
    _append_train(append_dirs)
    _create_txt()

    # _start_train()