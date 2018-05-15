#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 4/13/2018 10:07 AM 
# @Author : sunyonghai 
# @File : csv_utils.py 
# @Software: ZJ_AI
# =========================================================
import csv

splitsymbol = ','

# 功能：将一个二重列表写入到csv文件中
# 输入：文件名称，数据列表
def createListCSV(fileName="", dataList=[]):
    with open(fileName, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)
        for data in dataList:
            csvWriter.writerow(data)
        csvFile.close

    print("save data to '%s'" % fileName)

def createListCSV2(fileName="", dataList=[]):
    with open(fileName, "w+") as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerows(dataList)
        csvFile.close
    print("save data to '%s'" % fileName)

# 功能：从文本文件中读取返回为列表的形式
# 输入：文件名称，分隔符（默认,）
def readListCSV(fileName="", splitsymbol=","):
    dataList = []
    with open(fileName, "r") as csvFile:
        dataLine = csvFile.readline().strip("\n")
        while dataLine != "":
            tmpList = dataLine.split(splitsymbol)
            dataList.append(tmpList)
            dataLine = csvFile.readline().strip("\n")
        csvFile.close()

    print("read data from '%s'" % fileName)
    return dataList


# 功能：将一字典写入到csv文件中
# 输入：文件名称，数据字典
def createDictCSV(fileName="", dataDict={}):
    with open(fileName, "w+") as csvFile:
        csvWriter = csv.writer(csvFile)
        for k,v in dataDict.items():
            csvWriter.writerow([k,v])
        csvFile.close()

    print("save data to '%s'" % fileName)


# 功能：从csv文件中读取一个字典
# 输入：文件名称，keyIndex,valueIndex
def readDictCSV(fileName="", keyIndex=0, valueIndex=1):
    dataDict = {}
    with open(fileName, "r") as csvFile:
        dataLine = csvFile.readline().strip("\n")
        while dataLine != "":
            tmpList = dataLine.split(splitsymbol)
            dataDict[tmpList[keyIndex]] = tmpList[valueIndex]
            dataLine = csvFile.readline().strip("\n")
        csvFile.close()

    print("read data from '%s'" % fileName)
    return dataDict


# 功能：从csv文件中读取一个计数字典
# 输入：文件名称，keyIndex
def readDictCSV(fileName="", keyIndex=0):
    dataDict = {}
    with open(fileName, "r") as csvFile:
        dataLine = csvFile.readline().strip("\n")
        while dataLine != "":
            tmpList = dataLine.split(splitsymbol)
            if dataDict.get(tmpList[keyIndex]) == None:
                dataDict[tmpList[keyIndex]] = 0
            dataDict[tmpList[keyIndex]] = dataDict.get(tmpList[keyIndex]) + 1
            dataLine = csvFile.readline().strip("\n")
        csvFile.close()

    print("read data from '%s'" % fileName)
    return dataDict