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
url4 = "https://probe.my.to"


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


def CheckProxyIPStatus3(proxys):  # 检测高匿代理
    good = []
    for proxy in proxys:
        try:
            ip = proxy['http']
            session = requests.session()
            session.proxies = ip
            r = session.get(url4, allow_redirects=True)
            print(str(r.content, encoding='utf-8'))
            target = re.compile(r'"origin": ".*?"')
            realSIp = re.findall(target, str(r.content, encoding='utf-8'))[0]
            # print(str.format("realSIp: {0} , status_code: {1}", str(r.content, encoding='utf-8'), r.status_code))
            if realSIp == "":
                valid_ip = ip
                good.append(valid_ip)
            else:
                print(realSIp)
        except Exception as e:
            print(str(e))
            continue
    return good


def CheckProxyIPStatus4(proxys):  # 检测高匿代理
    good = []
    for proxy in proxys:
        try:
            ip = proxy['http']
            if testConnection(proxy):
                valid_ip = ip
                good.append(valid_ip)
        except Exception as e:
            print(str(e))
            continue
    return good


def testConnection(proxy):  # 通过检测icanhazip.com回显来检测可用性及匿名性
    try:
        ip = proxy['http']
        OrigionalIP = requests.get(
            "http://icanhazip.com", timeout=20).content

        session = requests.session()
        session.proxies = "http://"+ip
        MaskedIP = session.get(
            "http://icanhazip.com", timeout=20).content
        print(str.format(
            "OrigionalIP: {0} , MaskedIP: {1} , result: {2}", OrigionalIP, MaskedIP, OrigionalIP != MaskedIP))
        if OrigionalIP != MaskedIP:
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return False


def GetIPString(target):
    cop = re.compile("[^.^0-9]")
    return cop.sub("", target)


def main():
    CheckProxyIPStatus3([{"http": "200.111.182.6:443"}])


if __name__ == '__main__':
    main()
