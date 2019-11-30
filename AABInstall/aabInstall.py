#!use/bin/env python
# -*- coding utf-8 -*-

import os
import Work.ExcelSet
import Work.fileTool
import Work.miniGame
# from Work import *

path = os.path.split(os.path.realpath(__file__))[0]

aabPath = path + "/bundle.aab"
apksPath = path + "/bundle.apks"
jsonFilePath = path + "/tcl.json"
splitePath = path + "/splite/"
apkPath = path + "/package.apk"


# input
def PleaseInputPath():
    info = 'please input package path: \n'
    return info


# get input
def GetInput():
    return input(PleaseInputPath())


# menu
def GetShowInfo():
    info = '\n\n*************************\n'
    info += 'Enter your input:\n'

    info += ('1、output apks: \n')
    info += ('2、install apks(needLink phone): \n')
    info += ('3、output JSON file(needLink phone): \n')
    info += ('4、splite apks: \n')
    info += ('5、normal install pak: \n')
    info += ('6、show all log: \n')
    info += ('7、show error log: \n')
    info += ('8、clean log: \n')
    info += ('9、show apk info: \n')
    info += ('10、show installed info: \n')
    info += ('11、Excel to json: \n')

    info += ('100、test: \n')

    info += '*************************\n\n'
    return info


# get user input
while True:
    val = input(GetShowInfo())
    val = int(val)
    if val == 1:
        Work.fileTool.OutputAPKS(GetInput(), apksPath)
    elif val == 2:
        Work.fileTool.Install(apksPath)
    elif val == 3:
        Work.fileTool.OutputJSON(jsonFilePath)
    elif val == 4:
        Work.fileTool.SpliteAPKS(apksPath, jsonFilePath, splitePath)
    elif val == 5:
        Work.fileTool.NormalInstall(GetInput())
    elif val == 6:
        Work.fileTool.ShowAllLog()
    elif val == 7:
        Work.fileTool.ShowErrorLog()	
    elif val == 8:
        Work.fileTool.CleanLog()
    elif val == 9:
        Work.fileTool.ShowApkInfoFromAAPT(GetInput())
    elif val == 10:
        Work.fileTool.ShowInstalledInfoFromAAPT(GetInput())
    elif val == 11:
        Work.ExcelSet.ThemeExcelToJson(GetInput())
    elif val == 12:
        Work.ExcelSet.EmojiEffectToJson(GetInput())
    elif val == 13:
        Work.miniGame.LevelDataToJson(GetInput())
    elif val == 14:
        Work.miniGame.WordDataToJson(GetInput())

# elif val==100:
