#!use/bin/env python
# -*- coding utf-8 -*-

import Work.myopenpyxl
import json
import stat
import codecs
import Work.tool_jsonString
import Work.tool_file


def ThemeExcelToJson(filePath):
    wb = Work.myopenpyxl.OpenXlsxFullName(filePath)
    ws = Work.myopenpyxl.GetTargetSheet(wb, 'Sheet')

    len = Work.myopenpyxl.GetMaxRow(ws)

    jsonInfo = "["
    for i in range(len):
        tempStr = ""

        tempStr = "{\"Id\":\""
        tempStr += (str(Work.myopenpyxl.GetTargetCell(ws,
                                                      'A' + str(i + 1)).value) + "\"")
        tempStr += ",\"resId\":\""
        tempStr += (Work.myopenpyxl.GetTargetCell(ws,
                                                  'C' + str(i + 1)).value + "\"")
        tempStr += ",\"tName\":\""
        tempStr += (Work.myopenpyxl.GetTargetCell(ws,
                                                  'C' + str(i + 1)).value + "\"")
        tempStr += ",\"level\":"
        tempStr += (str(Work.myopenpyxl.GetTargetCell(ws,
                                                      'B' + str(i + 1)).value) + "}")

        if i == 0:
            jsonInfo += tempStr
        else:
            jsonInfo += "," + tempStr
    jsonInfo += "]"

    print(jsonInfo)


def LanagueToExcel(filePath):
    fo = open(filePath, "r")
    tempName = fo.name
    info = fo.read()
    fo.close()

    data = json.loads(info)

    wb = Work.myopenpyxl.CreateNewXlsx(tempName)
    ws = Work.myopenpyxl.GetNowActiveSheet(wb)
    num = 1
    for temp in data:
        index = str(num)
        Work.myopenpyxl.SetTargetCellPos(ws, 'A' + index, temp['Key'])
        Work.myopenpyxl.SetTargetCellPos(ws, 'B' + index, temp['Value'])
        num = num + 1
    Work.myopenpyxl.WriteXlsx(wb, tempName)


def RandomToExcel(filePath):
    fo = open(filePath, "r")
    tempName = fo.name
    info = fo.read()
    fo.close()

    data = json.loads(info)

    wb = Work.myopenpyxl.CreateNewXlsx(tempName)
    ws = Work.myopenpyxl.GetNowActiveSheet(wb)
    num = 1
    for temp in data:
        index = str(num)
        Work.myopenpyxl.SetTargetCellPos(ws, 'A' + index, temp['seed'])
        Work.myopenpyxl.SetTargetCellPos(ws, 'B' + index, temp['level'])
        Work.myopenpyxl.SetTargetCellPos(ws, 'C' + index, temp['A'])
        Work.myopenpyxl.SetTargetCellPos(ws, 'D' + index, temp['B'])
        Work.myopenpyxl.SetTargetCellPos(ws, 'E' + index, temp['C'])
        Work.myopenpyxl.SetTargetCellPos(ws, 'F' + index, temp['D'])
        num = num + 1
    Work.myopenpyxl.WriteXlsx(wb, tempName)


def EmojiToJson(filePath):
    wb = Work.myopenpyxl.OpenXlsxFullName(filePath)
    ws = Work.myopenpyxl.GetTargetSheet(wb, 'Sheet')
    len = Work.myopenpyxl.GetMaxRow(ws)

    dict = {}
    splitStr = ","
    effectArray = []

    for i in range(len):
        index = i + 1
        if (index >= 2):
            emoji = str(Work.myopenpyxl.GetTargetCell(
                ws, 'A' + str(index)).value)
            effectArray.append(emoji)
            cValue = str(Work.myopenpyxl.GetTargetCell(
                ws, 'C' + str(index)).value).lower()
            arr = cValue.split(splitStr)
            for word in arr:
                if (dict.__contains__(word)):
                    dict[word].append(emoji)
                else:
                    dict[word] = [emoji]
    Work.tool_file.WriteText(json.dumps(dict), filePath + "config.txt")
    CreateEmojiEffectExcel(filePath, effectArray)
    print("OK")


def CreateEmojiEffectExcel(filePath, arr):
    tempName = filePath + "emojiEffect.xlsxconfig.xlsx"
    wb = Work.myopenpyxl.CreateNewXlsx(tempName)
    ws = Work.myopenpyxl.GetNowActiveSheet(wb)

    Work.myopenpyxl.SetTargetCellPos(ws, 'A1', "ID")
    Work.myopenpyxl.SetTargetCellPos(ws, 'B1', "特效图片名")
    Work.myopenpyxl.SetTargetCellPos(ws, 'C1', "特效入场方式")
    Work.myopenpyxl.SetTargetCellPos(ws, 'D1', "特效入场时间")
    Work.myopenpyxl.SetTargetCellPos(ws, 'E1', "特效停留时间")
    Work.myopenpyxl.SetTargetCellPos(ws, 'F1', "特效飞出时间")
    Work.myopenpyxl.SetTargetCellPos(ws, 'G1', "入场特效")
    Work.myopenpyxl.SetTargetCellPos(ws, 'H1', "停留特效")
    Work.myopenpyxl.SetTargetCellPos(ws, 'I1', "消失特效")

    num = 2
    for temp in arr:
        index = str(num)
        Work.myopenpyxl.SetTargetCellPos(ws, 'A' + index, temp)
        Work.myopenpyxl.SetTargetCellPos(ws, 'B' + index, temp)
        Work.myopenpyxl.SetTargetCellPos(ws, 'C' + index, "0")
        Work.myopenpyxl.SetTargetCellPos(ws, 'D' + index, 0)
        Work.myopenpyxl.SetTargetCellPos(ws, 'E' + index, 0)
        Work.myopenpyxl.SetTargetCellPos(ws, 'F' + index, 0)
        Work.myopenpyxl.SetTargetCellPos(ws, 'G' + index, "")
        Work.myopenpyxl.SetTargetCellPos(ws, 'H' + index, "")
        Work.myopenpyxl.SetTargetCellPos(ws, 'I' + index, "")
        num = num + 1
    Work.myopenpyxl.WriteXlsx(wb, tempName)


def EmojiEffectToJson(filePath):
    wb = Work.myopenpyxl.OpenXlsxFullName(filePath)
    ws = Work.myopenpyxl.GetTargetSheet(wb, 'Sheet')

    len = Work.myopenpyxl.GetMaxRow(ws)

    dict = {}
    for i in range(len):
        index = i + 1
        if (index > 1):
            emoji = {}

            emoji["id"] = Work.myopenpyxl.GetTargetCell(
                ws, 'A' + str(index)).value
            emoji["img"] = str(Work.myopenpyxl.GetTargetCell(
                ws, 'B' + str(index)).value)
            emoji["type"] = Work.myopenpyxl.GetTargetCell(
                ws, 'C' + str(index)).value
            emoji["inT"] = Work.myopenpyxl.GetTargetCell(
                ws, 'D' + str(index)).value
            emoji["wT"] = Work.myopenpyxl.GetTargetCell(
                ws, 'E' + str(index)).value
            emoji["outT"] = Work.myopenpyxl.GetTargetCell(
                ws, 'F' + str(index)).value
            GValue = Work.myopenpyxl.GetTargetCell(ws, 'G' + str(index)).value
            if (GValue == None):
                GValue = ""
            emoji["inE"] = str(GValue)
            HValue = Work.myopenpyxl.GetTargetCell(ws, 'H' + str(index)).value
            if (HValue == None):
                HValue = ""
            emoji["wE"] = str(HValue)
            IValue = Work.myopenpyxl.GetTargetCell(ws, 'I' + str(index)).value
            if (IValue == None):
                IValue = ""
            emoji["outE"] = str(IValue)

            dict[emoji["id"]] = emoji

    Work.tool_file.WriteText(json.dumps(dict), filePath + "config.txt")
    print("OK")


def GtaIapSql(filePath, targetPath):
    wb = Work.myopenpyxl.OpenXlsxFullName(filePath)
    ws = Work.myopenpyxl.GetTargetSheet(wb, 'Sheet')
    len = Work.myopenpyxl.GetMaxRow(ws)

    fo = open(targetPath, "a+")

    allSql = ""
    dict = {}
    for i in range(len):
        index = i+1
        if (index >= 1):
            pos = "A{0}:BD{1}".format(str(index), str(index))
            list = Work.myopenpyxl.GetTargetCells(ws, pos)[0]
            strInfo = ""
            jIndex = 1
            for tempCurpe in list:
                strInfo = strInfo + \
                    GetStr(Work.myopenpyxl.GetTargetCellPos(
                        ws, index, jIndex).value)+","
                jIndex = jIndex+1
            sql = GetSql(strInfo+'\n')
            fo.write(sql)

    fo.close()
    print("OK")


def GetStr(info):
    if (info == None):
        info = ""
    strInfo = '\''
    strInfo = strInfo+str(info)
    strInfo = strInfo + '\''
    return strInfo


def GetSql(info):
    strInfo = "INSERT INTO"
    strInfo = strInfo+" [dbo].[raw_event_1_129_1-000000000002]([id],[sign],[aid],[did],[did2],[uuid],[fid],[target],[is_tester],[dt],[install_dt],[server_dt],[client_dt],[country],[countryx],[adjust_source],[ver],[gta_ver],[install_ver],[timezone],[event_sn],[ip],[max_level],[cur_level],[play_seconds],[open_count],[event_name],[iap_count],[device_class],[device_model],[from_adp],[from_camp],[from_app],[from_creative],[user_group],[v1],[v2],[v3],[v4],[v5],[v6],[v7],[v8],[vt],[created_at],[updated_at],[event_id],[v9],[v10],[v11],[v12],[ref],[property],[level_diff],[attribute],[playday]) VALUES("
    strInfo = strInfo + info
    strInfo = strInfo + ")"
    return strInfo


class EmojiEffectData:
    # id
    id = -1
    # 图片名
    image = ""
    # 特效入场方式
    enterType = 0
    # 特效入场动画时间
    enterTime = 0
    # 特效停留时间
    waitTime = 0
    # 特效飞出时间
    outTime = 0
    # 进入特效
    enterEffect = ""
    # 停留特效
    waitEffect = ""
    # 消失特效
    outEffect = ""
