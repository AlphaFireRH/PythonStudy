#!use/bin/env python3
# -*- coding utf-8 -*-

import os
import shutil
import stat

path = os.path.split(os.path.realpath(__file__))[0]


# 删除文件
def DeleteFile(path):
    if (os.path.exists(path)):
        os.remove(path)

# 删除文件夹


def CreateDir(path):
    os.mkdir(path)


def DeleteDir(rootdir):
    if (os.path.exists(rootdir)):
        filelist = []
        filelist = os.listdir(rootdir)  # 列出该目录下的所有文件名
        for f in filelist:
            filepath = os.path.join(rootdir, f)  # 将文件名映射成绝对路劲
            if os.path.isfile(filepath):  # 判断该文件是否为文件或者文件夹
                os.remove(filepath)  # 若为文件，则直接删除
                print(str(filepath)+" removed!")
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath, True)  # 若为文件夹，则删除该文件夹及文件夹内所有文件
            print("dir "+str(filepath)+" removed!")
        shutil.rmtree(rootdir, True)  # 最后删除img总文件夹
        print("删除成功")


def WriteText(info, targetPath):
    DeleteFile(targetPath)

    fo = open(targetPath, "w+")
    fo.write(info)
    fo.close()


def WriteTextForByte(info, targetPath):
    DeleteFile(targetPath)

    fo = open(targetPath, "wb+")
    fo.write(info.encode('utf-8'))
    fo.close()


def ReadText(targetPath):
    info = ""
    fo = open(targetPath, "r")
    info = fo.read()
    fo.close()
    return info


def ReadTextForByte(targetPath):
    info = ""
    fo = open(targetPath, "rb")
    info = fo.read()
    fo.close()
    return info
