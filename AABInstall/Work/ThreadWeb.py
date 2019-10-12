#!use/bin/env python3
# -*- coding utf-8 -*-

import urllib3
from urllib import request
import json
import re
import _thread
import threading
import time
import mongodbTool
import copy
import random
import WebRequest
import ProxyMgr

mongo = mongodbTool.MyMongoDB()
finishMongo = mongodbTool.MyMongoDB()
finishMongo.SetDB(finishMongo.GetDBWithName("finishdb"))
finishMongo.SetCollection(finishMongo.GetCollectionWithName("finishcol"))
maxUserNumber = 100000000
# https://www.zhihu.com/people/haozhi/following
base = 'href="//www.zhihu.com/people/'

timeScale = 1
finishFindDic = {}
collectList = {}
insertList = []

waitFindList = []
tempWaitDic = {}

GetWaitLock = threading.Lock()
PushFinishLock = threading.Lock()


def ShowState():  # 打印
    print("changeUser")
    print("now collect " + str(len(collectList)))
    print("now finish " + str(len(finishFindDic)))
    print("wait " + str(len(waitFindList)))


def ShowThreadingInfo():  # 打印线程信息
    # 1 获取线程ID,NAME
    t = threading.currentThread()
    # 线程ID
    print('Thread id : %d' % t.ident)


def UpDateHost():  # 更新池
    ProxyMgr.UpDateHttpIP()


def GetFollowingUrl(targetName):
    return "https://www.zhihu.com/people/"+targetName+"/following"


def GetFollowersUrl(targetName):
    return "https://www.zhihu.com/people/"+targetName+"/followers"


def Request(targetUrl):  # 请求网络数据
    return WebRequest.open_url_random_host(targetUrl)


def TryInsertThread():  # 数据入库
    global insertList
    if len(insertList) > 100:
        mongo.InsertDicts(insertList)
        insertList = []


def InitDB():  # 初始化库
    if len(waitFindList) == 0:
        waitFindList.append("haozhi")
        tempWaitDic["haozhi"] = 0


def InitGetDbData():  # 还原库
    for x in finishMongo.FindTargetValue({"_id": 0}):
        target = x['tempToken']
        if target not in finishFindDic:
            finishFindDic[target] = True
    for x in mongo.FindTargetValue({"articlesCount": 0}):
        target = x['urlToken']
        if target not in collectList:
            collectList[target] = True
        if (target not in finishFindDic) and (target not in tempWaitDic):
            tempWaitDic[target] = x['followerCount']
            waitFindList.append(target)
    ShowState()
    print("请求完毕")


def BeginThread():  # 多线程 处理
    threads = []
    i = 0
    while i < 3:
        threads.append(threading.Thread(target=CheckWaitThread))
        i += 1
    for tempThread in threads:
        tempThread.start()


def GetWaitThread():
    tempToken = None
    tempMaxFlooerNum = -1
    GetWaitLock.acquire()
    if len(waitFindList) > 0:
        ShowState()
        tempMaxIndex = 0
        for i in range(len(waitFindList)):
            target = waitFindList[i]
            if not(target == None):
                if tempWaitDic[target] > tempMaxFlooerNum:
                    tempMaxFlooerNum = tempWaitDic[target]
                    tempMaxIndex = i

        tempToken = waitFindList[tempMaxIndex]
        waitFindList.pop(tempMaxIndex)
        tempWaitDic.pop(tempToken)
        if tempToken not in finishFindDic:
            finishFindDic[tempToken] = True
            dic = {}
            dic["tempToken"] = tempToken
            finishMongo.InsertDict(dic)

    GetWaitLock.release()
    return tempToken


def PushWaitThread(tempToken, userDataReBuild):
    PushFinishLock.acquire()
    if ((tempToken not in tempWaitDic) and (tempToken not in finishFindDic)):
        tempWaitDic[tempToken] = True
        waitFindList.append(tempToken)
        if tempToken not in collectList:
            collectList[tempToken] = userDataReBuild['followerCount']
            insertList.append(userDataReBuild)
            TryInsertThread()
    PushFinishLock.release()


def CheckWaitThread():
    while(len(waitFindList)):
        tempToken = GetWaitThread()
        try:
            if tempToken == None:
                time.sleep(1 * timeScale)
            else:
                followingNumber = 1
                followerNumber = 1
                errorNum = 0
                while(errorNum < 5):
                    if followingNumber == 1:
                        if GetUserTupleThread(GetFollowingUrl(tempToken)) == 0:
                            errorNum += 1
                        else:
                            errorNum = 0
                    else:
                        if GetUserTupleThread(GetFollowingUrl(tempToken)+'?page='+str(followingNumber)) == 0:
                            errorNum += 1
                        else:
                            errorNum = 0
                    followingNumber += 1
                errorNum = 0
                while(errorNum < 5):
                    if followerNumber == 1:
                        if GetUserTupleThread(GetFollowersUrl(tempToken)) == 0:
                            errorNum += 1
                        else:
                            errorNum = 0
                    else:
                        if GetUserTupleThread(GetFollowersUrl(tempToken)+'?page='+str(followerNumber)) == 0:
                            errorNum += 1
                        else:
                            errorNum = 0
                    followerNumber += 1
        except Exception as e:
            print(e)
    print("****** all finish ******")


def GetUserTupleThread(targetUrl):
    ShowThreadingInfo()
    html = Request(targetUrl)
    collectNum = 0
    if html != "":
        target = re.compile(r'{"id":.*?articlesCount":')
        tuple = re.findall(target, html)
        if tuple is not None:
            collectNum = len(tuple)
            for index in range(len(tuple)):
                data = tuple[index]
                if data != None:
                    jsonData = data + "0}"
                    try:
                        userDataReBuild = json.loads(jsonData)
                        tempToken = userDataReBuild['urlToken']
                        PushWaitThread(tempToken, userDataReBuild)
                    except Exception as e:
                        print(e)
    time.sleep(random.uniform(1 * timeScale, 3 * timeScale))
    return collectNum


def GetFollowingAndFollowerNumber(targetUrl):
    ShowThreadingInfo()
    followingNumber = 0
    followerNumber = 0

    html = Request(targetUrl)
    if html != "":
        try:
            target = re.compile(
                r'<strong title=".*?" class="NumberBoard-itemValue">.*?</strong>')
            tuple = re.findall(target, html)
            print(html)
            for index in range(len(tuple)):
                data = tuple[index]
                if data != None:
                    data = str(data).replace(
                        '<strong title="', '')
                    data = data[0:data.index('\"')]
                    print('----------'+data)
                if index == 0:
                    followingNumber = int(data)
                else:
                    followerNumber = int(data)
        except Exception as e:
            print(e)
            UpDateHost()
    time.sleep(random.uniform(1 * timeScale, 3 * timeScale))
    if followingNumber == 0 and followerNumber == 0:
        print(targetUrl)
    return followingNumber, followerNumber


def main():
    InitGetDbData()
    InitDB()
    BeginThread()


if __name__ == '__main__':
    main()
