#!use/bin/env python3
# -*- coding utf-8 -*-

import requests
import socket
import re
socket.setdefaulttimeout(3)


# 用这个网页去验证，遇到不可用ip会抛异常
url = "http://ip.chinaz.com/getip.aspx"
url2 = "http://proxy.mimvp.com/check.php"


def CheckProxyIPStatus(proxys):  # 检测高匿代理
    good = []
    for proxy in proxys:
        # try:
        ip = proxy['http']
        print(ip)
        session = requests.session()
        session.proxies = ip
        r = session.get(url2, allow_redirects=True)
        realSIp = GetRealIp(str(r.content, encoding='utf-8'))
        if realSIp == "":
            valid_ip = ip[5:]
            good.append(valid_ip)
        else:
            print(realSIp)
        # except Exception as e:
        #     print(str(e))
        #     continue
    return good


def GetRealIp(html):
    realIP = ""
    target = re.compile(r'<font color="red">.*?</font>')
    cop = re.compile("[^.^0-9]")
    tuple = re.findall(target, html)
    if tuple is not None:
        for index in range(len(tuple)):
            data = tuple[index]
            if data != None and data != "":
                try:
                    realIP = cop.sub("", data)
                except Exception as e:
                    print(str(e))
                    realIP = ""
    return realIP


def main():
    CheckProxyIPStatus([{"http": "61.178.149.237:59042"}])


if __name__ == '__main__':
    main()
