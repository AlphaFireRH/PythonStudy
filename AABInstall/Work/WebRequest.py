#!use/bin/env python3
# -*- coding utf-8 -*-

import io
import sys
import random
import time
import json
import re
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

user_agents = [
    "Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02",
    "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3",
    "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
]

http_ip = [
    '119.101.117.134:9999',
    '125.40.238.181:56738',
    '139.198.191.107:1080',
    '106.15.42.179:33543',
    '183.185.78.49:80',
    '122.117.65.107:38614',
    '119.180.175.167:8060',
    '112.85.164.94:9999',
    '61.176.223.7:58822',
    '47.107.158.219:8000',
    '112.87.70.162:9999'
]
tryNumber = 0


def open_url(url_str, proxy_ip):
    html = ""
    headerInfo = GetHeaders()

    if bool(proxy_ip):
        html = requests.get(url=url_str,  headers=headerInfo,
                            proxies=proxy_ip).content.decode('utf8')

    else:
        html = requests.get(
            url=url_str, headers=headerInfo).content.decode('utf8')
    # 返回网页内容,动态加载的需要另行处理
    return html


def GetWebInfo(url_str, proxy_ip):
    html = ""
    headerInfo = GetHeaders()

    #

    if bool(proxy_ip):
        print(url_str)
        proxy = urllib3.ProxyManager(
            'http://'+proxy_ip['http'], headers=headerInfo)
        r = proxy.request('get', url_str)
        print('status ' + str(r.status))
        html = r.data.decode()
        # print(html.decode())
    else:
        http = urllib3.PoolManager(timeout=30)
        r = http.request(
            'GET', url_str, headers=headerInfo
        )
        print('status ' + str(r.status))
        html = r.data.decode()
    return (html)


def open_url_random_host(url_str):
    global tryNumber
    html = ""
    # print(url_str)
    if len(http_ip) == 0 or tryNumber > 1000:
        UpDateHttpIP()
    elif len(http_ip) > 0:
        try:
            proxy_ip = GetProxy_ip()

            # print('使用代理的IP:', proxy_ip)
            html = open_url(url_str, proxy_ip)
            tryNumber += 1
        except Exception as e:
            print(e)
            html = ""
    return html


# 随机获取请求头
def GetHeaders():
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }
    return headers

# 随机获取代理IP


def GetProxy_ip():
    proxy_ip = {
        'http': random.choice(http_ip),
    }
    return proxy_ip


def UpDateHttpIP():
    print("~~~~~~~~~~~~~~~~~~~UpdateIp~~~~~~~~~~~~~~~~~~~~")
    global tryNumber
    tryNumber = 0
    http_ip = []

    info = GetWebInfo(
        'http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=', '')
    target = re.compile(r';\n</script>\n.*?<br>高效')
    tuple = re.findall(target, info)

    for index in range(len(tuple)):
        data = tuple[index]
        if data != None:
            data = str(data).replace(';\n</script>\n', '')
            data = str(data).replace('<br>高效', '')

            values = data.split('<br>')
            try:
                for tempIp in values:
                    if tempIp not in http_ip:
                        http_ip.append(tempIp)
            except Exception as e:
                print(e)

    # print('request...'+targetUrl)


UpDateHttpIP()

# '''
# 该脚本使用说明:

# 使用免费的代理或者自己购买的代理,打开指定的网页地址,模拟用户使用独立IP访问相同页面
# 这里演示,使用的是89免费代理,地址:http://www.89ip.cn/
# 可以使用http://filefab.com/查看IP

# http_ip:
# 可以自行编辑添加更多代理
# url_str:
# 可以自行编辑为需要打开的网页地址

# '''


# url_str = 'https://vku.youku.com/live/ilproom?spm=a2hlv.20025885.0.0&id=8009372&scm=20140666.manual.65.live_8014311'

# print("访问的网页地址:", url_str)


# '''
# 循环执行,每次访问后等待指定时间后重新访问,避免过于频繁
# max_count:
# 可以自行编辑,访问多少次后自动终止
# sleep_time:
# 可以自行编辑,等待多久后重新发起新的独立IP访问
# '''

# flag = True
# max_count = 3
# sleep_time = 3

# print('共计需要访问', url_str, '网页', max_count, '次')

# # 这里只做简单演示请求,单次延时访问,并发可以使用asyncio,aiohttp
# while flag:
#     proxy_ip = {
#         'http': random.choice(http_ip),
#     }

#     print('使用代理的IP:', proxy_ip)
#     html = open_url(url_str, proxy_ip)

#     # 解析网页内容,可以使用BeautifulSoup
#     print('返回网页内容长度:', len(html))

#     time.sleep(sleep_time)
#     print('等待', sleep_time, '秒后,重新使用独立IP发起网页请求')

#     max_count -= 1

#     if(max_count == 0):
#         flag = False

# print("执行结束")
