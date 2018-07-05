# -*- coding: utf-8 -*-
# @Time    : 4/26/2018 2:47 PM
# @Author  : sunyonghai
# @File    : ftp_upload.py
# @Software: ZJ_AI

import argparse
import ftp_utils
import sys

def run_upload(server_path, local_abs_path):
    ftp = ftp_utils.ftp_handler()
    result = ftp_utils.upload(
        ftp,
        server_path,
        local_abs_path
    )

    print("all completed" if result[0] == 1 else "some failed")
    print(result[1])
    # sys.exit()

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-spu', '--remote_path_u', help='path in server', default='/data/test_ftp')
parser.add_argument('-lpu', '--local_path_u', help='path in local', default='/home/syh/train_data/test.zip')
args = parser.parse_args()

def main():
    if args.remote_path_u and args.local_path_u:
        run_upload(args.remote_path_u, args.local_path_u)

if __name__  == '__main__':
    main()

"""
cd /home/syh/RetinaNet/data_processing
python ftp_upload.py -spu /home/ftpuser/ftp/predict_data/test_zip -lpu /home/syh/RetinaNet/data_52/test_zip/zip
python ftp_upload.py -spu /data/test_ftp/ -lpu /home/syh/train_data/test.zip
"""