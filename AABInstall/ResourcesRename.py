#!use/bin/env python
# -*- coding utf-8 -*-

import os
# import Work.ExcelSet
import Work.tool_file as fileTool
import Work.myopenpyxl as myopenpyxl
from PIL import Image
# import json
# import stat
# import codecs
import datetime
import numpy
# import Work.tool_jsonString as jsonToString

# pip3 install pillow
# pip3 install numpy
# sudo easy_install PIL
# pip install openpyxl

path = os.path.split(os.path.realpath(__file__))[0]
sorcesPath = path + "/sketch/"
destinationPath = path + "/unity/"
gameVersion = "1.0.0"
excelFilePath = path+"/resourcemap.xlsx"


def Init():  # 路径初始化
    fileTool.DeleteDir(destinationPath)
    fileTool.CreateDir(destinationPath)


def ReadConfig():  # 读取配置文件

    wb = myopenpyxl.OpenXlsxFullName(excelFilePath)
    ws = myopenpyxl.GetTargetSheet(wb, 'resourcemap')

    len = myopenpyxl.GetMaxRow(ws)

    for i in range(len+1):
        if i == 0:
            continue
        artPath = str(myopenpyxl.GetTargetCell(ws,
                                               'B' + str(i)).value)
        imagePath = sorcesPath + artPath
        if(fileTool.FileExists(imagePath)):
            md5 = fileTool.GetMD5(imagePath)
            oldMd5 = str(myopenpyxl.GetTargetCell(ws,
                                                  'I' + str(i)).value)
            if(md5 == oldMd5):
                continue
            else:
                img = Image.open(imagePath)
                size = img.size
                myopenpyxl.SetTargetCellPos(ws, 'D' + str(i), size[0])
                myopenpyxl.SetTargetCellPos(ws, 'E' + str(i), size[1])
                myopenpyxl.SetTargetCellPos(
                    ws, 'F' + str(i), fileTool.GetFileSize(imagePath))
                myopenpyxl.SetTargetCellPos(ws, 'G' + str(i), gameVersion)
                myopenpyxl.SetTargetCellPos(
                    ws, 'H' + str(i), datetime.datetime.now())
                myopenpyxl.SetTargetCellPos(ws, 'I' + str(i), md5)
                CleanImage(imagePath, destinationPath+myopenpyxl.GetTargetCell(ws,
                                                                               'A' + str(i)).value)

    myopenpyxl.WriteXlsxFullName(wb, excelFilePath)


def CleanImage(srcfile, dstfile):  # 清理图片 将透明度小于5的 清理掉
    fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
    if not os.path.exists(fpath):
        os.makedirs(fpath)  # 创建路径
    im1 = Image.open(srcfile)
    np_im = numpy.array(im1)
    np_im = np_im.copy()
    for row in np_im:
        for pixel in row:
            if pixel[3] <= 5:
                pixel[3] = 0
    new_im = Image.fromarray(np_im)
    new_im.save(dstfile)


def main():
    global gameVersion
    gameVersion = input("\nPlease input game next version.\n\n")
    print("\nClean Dir...\n\n")
    Init()
    print("\nRead and Update Config...\n\n")
    ReadConfig()

    print("\n\n-------------Finish-------------\n\n")


if __name__ == '__main__':
    main()
