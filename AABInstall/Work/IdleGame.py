#!use/bin/env python
# -*- coding utf-8 -*-

import os
import myopenpyxl
import json
import stat
import codecs
import tool_jsonString
import tool_file


def ClientConfigToJson(filePath):
    wb = myopenpyxl.OpenXlsxFullName(filePath)

    targetPath = os.path.split(filePath)[0] + "\\"

    SetSceneAndRole(targetPath, wb)
    SetConstClient(targetPath, wb)
    SetModel(targetPath, wb)
    SetAnimation(targetPath, wb)
    SetIcon(targetPath, wb)

    print("OK")


def SetConstClient(filePath, wb):
    ws = myopenpyxl.GetTargetSheet(wb, 'const_client')
    len = myopenpyxl.GetMaxRow(ws)

    tempArr = []
    for i in range(len):
        index = i+1
        if (index > 2):
            pos = "A{0}:B{1}".format(str(index), str(index))
            list = myopenpyxl.GetTargetCells(ws, pos)[0]
            dictData = {}
            dictData['Id'] = list[0].value
            dictData['Value'] = list[1].value
            tempArr.append(dictData)
    tool_file.WriteText(json.dumps(
        tempArr), filePath + "ConstConfig.txt")


def SetSceneAndRole(filePath, wb):
    ws = myopenpyxl.GetTargetSheet(wb, 'scene_role')
    len = myopenpyxl.GetMaxRow(ws)

    tempArr = []
    for i in range(len):
        index = i+1
        if (index > 2):
            pos = "A{0}:B{1}".format(str(index), str(index))
            list = myopenpyxl.GetTargetCells(ws, pos)[0]
            dictData = {}
            dictData['Id'] = list[0].value
            dictData['RoleId'] = str(list[1].value)
            tempArr.append(dictData)
    tool_file.WriteText(json.dumps(
        tempArr), filePath + "SceneRoleConfig.txt")


def SetModel(filePath, wb):
    ws = myopenpyxl.GetTargetSheet(wb, 'model')
    len = myopenpyxl.GetMaxRow(ws)

    tempArr = []
    for i in range(len):
        index = i+1
        if (index > 2):
            pos = "A{0}:C{1}".format(str(index), str(index))
            list = myopenpyxl.GetTargetCells(ws, pos)[0]
            dictData = {}
            dictData['Id'] = list[0].value
            dictData['RoleId'] = list[1].value
            dictData['PrefabName'] = str(list[2].value)
            tempArr.append(dictData)
    tool_file.WriteText(json.dumps(tempArr), filePath + "ModelConfig.txt")


def SetAnimation(filePath, wb):
    ws = myopenpyxl.GetTargetSheet(wb, 'amin')
    len = myopenpyxl.GetMaxRow(ws)

    tempArr = []
    for i in range(len):
        index = i+1
        if (index > 2):
            pos = "A{0}:E{1}".format(str(index), str(index))
            list = myopenpyxl.GetTargetCells(ws, pos)[0]
            dictData = {}
            dictData['Id'] = list[0].value
            dictData['RoleId'] = list[1].value
            dictData['AniType'] = list[2].value
            dictData['CycleNum'] = list[3].value
            dictData['AniName'] = str(list[4].value)
            tempArr.append(dictData)
    tool_file.WriteText(json.dumps(
        tempArr), filePath + "AnimationConfig.txt")


def SetIcon(filePath, wb):
    ws = myopenpyxl.GetTargetSheet(wb, 'icon_table')
    len = myopenpyxl.GetMaxRow(ws)

    tempArr = []
    for i in range(len):
        index = i+1
        if (index > 2):
            pos = "A{0}:F{1}".format(str(index), str(index))
            list = myopenpyxl.GetTargetCells(ws, pos)[0]
            dictData = {}
            dictData['Id'] = list[0].value
            dictData['Type'] = list[1].value
            dictData['SubType'] = list[2].value
            dictData['Lv'] = list[3].value
            dictData['Icon'] = str(list[4].value)
            dictData['Name'] = str(list[5].value)
            tempArr.append(dictData)
    tool_file.WriteText(json.dumps(tempArr), filePath + "IconConfig.txt")


def GetIntValue(obj):
    return obj.value


def GetStringValue(obj):
    return str(obj.value)


def main():
    ClientConfigToJson(input('please input package path: \n'))


if __name__ == '__main__':
    main()
