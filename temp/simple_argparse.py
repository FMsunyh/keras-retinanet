#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/28/2018 2:27 PM 
# @Author : sunyonghai 
# @File : simple_argparse.py.py 
# @Software: ZJ_AI
# =========================================================

import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True, help="name of the user")


args = vars(ap.parse_args())
# display a friendly message to the user
print("Hi there {}, it's nice to meet you!".format(args["name"]))