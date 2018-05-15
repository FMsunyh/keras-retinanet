# -*- coding: utf-8 -*-
# @Time    : 4/27/2018 3:33 PM
# @Author  : sunyonghai
# @File    : run_preprocessing.py
# @Software: ZJ_AI
import argparse

import io_utils
import send_email
import ftp_config

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-p', '--phase', help='data folder', default='data_63')
parser.add_argument('-dt', '--data', help='data time', default='2018-05-02')
args = parser.parse_args()

import os
import before_label
import compression
import config
import ftp_download
import archiving
import ftp_upload

class Pre_config(object):
    def __init__(self):
        self.ftp_home = ftp_config.ftp_home
        self.ftp_collect_data = 'collect_data'
        self.ftp_predict_data = 'predict_data'
        self.local_home = config.ROOT_HOME
        self.local_dir = os.path.join(self.local_home, args.phase)
        self.remote_zip_file = os.path.join(self.ftp_home, self.ftp_collect_data, args.data+'.zip')
        self.local_zip_file = os.path.join(self.local_dir, args.data+'.zip')
        self.upzip_dir = self.local_dir
        self.data_dir = os.path.join(self.upzip_dir, args.data)
        self.data_folder = args.data
        self.str_date = args.data.strip('-')
        self.zip_dir = os.path.join(self.data_dir, 'zip')
        self.upload_dir = os.path.join(self.ftp_home, self.ftp_predict_data, args.data)

# parser = argparse.ArgumentParser(description='Get the data info')
# parser.add_argument('-sp', '--remote_path', help='path in server', default='/home/ftpuser/ftp/collect_data/2018-04-26.zip')
# parser.add_argument('-lp', '--local_path', help='path in local', default='/home/syh/RetinaNet/data_63')
#
# parser.add_argument('-i', '--input',help='directory of zip or file of zip', default='/home/syh/RetinaNet/data_63/2018-04-26.zip')
# parser.add_argument('-o', '--output',help='output diretory', default='/home/syh/RetinaNet/data_63')
#
# parser.add_argument('-p', '--parent_dir',help='the parent folder of image', default='/home/syh/RetinaNet/data_63/2018-04-26')
# parser.add_argument('-d', '--folder_name',help='the folder of image', default='2018-04-26')
# parser.add_argument('-s', '--str_date',help='year month day', default='')
#
# parser.add_argument('-ic', '--dir',help='directory to zip', default='/home/syh/RetinaNet/data_63/2018-04-26')
# parser.add_argument('-oc', '--output_zip',help='output diretory', default='/home/syh/RetinaNet/data_63/2018-04-26')
#
# parser.add_argument('-spu', '--remote_path_u', help='path in server', default='/home/ftpuser/ftp/predict_data/2018-04-26')
# parser.add_argument('-lpu', '--local_path_u', help='path in local', default='/home/syh/RetinaNet/data_63/2018-04-26/zip')

# args = parser.parse_args()

"""
1. download(ftp)
2. archiving
3. preprocess
4. compression
5. upload(ftp)
"""

C = Pre_config()

# 1. download(ftp)
def _download():
    if C.remote_zip_file and C.local_dir:
        ftp_download.run_download(C.remote_zip_file, C.local_dir)
    else:
        print('download error')

def _copy_download():
    if C.remote_zip_file and C.local_dir:
        io_utils.copy(C.remote_zip_file, C.local_dir)
    else:
        print('copy error')
# 2. archiving
def _archiving():
    # if os.path.isdir(C.local_zip_file):
    #     archiving.unzip_dir(args.input, args.output)
    # else:
    if C.local_zip_file and C.data_dir:
        archiving.unzip_file(C.local_zip_file, C.data_dir)
    else:
        print('archiving error')

# 3. preprocess
def _preprocess():
#  python before_label.py -p /home/syh/RetinaNet/data_63/2018-04-26/ -s 20180426 -d 2018-04-26
    if C.data_dir and C.data_folder and C.str_date:
        before_label.before_label_process(C.data_dir, C.data_folder, C.str_date)
    else:
        print('preprocess error')

# 4. compression
# python compression.py -ic /home/syh/RetinaNet/data_63/2018-04-26 -oc /home/syh/RetinaNet/data_63/2018-04-26
def _compression():
    if C.data_dir:
        compression.zip_batch(C.data_dir, C.data_dir)
    else:
        print('compression error')

# 5. upload(ftp)
# python ftp_upload.py -sp /home/ftpuser/ftp/predict_data/2018-04-26 -lp /home/syh/RetinaNet/data_63/2018-04-26/zip
def  _upload():
    if C.upload_dir and C.zip_dir:
        ftp_upload.run_upload(C.upload_dir, C.zip_dir)
    else:
        print('upload error')

def  _copy_upload():
    if C.upload_dir and C.zip_dir:
        # ftp_upload.run_upload(C.upload_dir, C.zip_dir)
        io_utils.copy_dir(C.zip_dir, C.upload_dir)
    else:
        print('upload error')

def _email():
    context = "Dear All,\ndata: '{}' has uploaded to 196-FTP server. \n\n\nNote:this email send by ai-server,don't reply.".format(args.data)
    send_email.notify(context)

if __name__ == '__main__':
    _copy_download()
    _archiving()
    _preprocess()
    _compression()
    _copy_upload()
    _email()
    print('finished!')


"""
run 
python run_preprocessing.py -p data_63 -d 2018-05-03

"""