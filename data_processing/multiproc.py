# -*- coding: utf-8 -*-
# @Time    : 5/15/2018 11:45 AM
# @Author  : sunyonghai
# @File    : multiproc.py
# @Software: ZJ_AI
from multiprocessing import Process, Pool, cpu_count
import multiprocessing

# write process:
def write(q,data):
    # while True:
    #     pass
    q.put(data)


# read process:
def read(q):
    while True:
        value = q.get(True)
        if value !=None:
            print(value)
        else:
            break

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    q = manager.Queue()
    pr = Process(target=read, args=(q,))
    pr.start()

    p = Pool()
    for i in range(4):
        p.apply_async(write, args=(q, i))

    p.close()
    p.join()
    q.put(None)
    pr.join()

    print("end")