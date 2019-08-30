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
