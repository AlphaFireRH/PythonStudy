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
finishMongo = mongodbTool.MyMongoDB()
finishMongo.SetDB(finishMongo.GetDBWithName("finishdetaildb"))
finishMongo.SetCollection(finishMongo.GetCollectionWithName("finishdetailcol"))
base = 'href="//www.zhihu.com/people/'

requestMaxValue = 4000
timeScale = 1
finishDic = {}
waitList = []

GetWaitLock = threading.Lock()


def ShowState():  # 打印
    print("changeUser")
    print("now finish " + str(len(finishDic)))
    print("wait " + str(len(waitList)))


def Request(targetUrl):  # 请求网络数据
    return WebRequest.open_url_random_host(targetUrl)


def GetFollowingUrl(targetName):  # 拼接连接地址
    return "https://www.zhihu.com/people/"+targetName+"/following"


def GetOneKey():  # 获取key
    global waitList
    GetWaitLock.acquire()
    if len(waitList) > 0:
        target = waitList[0]
        waitList.remove(target)
        dbData = mongo.FindDataOne({"urlToken": target})
        GetWaitLock.release()
        return dbData
    else:
        GetWaitLock.release()
        return None


def TrySleep():  # 延时等待
    time.sleep(random.uniform(1 * timeScale, 3 * timeScale))


def BeginThread():  # 多线程 处理
    threads = []
    i = 0
    while i < 3:
        threads.append(threading.Thread(target=CheckWaitThread))
        i += 1
    for tempThread in threads:
        tempThread.start()


def UpdateDic(dbData, newDic, setStatusOnly):  # 更新数据库数据
    global finishDic
    mongo.Update(dbData, newDic)
    tempToken = newDic["urlToken"]
    if not setStatusOnly:
        finishDic[tempToken] = True
        dic = {}
        dic["tempToken"] = tempToken
        finishMongo.InsertDict(dic)


def SetStatusOnly(dbData):  # 查询不到 仅改变状态 以后再查
    dic = copy.deepcopy(dbData)
    dic['setStatusOnly'] = True
    UpdateDic(dbData, dic, True)


def InitData():  # 初始化数据
    InitFinishData()
    InitWaitData()


def InitFinishData():
    global finishDic
    finishDic = {}
    for x in finishMongo.FindTargetValue({"_id": 0}):
        target = x['tempToken']
        if target not in finishDic:
            finishDic[target] = True


def InitWaitData():
    global waitList
    global finishDic
    dbData = mongo.FindDataLimit(
        {"simpleInfo": None, "setStatusOnly": None}, requestMaxValue)
    num = 0
    for x in dbData:
        target = x['urlToken']
        if target not in waitList:
            if target not in finishDic:
                waitList.append(target)
            else:
                tempData = mongo.FindDataOne({"urlToken": target})
                if tempData:
                    SetStatusOnly(tempData)
                num += 1
    print(num)
    print(len(finishDic))
    print(len(waitList))


def CheckWaitThread():  # 更新数据
    while True:
        dbData = GetOneKey()
        try:
            if dbData != None:
                url = GetFollowingUrl(dbData['urlToken'])
                finishStatus = False
                for i in range(20):
                    TrySleep()
                    requestData = Request(url)
                    dic = AnalysisData(requestData, dbData)
                    if dic['simpleInfo'] != None and len(dic['simpleInfo']) > 0:
                        dic['setStatusOnly'] = False
                        UpdateDic(dbData, dic, False)
                        finishStatus = True
                        break
                if not finishStatus:
                    SetStatusOnly(dbData)
            else:
                InitWaitData()
            ShowState()
        except Exception as e:
            print(e)


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
    InitData()
    BeginThread()


if __name__ == '__main__':
    main()
