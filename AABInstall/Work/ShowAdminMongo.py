#!use/bin/env python3
# -*- coding utf-8 -*-

import os

path = os.path.split(os.path.realpath(__file__))[0]

# 打开控制台


def OpenAdminMongo():
    targetPath = 'cd ' + path + 'Tool\\adminMongo-master\\'
    print(targetPath)
    cmdInfo = targetPath
    os.system(cmdInfo)

    cmdInfo = "npm start"
    os.system(cmdInfo)


OpenAdminMongo()
