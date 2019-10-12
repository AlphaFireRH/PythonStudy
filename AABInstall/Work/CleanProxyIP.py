#!use/bin/env python3
# -*- coding utf-8 -*-

import requests
import socket
import re
socket.setdefaulttimeout(3)


# 用这个网页去验证，遇到不可用ip会抛异常
url1 = "http://ip.chinaz.com/getip.aspx"
url2 = "http://proxy.mimvp.com/check.php"
url3 = "https://httpbin.org/ip"


def CheckProxyIPStatus1(proxys):  # 检测高匿代理
    good = []
    for proxy in proxys:
        try:
            ip = proxy['http']
            session = requests.session()
            session.proxies = ip
            r = session.get(url1, allow_redirects=True)
            realSIp = GetRealIp(str(r.content, encoding='utf-8'))
            valid_ip = ip
            good.append(valid_ip)
        except Exception as e:
            print(str(e))
            continue
    return good


def CheckProxyIPStatus2(proxys):  # 检测高匿代理
    good = []
    for proxy in proxys:
        try:
            ip = proxy['http']
            session = requests.session()
            session.proxies = ip
            r = session.get(url2, allow_redirects=True)
            realSIp = GetRealIp(str(r.content, encoding='utf-8'))
            if realSIp == "":
                valid_ip = ip
                good.append(valid_ip)
            else:
                print(realSIp)
        except Exception as e:
            print(str(e))
            continue
    return good


def CheckProxyIPStatus3(proxys):  # 检测高匿代理
    good = []
    for proxy in proxys:
        try:
            ip = proxy['http']
            session = requests.session()
            session.proxies = ip
            r = session.get(url3, allow_redirects=True)
            realSIp = GetRealIp(str(r.content, encoding='utf-8'))
            print(realSIp)
            if realSIp == "":
                valid_ip = ip
                good.append(valid_ip)
            else:
                print(realSIp)
        except Exception as e:
            print(str(e))
            continue
    return good


def GetRealIp(html):
    # print(html)
    realIP = ""
    target = re.compile(r'<font color="red">.*?</font>')
    tuple = re.findall(target, html)
    if tuple is not None:
        for index in range(len(tuple)):
            data = tuple[index]
            if data != None and data != "":
                try:
                    realIP = GetIPString(data)
                except Exception as e:
                    print(str(e))
                    realIP = ""
    return realIP


def GetIPString(target):
    cop = re.compile("[^.^0-9]")
    return cop.sub("", target)


def main():
    CheckProxyIPStatus2([{"http": "163.204.245.249:9999"}])


if __name__ == '__main__':
    main()
