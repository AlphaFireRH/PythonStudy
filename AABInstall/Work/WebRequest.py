#!use/bin/env python3
# -*- coding utf-8 -*-

import io
import sys
import random
import ProxyMgr
import time
# import json
# import re
import requests
import urllib3
# from bs4 import BeautifulSoup
from UserAgentMgr import GetHeaders
import gzip


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

tryNumber = 0


def open_url(url_str, proxy_ip):
    url_str = url_str.replace(" ", "")
    html = ""
    headerInfo = GetHeaders()
    session = requests.session()
    session.headers = headerInfo
    if bool(proxy_ip):
        session.proxies = proxy_ip
        # session.max_redirects = 200
        r = session.get(url_str, allow_redirects=True)
        r.keep_alive = True
        if r.status_code == 200:
            # print(gzip.decompress(r.content))
            html = str(r.content, encoding='utf-8')
    else:
        html = str(requests.get(
            url=url_str, headers=headerInfo).content, 'utf8')

        r.keep_alive = True
    # 返回网页内容,动态加载的需要另行处理
    return html


def open_url_urllib3(url_str, proxyIp):
    url_str = url_str.replace(" ", "")
    html = ""
    headerInfo = GetHeaders()
    proxy = urllib3.ProxyManager(
        'http://'+proxyIp, headers=headerInfo)
    r = proxy.request('get', url_str)
    r.keep_alive = True
    if r.status == 200:
        html = r.data.decode()
    else:
        print(r.status)

    # print(html)
    return (html)


def GetWebInfo(url_str, proxy_ip):
    url_str = url_str.replace(" ", "")
    html = ""
    headerInfo = GetHeaders()

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

    while tryNum < 10:
        try:
            proxyIp = ProxyMgr.GetProxy_ip_str()
            html = open_url(url_str, proxyIp)
            if html != "":
                tryNumber += 1
                break
        except Exception as e:
            print(url_str)
            print(proxyIp)
            print(e)
            html = ""
            tryNum += 1
        time.sleep(random.uniform(1, 3))
    return html

# proxyIp = ProxyMgr.GetProxy_ip_str()
# open_url_urllib3(
#     "https://www.zhihu.com/people/guo-zi-501/following", proxyIp['http'])
# print(open_url("https://www.zhihu.com/people/guo-zi-501/following",
#                {'http': '120.83.109.68:9999'}))

# "https: // www.zhihu.com/people/zhang-xiao-bei/following?page = 3 https: // www.zhihu.com/people/tian-ji-shun/following?page = 3 https: // www.zhihu.com/people/warfalcon/following?page = 2 https: // www.zhihu.com/people/zhang-xiao-bei/following?page = 4 https: // www.zhihu.com/people/warfalcon/followers?page = 2 "
