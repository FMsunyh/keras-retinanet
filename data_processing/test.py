# -*- coding: utf-8 -*-
# @Time    : 5/31/2018 9:20 PM
# @Author  : sunyonghai
# @File    : test.py
# @Software: ZJ_AI

from multiprocessing import Pool, Lock, Value
import os

tests_count = 80

lock = Lock()

counter = Value('i', 0)  # int type，相当于java里面的原子变量


def run(fn):
    global tests_count, lock, counter
    with lock:
        counter.value += 1

    print( 'NO. (%d/%d) test start. PID: %d ' % (counter.value, tests_count, os.getpid()))
    # do something below ...


if __name__ == "__main__":
    pool = Pool(4)
    # 80个任务，会运行run()80次，每次传入xrange数组一个元素
    pool.map(run, range(80))
    pool.close()
    pool.join()