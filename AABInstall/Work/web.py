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


class UserData(object):
    def __init__(self):
        try:
            self.id = 0
        except Exception as e:
            print(e)
    id = 0
    urlToken = ""
    name = ""
    useDefaultAvatar = False
    avatarUrl = ""
    avatarUrlTemplate = ""
    isOrg = False
    type = ""
    url = ""
    userType = ""
    headline = ""
    gender = -1
    isAdvertiser = False
    vipInfo = {}
    badge = []
    isFollowing = False
    isFollowed = False
    followerCount = 0
    answerCount = 0
    articlesCount = 0


mongo = mongodbTool.MyMongoDB()
finishMongo = mongodbTool.MyMongoDB()
finishMongo.SetDB(finishMongo.GetDBWithName("finishdb"))
finishMongo.SetCollection(finishMongo.GetCollectionWithName("finishcol"))

#  https://www.zhihu.com/people/haozhi/following
# allUser={}
finishFindList = {}
waitFindList = []
maxUserNumber = 100000000
base = 'href="//www.zhihu.com/people/'
insertList = []
collectList = {}
tempWait = {}


def InitGetDbData():
    for x in mongo.FindTargetValue({"articlesCount": 0}):
        target = x['urlToken']
        if target not in collectList:
            collectList[target] = True
    for x in finishMongo.FindTargetValue({"_id": 0}):
        target = x['tempToken']
        if target not in finishFindList:
            finishFindList[target] = True
    print("请求完毕")
    for x in collectList:
        if (x not in finishFindList) and (x not in tempWait):
            tempWait[x] = True
            waitFindList.append(x)


def ShowState():
    print("changeUser")
    print("now collect " + str(len(collectList)))
    print("now finish " + str(len(finishFindList)))
    print("wait " + str(len(waitFindList)))


def NeedBreak():
    state = False
    if len(finishFindList) >= maxUserNumber:
        state = True
    return state


proxieRequest = 'http://dev.energy67.top/api/?apikey=fba0068b9fe964c50414feef499fc05419c12fb1&num=3&type=json&line=win&proxy_type=putong&sort=rand&model=all&protocol=http&address=&kill_address=&port=&kill_port=&today=false&abroad=1&isp=&anonymity='

proxie = {'http': 'http://58.253.153.247:9999',
          'https': 'https://58.253.153.1:9999'}
header = {'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) 'r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
          'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label', 'Connection': 'keep-alive'}


def GetBaiduInfo():
    http = urllib3.PoolManager(timeout=30)
    r = http.request(
        'GET', 'http://' + 'www.baidu.com'
        # +GetInputData()
    )
    print(r.status)
    print(r.data.decode())


def GetWebInfo(targetUrl):
    global proxie
    global header
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager(timeout=30)
    r = http.request(
        'GET', targetUrl
    )

    #proxy = urllib3.ProxyManager(targetUrl, headers=header)
    #r = proxy.request('GET', targetUrl)

    # print(r.status)
    # print(r.data.decode())

    return (r.data.decode())


def GetFollowingUrl(targetName):
    return "https://www.zhihu.com/people/"+targetName+"/following"


def GetFollowersUrl(targetName):
    return "https://www.zhihu.com/people/"+targetName+"/followers"


def GetUserTuple(targetUrl):
    info = GetWebInfo(targetUrl)
    target = re.compile(r'{"id":.*?articlesCount":')
    tuple = re.findall(target, info)
    for index in range(len(tuple)):
        data = tuple[index]
        if data != None:
            jsonData = data + "0}"
            try:
                userDataReBuild = json.loads(jsonData)
                tempToken = userDataReBuild['urlToken']
                if tempToken not in finishFindList:
                    insertList.append(userDataReBuild)
                    finishFindList[tempToken] = True
                    if tempToken not in tempWait:
                        tempWait[tempToken] = True
                        waitFindList.append(tempToken)
            except Exception as e:
                print(e)


def CheckWait():
    tempToken = waitFindList[0]
    waitFindList.pop(0)
    GetUserTuple(GetFollowingUrl(tempToken))
    GetUserTuple(GetFollowersUrl(tempToken))


def LoopSetData():
    global insertList
    state = (NeedBreak() or waitFindList.count == 0)
    while(state == False):
        ShowState()
        CheckWait()
        if len(insertList) > 20:
            mongo.InsertDicts(insertList)
            insertList = []

        state = (NeedBreak() or waitFindList.count == 0)

    print("Success")


def Step():
    InitGetDbData()
    if len(waitFindList) == 0:
        waitFindList.append("haozhi")
    # LoopSetData()

    threads = []
    for i in range(1):
        threads.append(threading.Thread(target=CheckWaitThread))

    for tempThread in threads:
        tempThread.start()


GetWaitLock = threading.Lock()
PushFinishLock = threading.Lock()


def TryInsertThread():
    global insertList
    if len(insertList) > 100:
        mongo.InsertDicts(insertList)
        insertList = []


def GetWaitThread():
    tempToken = None
    GetWaitLock.acquire()
    if len(waitFindList) > 0:
        ShowState()
        while(len(waitFindList) > 0):
            tempToken = waitFindList[0]
            waitFindList.pop(0)
            tempWait.pop(tempToken)
            if tempToken not in finishFindList:
                finishFindList[tempToken] = True
                dic = {}
                dic["tempToken"] = tempToken
                finishMongo.InsertDict(dic)
                break
    GetWaitLock.release()
    return tempToken


def PushWaitThread(tempToken, userDataReBuild):
    PushFinishLock.acquire()
    if ((tempToken not in tempWait) and (tempToken not in finishFindList)):
        tempWait[tempToken] = True
        waitFindList.append(tempToken)
        if tempToken not in collectList:
            collectList[tempToken] = True
            insertList.append(userDataReBuild)
            TryInsertThread()
    PushFinishLock.release()


def CheckWaitThread():
    while(True):
        tempToken = GetWaitThread()
        if tempToken == None:
            time.sleep(1)
        else:
            GetUserTupleThread(GetFollowingUrl(tempToken))
            GetUserTupleThread(GetFollowersUrl(tempToken))


def GetUserTupleThread(targetUrl):
    print('request...')
    info = GetWebInfo(targetUrl)
    target = re.compile(r'{"id":.*?articlesCount":')
    tuple = re.findall(target, info)
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

    time.sleep(random.uniform(0.02, 0.3))


Step()
