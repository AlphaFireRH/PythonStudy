#!use/bin/env python3
# -*- coding utf-8 -*-

import re
import _thread
import threading
import time
import mongodbTool
import copy
import random
import WebRequest

mongo = mongodbTool.MyMongoDB()
base = 'href="//www.zhihu.com/people/'

timeScale = 1


def Request(targetUrl):  # 请求网络数据
    return WebRequest.GetWebInfo(targetUrl, False)


def GetFollowingUrl(targetName):
    return "https://www.zhihu.com/people/"+targetName+"/following"


def GetOneKey():  # 获取key
    dbData = mongo.FindData({"simpleInfo": None})
    return dbData


def BeginThread():  # 多线程 处理
    CheckWaitThread()
    # threads = []
    # i = 0
    # while i < 3:
    #     threads.append(threading.Thread(target=CheckWaitThread))
    #     i += 1
    # for tempThread in threads:
    #     tempThread.start()


def UpdateDic(dbData, newDic):
    mongo.Update(dbData, newDic)


def CheckWaitThread():
    while True:
        dbData = GetOneKey()
        if dbData:
            url = GetFollowingUrl(dbData['urlToken'])
            requestData = Request(url)
            dic = AnalysisData(requestData, dbData)
            if dic['simpleInfo'] != None and len(dic['simpleInfo']) > 0:
                print(dic['simpleInfo'])
                UpdateDic(dbData, dic)
        else:
            break
        time.sleep(random.uniform(1 * timeScale, 3 * timeScale))


def AnalysisData(html, dbData):
    dic = copy.deepcopy(dbData)
    if html != "":
        try:
            simpleInfo = str(GetTargetInfo(
                r'property="og:description" content=".*?"/>', html))
            dic['simpleInfo'] = simpleInfo
            dic['answers'] = GetNumberString(GetTargetInfo(
                r'回答<span class="Tabs-meta">.*?</span>', html))
            dic['asks'] = GetNumberString(GetTargetInfo(
                r'提问<span class="Tabs-meta">.*?</span>', html))
            dic['posts'] = GetNumberString(GetTargetInfo(
                r'文章<span class="Tabs-meta">.*?</span>', html))
            dic['columns'] = GetNumberString(GetTargetInfo(
                r'专栏<span class="Tabs-meta">.*?</span>', html))
            dic['pins'] = GetNumberString(GetTargetInfo(
                r'想法<span class="Tabs-meta">.*?</span>', html))
        except Exception as e:
            print(str(e))
    return dic


def GetTargetInfo(info, html):  # 正则提取
    returnValue = ""
    target = re.compile(info)
    tuple = re.findall(target, html)
    try:
        if tuple is not None:
            if len(tuple) > 0:
                returnValue = tuple[0]
    except Exception as e:
        print(e)
    return returnValue


def GetNumberString(target):
    cop = re.compile("[^.^0-9]")
    return cop.sub("", target)


def main():
    BeginThread()


if __name__ == '__main__':
    main()
