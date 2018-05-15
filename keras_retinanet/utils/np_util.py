#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/26/2018 2:02 PM 
# @Author : sunyonghai 
# @File : np_util.py 
# @Software: ZJ_AI
# =========================================================

import numpy as np
import time

# arr = np.random.randint(1,100,(1280,))
# print(arr.shape)
#
# start = time.time()
# arr_list = arr.tolist()
# arr_str = ','.join(str(i) for i in arr_list)
# print(arr_str)
#
# print("# for-processing time:",  str(1000 * (time.time()-start)) + 'ms')
#
#
# start = time.time()
# arr_list = arr.tolist()
# arr_str = ','.join(map(str, arr_list))
# print(arr_str)
#
# print("# map-processing time:",  str(1000 * (time.time()-start)) + 'ms')


arr = np.random.randint(1,10,(2,2,3))
print(arr)
new_arr = arr[:,:,::-1].copy()
print(new_arr)