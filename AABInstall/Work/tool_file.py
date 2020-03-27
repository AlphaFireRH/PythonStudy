#!use/bin/env python3
# -*- coding utf-8 -*-

import os
import shutil
import stat
import hashlib
import math
from decimal import *

path = os.path.split(os.path.realpath(__file__))[0]


def FileExists(path):
    if os.path.isfile(path):
        return True
    return False


def GetMD5(targetPath):  # 获取md5值
    if not os.path.isfile(targetPath):
        return
    myhash = hashlib.md5()
    f = open(targetPath, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def GetFileSize(targetPath):  # 获取文件体积
    file_size = float(os.stat(targetPath).st_size)
    targetValue = ""
    for i in range(5):
        if i > 0:
            index = 5-i
            if(file_size > math.pow(1024, index)):
                result = float("%0.2f" % (file_size/math.pow(1024, index)))
                targetValue = str(result)
                if index == 5:
                    targetValue = targetValue+"P"
                if index == 4:
                    targetValue = targetValue+"T"
                if index == 3:
                    targetValue = targetValue+"G"
                if index == 2:
                    targetValue = targetValue+"M"
                if index == 1:
                    targetValue = targetValue+"K"
                break

    return targetValue


def DeleteFile(path):  # 删除文件
    if (os.path.exists(path)):
        os.remove(path)


def RenameFile(srcfile, dstfile):  # 重命名文件
    if (os.path.exists(srcfile)):
        os.rename(srcfile, dstfile)


def MoveFile(srcfile, dstfile):  # 移动文件
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.move(srcfile, dstfile)  # 移动文件


def CopyFile(srcfile, dstfile):  # 复制文件
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件


def CreateDir(path):  # 创建文件夹
    os.mkdir(path)


def DeleteDir(rootdir):  # 删除文件夹
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
