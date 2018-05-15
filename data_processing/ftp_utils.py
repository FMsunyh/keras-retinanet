#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 4/16/2018 3:31 PM 
# @Author : sunyonghai 
# @File : ftp_utils.py 
# @Software: ZJ_AI
# =========================================================
# !/usr/bin/python3
# coding: utf-8
import argparse
from  data_processing  import ftp_config
import ftplib
import os

# Get connection
def get_connect(host, port, username, password):
    """
    :param host: FTP ip
    :param port: FTP port
    :param username: FTP userName
    :param password: FTP password
    :return: ftp
    """
    print("FTP connection...")
    result = [1, ""]

    try:
        ftp = ftplib.FTP()
        ftp.set_debuglevel(2)
        ftp.connect(host, port)
        ftp.login(username, password)

        result = [1, "connection success", ftp]

    except Exception as e:
        result = [-1, "connection fail, reason:{0}".format(e)]

    return result

# download
def download(ftp, remote_path, localAbsDir):
    """
    :param ftp:
    :param remote_path: server path (relative path or absolute path)
    :param localAbsDir: client path, such as: E:/FTP/downDir/
    :return:
    """
    result = [1, ""]

    try:
        remote_path = format_path(remote_path)
        localAbsDir = format_path(localAbsDir)

        remoteRel = ""
        if remote_path == "":
            remote_path = ftp_config.ftp_home
        else:
            if remote_path.startswith(ftp_config.ftp_home):
                remoteRel = remote_path.replace(ftp_config.ftp_home, "/")
                remoteRel = format_path(remoteRel)
            else:
                remoteRel = remote_path

        if localAbsDir == "":
            localAbsDir = ftp_config.localDir
            localAbsDir = format_path(localAbsDir)

        remoteAbs = format_path(ftp_config.ftp_home, remoteRel)

        if os.path.isdir(remoteAbs):
            rs = download_dir(ftp, remoteRel, localAbsDir)
        else:
            rs = download_file(ftp, remoteRel, localAbsDir,overwrite=True)

        if rs[0] == -1:
            result[0] = -1
        result[1] = result[1] + "\n" + rs[1]
    except Exception as e:
        result = [-1, "download fail, reason:{0}".format(e)]

    return result


# download all files in directory
def download_dir(ftp, server_dir, localAbsDir):
    """
    :param ftp:
    :param server_dir:
    :param localAbsDir:
    :return:
    """
    print("start download dir by use FTP...")
    result = [1, ""]

    try:
        server_dir = format_path(server_dir)
        localAbsDir = format_path(localAbsDir)

        files = []  # files
        dirs = []  # folders
        remote_paths = ftp.nlst(server_dir)
        if len(remote_paths) > 0:
            for remote_path in remote_paths:
                remote_path = format_path(remote_path)

                if isDir(ftp, remote_path):
                    dirs.append(remote_path)
                else:
                    files.append(remote_path)

        ftp.cwd("")  #  cd ftp_home
        if len(files) > 0:
            for rrp in files:  # rrp is relPath
                rs = download_file(ftp, rrp, localAbsDir)
                if rs[0] == -1:
                    result[0] = -1
                result[1] = result[1] + "\n" + rs[1]

        if len(dirs) > 0:
            for rrd in dirs:  # rrd is relDir
                dirName = lastDir(rrd)
                localAbsDir = format_path(localAbsDir, dirName)
                rs = download_dir(ftp, rrd, localAbsDir)
                if rs[0] == -1:
                    result[0] = -1
                result[1] = result[1] + "\n" + rs[1]

    except Exception as e:
        result = [-1, "download fail, reason:{0}".format(e)]

    return result


# download the file
def download_file(ftp, remoteRelPath, localAbsDir, overwrite=False):
    """
    :param ftp:
    :param remoteRelPath:
    :param localAbsDir:
    :return:
    """
    print("start download file by use FTP...")
    result = [1, ""]

    try:
        fileName = os.path.basename(remoteRelPath)  # file name

        localAbsPath = format_path(localAbsDir, fileName)
        splitPaths = os.path.split(localAbsPath)

        lad = splitPaths[0]
        lad = format_path(lad)
        if not os.path.exists(lad):
            os.makedirs(lad)

        # if exists, not download(default)
        if not os.path.exists(localAbsPath) or overwrite == True:
            handle = open(localAbsPath, "wb")
            ftp.retrbinary("RETR %s" % remoteRelPath, handle.write, 1024)
            handle.close()
            ret_msg = "download " + splitPaths[1] + " success"
        else:
            ret_msg = '{} is existed! Skip'.format(localAbsPath)

        result = [1, ret_msg]

    except Exception as e:
        result = [-1, "download fail, reason:{0}".format(e)]

    return result


# upload
def upload(ftp, server_dir, local_path):
    """
    :param ftp:
    :param server_dir:
    :param local_path:
    :return:
    """
    result = [1, ""]

    try:
        server_dir = format_path(server_dir)
        local_path = format_path(local_path)

        localRelDir = ""
        if local_path == "":
            local_path = ftp_config.localDir
            local_path = format_path(local_path)
        else:
            if local_path.startswith(ftp_config.localDir):  #  absolute path
                localRelDir = local_path.replace(ftp_config.localDir, "/")
                localRelDir = format_path(localRelDir)
            else:  #
                local_path = format_path(ftp_config.localDir, local_path)

        if server_dir == "":
            server_dir = format_path("/uploadFiles/", localRelDir)
        else:
            if server_dir.startswith(ftp_config.ftp_home):
                server_dir = server_dir.replace(ftp_config.ftp_home, "/")
                server_dir = format_path(server_dir)

        if os.path.isdir(local_path):  # isDir
            rs = upload_dir(ftp, server_dir, local_path)
        else:  # isFile
            rs = upload_file(ftp, server_dir, local_path)

        if rs[0] == -1:
            result[0] = -1
        result[1] = result[1] + "\n" + rs[1]

    except Exception as e:
        result = [-1, "upload fail, reason:{0}".format(e)]

    return result


# upload folder
def upload_dir(ftp, server_dir, localAbsDir):
    """
    :param ftp:
    :param server_dir:
    :param localAbsDir:
    :return:
    """
    print("start upload dir by use FTP...")
    result = [1, ""]

    try:
        for root, dirs, files in os.walk(localAbsDir):
            if len(files) > 0:
                for fileName in files:
                    localAbsPath = localAbsDir + fileName
                    rs = upload_file(ftp, server_dir, localAbsPath)
                    if rs[0] == -1:
                        result[0] = -1
                    result[1] = result[1] + "\n" + rs[1]

            if len(dirs) > 0:
                for dirName in dirs:
                    rrd = format_path(server_dir, dirName)
                    lad = format_path(localAbsDir, dirName)
                    rs = upload_dir(ftp, rrd, lad)
                    if rs[0] == -1:
                        result[0] = -1
                    result[1] = result[1] + "\n" + rs[1]

            break
    except Exception as e:
        result = [-1, "upload fail, reason:{0}".format(e)]

    return result


#
def upload_file(ftp, server_dir, localAbsPath):
    """
    :param ftp:
    :param server_dir:
    :param localAbsPath:
    :return:
    """
    print("start upload file by use FTP...")
    result = [1, ""]

    try:
        try:
            ftp.cwd(server_dir)
        except ftplib.error_perm:
            try:
                ftp.mkd(server_dir)
            except ftplib.error_perm:
                print("U have no authority to make dir")

        fileName = os.path.basename(localAbsPath)
        remoteRelPath = format_path(server_dir, fileName)

        handle = open(localAbsPath, "rb")
        ftp.storbinary("STOR %s" % remoteRelPath, handle, 1024)
        handle.close()

        result = [1, "upload " + fileName + " success"]
    except Exception as e:
        result = [-1, "upload fail, reason:{0}".format(e)]

    return result


# remote path isDir or isFile
def isDir(ftp, path):
    try:
        ftp.cwd(path)
        ftp.cwd("..")
        return True
    except:
        return False


# return last dir'name in the path, like os.path.basename
def lastDir(path):
    path = format_path(path)
    paths = path.split("/")
    if len(paths) >= 2:
        return paths[-2]
    else:
        return ""


#
def format_path(path, *paths):
    """
    :param path: path 1
    :param paths: path 2-n
    :return:
    """
    if path is None or path == "." or path == "/" or path == "//":
        path = ""

    if len(paths) > 0:
        for pi in paths:
            if pi == "" or pi == ".":
                continue
            path = path + "/" + pi

    if path == "":
        return path

    while path.find("\\") >= 0:
        path = path.replace("\\", "/")
    while path.find("//") >= 0:
        path = path.replace("//", "/")

    if path.find(":/") > 0:  #  NOT EQ ZERO, OS.PATH.ISABS NOT WORK
        if path.startswith("/"):
            path = path[1:]
    else:
        if not path.startswith("/"):
            path = "/" + path

    if os.path.isdir(path):  # remote path is not work
        if not path.endswith("/"):
            path = path + "/"
    elif os.path.isfile(path):  # remote path is not work
        if path.endswith("/"):
            path = path[:-1]
    elif path.find(".") < 0:  # maybe it is a dir
        if not path.endswith("/"):
            path = path + "/"
    else:  # maybe it is a file
        if path.endswith("/"):
            path = path[:-1]

    # print("new path is " + path)
    return path

import sys

def ftp_handler():
    result = get_connect(
        host=ftp_config.host,
        port=ftp_config.port,
        username=ftp_config.username,
        password=ftp_config.password
    )

    if result[0] != 1:
        print(result[1])
        sys.exit()
    else:
        print("connection success")

    ftp = result[2]

    return ftp

def runFTP(remote_path, local_path):

    ftp = ftp_handler()
    result = download(
        ftp=ftp,
        remote_path=remote_path,
        localAbsDir=local_path
    )

    # result = ftp_client.upload(
    #     ftp=ftp,
    #     server_dir=remote_path,
    #     local_path=local_path
    # )

    # ftp.quit()

    print("all completed" if result[0] == 1 else "some failed")
    print(result[1])
    sys.exit()

# parser = argparse.ArgumentParser(description='Get the data info')
# parser.add_argument('-sp', '--remote_path',help='path in server', default='')
# parser.add_argument('-lp', '--local_path',help='path in local', default='')
# args = parser.parse_args()
#
# def main():
#     if args.remote_path and args.local_path:
#         runFTP(args.remote_path, args.local_path)
#
#
# if __name__  == '__main__':
#     main()

"""
cd /home/syh/RetinaNet/data_processing
python ftp_utils.py -sp /home/ftpuser/ftp/train_data -lp /home/syh/ftp
"""

