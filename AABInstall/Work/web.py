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
maxUserNumber = 100000000
base = 'href="//www.zhihu.com/people/'

#  https://www.zhihu.com/people/haozhi/following
# allUser={}
finishFindDic = {}
collectList = {}
insertList = []

waitFindList = []
tempWaitDic = {}


def InitGetDbData():
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
    print("请求完毕")


def ShowState():
    print("changeUser")
    print("now collect " + str(len(collectList)))
    print("now finish " + str(len(finishFindDic)))
    print("wait " + str(len(waitFindList)))


def NeedBreak():
    state = False
    if len(finishFindDic) >= maxUserNumber:
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
                if tempToken not in finishFindDic:
                    insertList.append(userDataReBuild)
                    finishFindDic[tempToken] = True
                    if tempToken not in tempWaitDic:
                        tempWaitDic[tempToken] = userDataReBuild['followerCount']
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
        tempWaitDic["haozhi"] = 0
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
    if len(insertList) > 200:
        mongo.InsertDicts(insertList)
        insertList = []


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

        # while(len(waitFindList) > 0):
        #     tempToken = waitFindList[0]
        #     waitFindList.pop(0)
        #     tempWaitDic.pop(tempToken)
        #     if tempToken not in finishFindDic:
        #         finishFindDic[tempToken] = True
        #         dic = {}
        #         dic["tempToken"] = tempToken
        #         finishMongo.InsertDict(dic)
        #         break
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


def WaitFindListSort():
    waitFindList.sort(key=lambda x: tempWaitDic[x], reverse=True)


def CheckWaitThread():
    while(True):
        tempToken = GetWaitThread()
        if tempToken == None:
            time.sleep(1)
        else:
            followingNumber, followerNumber = GetFollowingAndFollowerNumber(
                GetFollowingUrl(tempToken))

            time.sleep(1)

            for num in range(1 + (followingNumber-1)//10):
                time.sleep(random.uniform(0.02, 0.3))
                if num == 0:
                    GetUserTupleThread(GetFollowingUrl(tempToken))
                else:
                    GetUserTupleThread(GetFollowingUrl(
                        tempToken)+'?page='+str(num+1))

            for num in range(1 + (followerNumber-1)//10):
                time.sleep(random.uniform(0.02, 0.3))
                if num == 0:
                    GetUserTupleThread(GetFollowersUrl(tempToken))
                else:
                    GetUserTupleThread(GetFollowersUrl(
                        tempToken)+'?page='+str(num+1))


def GetUserTupleThread(targetUrl):
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

    print('request...'+targetUrl)
    time.sleep(random.uniform(0.02, 0.3))


def GetFollowingAndFollowerNumber(targetUrl):
    info = GetWebInfo(targetUrl)
    target = re.compile(
        r'<strong class="NumberBoard-itemValue" title=".*?">')
    tuple = re.findall(target, info)

    followingNumber = 0
    followerNumber = 0
    for index in range(len(tuple)):
        data = tuple[index]
        if data != None:
            data = str(data).replace(
                '<strong class="NumberBoard-itemValue" title="', '')
            data = data.replace(
                '">', '')
            if index == 0:
                followingNumber = int(data)
            else:
                followerNumber = int(data)
    return followingNumber, followerNumber


Step()
