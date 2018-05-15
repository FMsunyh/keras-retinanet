# -*- coding: utf-8 -*-
# @Time    : 4/26/2018 2:46 PM
# @Author  : sunyonghai
# @File    : ftp_download.py
# @Software: ZJ_AI

import argparse
import ftp_utils
import sys

def run_download(remote_path, local_path):
    ftp = ftp_utils.ftp_handler()
    result = ftp_utils.download(
        ftp=ftp,
        remote_path=remote_path,
        localAbsDir=local_path
    )

    print("all completed" if result[0] == 1 else "some failed")
    print(result[1])
    # sys.exit()

# parser = argparse.ArgumentParser(description='Get the data info')
# parser.add_argument('-sp', '--remote_path', help='path in server', default='')
# parser.add_argument('-lp', '--local_path', help='path in local', default='')
# args = parser.parse_args()
#
# def main():
#     if args.remote_path and args.local_path:
#         run_download(args.remote_path, args.local_path)
#
# if __name__  == '__main__':
#     main()

"""
cd /home/syh/RetinaNet/data_processing
python ftp_download.py -sp /home/ftpuser/ftp/train_data -lp /home/syh/ftp
/home/syh/RetinaNet/data_52_train
"""