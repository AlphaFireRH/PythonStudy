#!use/bin/env python3
# -*- coding utf-8 -*-

import random
import requests
import json
import re

http_ip = []


def GetProxy_ip():  # 随机获取代理IP
    proxy_ip = {
        'http': random.choice(http_ip),
    }
    return proxy_ip


def GetProxy_ip_str():  # 随机获取代理IP
    return random.choice(http_ip)


def UpDateHttpIP():  # 更新IP
    print("~~~~~~~~~~~~~~~~~~~UpdateIp~~~~~~~~~~~~~~~~~~~~")
    global http_ip
    while(True):
        PushInPool()
        http_ip = RemoveBadProxy(http_ip)
        if len(http_ip) > 0:
            break


def PushInPool():  # 新IP入池
    global http_ip
    response = requests.get(
        'http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=', timeout=5)
    if response.status_code == 200:
        target = re.compile(r';\n</script>\n.*?<br>高效')
        tuple = re.findall(target, response.content.decode('utf8'))
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


def RemoveBadProxy(proxys):  # 移除无效IP
    badNum = 0
    goodNum = 0
    good = []
    for proxy in proxys:
        try:
            proxy_host = proxy
            protocol = 'https' if 'https' in proxy_host else 'http'
            proxies = {protocol: proxy_host}
            response = requests.get(
                'https://www.baidu.com', proxies=proxies, timeout=10)
            if response.status_code != 200:
                badNum += 1
                print(proxy_host, 'bad proxy')
            else:
                goodNum += 1
                good.append(proxies)
                print(proxy_host, 'success proxy')
        except Exception as e:
            print(e)
            # print proxy_host, 'bad proxy'
            badNum += 1
            continue
    print('success proxy num : ', goodNum)
    print('bad proxy num : ', badNum)
    return good


def region():
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
    UpDateHttpIP()
