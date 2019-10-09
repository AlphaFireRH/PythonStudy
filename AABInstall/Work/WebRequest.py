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
import UserAgentMgr
import ProxyMgr
#from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

tryNumber = 0


def open_url(url_str, proxy_ip):
    url_str = url_str.replace(" ", "")
    html = ""
    headerInfo = UserAgentMgr.GetHeaders()
    session = requests.session()
    session.headers = headerInfo
    if bool(proxy_ip):
        session.proxies = proxy_ip
        # session.max_redirects = 200
        r = session.get(url_str, allow_redirects=True)
        if r.status_code == 200:
            html = r.content.decode('utf8')
        r.keep_alive = True
    else:
        r = requests.get(
            url=url_str, headers=headerInfo).content.decode('utf8')
        r.keep_alive = True
    # 返回网页内容,动态加载的需要另行处理
    return html


def open_url_urllib3(url_str, proxyIp):
    url_str = url_str.replace(" ", "")
    html = ""
    headerInfo = UserAgentMgr.GetHeaders()
    proxy = urllib3.ProxyManager(
        'http://'+proxyIp, headers=headerInfo)
    r = proxy.request('GET', url_str)
    if r.status == 200:
        html = r.data.decode()
    r.keep_alive = False
    # print(html)
    return (html)


def GetWebInfo(url_str, proxy_ip):
    url_str = url_str.replace(" ", "")
    html = ""
    headerInfo = UserAgentMgr.GetHeaders()

    if bool(proxy_ip):
        print(url_str)
        proxy = urllib3.ProxyManager(
            'http://'+proxy_ip['http'], headers=headerInfo)
        r = proxy.request('get', url_str)
        if r.status == 200:
            html = r.data.decode()
    else:
        http = urllib3.PoolManager(timeout=30)
        r = http.request(
            'GET', url_str, headers=headerInfo
        )
        if r.status == 200:
            html = r.data.decode()
    # print(html.decode())
    return (html)


def open_url_random_host(url_str):
    url_str = url_str.replace(" ", "")
    global tryNumber
    html = ""
    # print(url_str)
    tryNum = 0
    proxyIp = ""
    if len(ProxyMgr.http_ip) == 0 or tryNumber > 1000:
        tryNumber = 0
        ProxyMgr.UpDateHttpIP()

    while tryNum < 1:
        try:
            proxyIp = ProxyMgr.GetProxy_ip_str()
            html = open_url(url_str, proxyIp)
            tryNumber += 1
            break
        except Exception as e:
            print(url_str)
            print(proxyIp)
            print(e)
            html = ""
            tryNum += 1
    return html


# open_url_urllib3(
#     "https://www.zhihu.com/people/haozhi/following", "120.83.109.68:9999")
# print(open_url("https://www.zhihu.com/people/zhi-ke-ji-13/followers?page=4",{'http': '92.255.248.230:45906'}))

# "https: // www.zhihu.com/people/zhang-xiao-bei/following?page = 3 https: // www.zhihu.com/people/tian-ji-shun/following?page = 3 https: // www.zhihu.com/people/warfalcon/following?page = 2 https: // www.zhihu.com/people/zhang-xiao-bei/following?page = 4 https: // www.zhihu.com/people/warfalcon/followers?page = 2 "
