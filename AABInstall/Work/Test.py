import os
import urllib3
from alive_progress import alive_bar
# from UserAgentMgr import GetHeaders

path = os.path.split(os.path.realpath(__file__))[0]


def DownloadTarget(filePath, url):
    http = urllib3.PoolManager()
    res = http.request('GET', url)
    if res.status == 200:
        print(res.data)
        total_size = int(int(res.headers.get("Content-Length"))/1024+0.5)
        # 下载文件
        with open(filePath, 'wb') as fd:
            with alive_bar(total_size) as bar:   # declare your expected total
                for data in res.iter_content(chunk_size=1024):
                    fd.write(data)
                    bar()


# def TestTarget(url):
#     headerInfo = GetHeaders()
#     response = requests.get(url)
#     response.headers = headerInfo
#     print(response.text)


def main():
    DownloadTarget(path+"/download.111", "https://excel.officeapps.live.com/x/_layouts/XlFileHandler.aspx?WacUserType=WOPI&usid=e16f9ac0-5f8f-4161-a098-48edf5d5e103&NoAuth=1&waccluster=PHK1")
    print("\n\n-------------Finish-------------\n\n")


if __name__ == '__main__':
    main()
