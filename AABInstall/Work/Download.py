#!use/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from alive_progress import alive_bar
from UserAgentMgr import GetHeaders

path = os.path.split(os.path.realpath(__file__))[0]


def DownloadTarget(filePath, url):
    res = requests.get(url, stream=True)
    if res.ok:
        total_size = int(int(res.headers.get("Content-Length"))/1024+0.5)
        # 下载文件
        with open(filePath, 'wb') as fd:
            with alive_bar(total_size) as bar:   # declare your expected total
                for data in res.iter_content(chunk_size=1024):
                    fd.write(data)
                    bar()


def TestTarget(url):
    headerInfo = GetHeaders()
    response = requests.get(url)
    response.headers = headerInfo
    print(response.text)


def main():
    # DownloadTarget(path+"/download.111", "https://xiazai.xqishu.com/txt/%E5%89%91%E7%8E%8B%E6%9C%9D.txt")
    TestTarget("https://histonegames.sharepoint.com/:x:/r/sites/p160/_layouts/15/Doc.aspx?sourcedoc= % 7B5A6BA968-B430-44DA-B9F6-926F3A09D8A9 % 7D & file=Word % 20Serenity % 20 % E7 % AB % 8B % E9 % A1 % B9 % E7 % B3 % BB % E7 % BB % 9F % E8 % AE % BE % E8 % AE % A1.xlsx & action=default & mobileredirect=true & cid=5e582617-1a28-4d1a-9bd2-f310f80cf277")
    # DownloadTarget(path+"/download.111", "https://excel.officeapps.live.com/x/_layouts/XlFileHandler.aspx?WacUserType=WOPI&usid=e16f9ac0-5f8f-4161-a098-48edf5d5e103&NoAuth=1&waccluster=PHK1")
    print("\n\n-------------Finish-------------\n\n")
    os.system("pause")


if __name__ == '__main__':
    main()
