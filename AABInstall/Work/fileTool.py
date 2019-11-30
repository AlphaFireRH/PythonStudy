#!use/bin/env python3
# -*- coding utf-8 -*-

import os
import shutil
import stat

path = os.path.split(os.path.realpath(__file__))[0]
# 工具路径
toolPath = path + "/tool/"
buildToolPath = toolPath + "BuildTool/"
bundletoolPath = toolPath + "bundletool.jar"
adbPath = toolPath + "adb.exe"
aaptPath = buildToolPath + "aapt.exe"

ksPath = toolPath + "store.keystore"
ks_Alias = "wordsearchpop"
ks_pass = "johnstorepass"

spaceStr = " "


# 输出APKS文件
def OutputAPKS(aabPath, apksPath):
    DeleteFile(apksPath)
    cmdInfo = "java -jar" + spaceStr + bundletoolPath + spaceStr
    cmdInfo += "build-apks" + spaceStr
    cmdInfo += "--bundle=" + aabPath + spaceStr
    cmdInfo += "--output=" + apksPath + spaceStr
    cmdInfo += "--ks=" + ksPath + spaceStr
    cmdInfo += "--ks-pass=pass:" + ks_pass + spaceStr
    cmdInfo += "--ks-key-alias=" + ks_Alias + spaceStr
    cmdInfo += "--key-pass=pass:" + ks_pass + spaceStr
    os.system(cmdInfo)
    os.system('exit')


# 安装apks
def Install(apksPath):
    cmdInfo = "java -jar " + bundletoolPath + spaceStr
    cmdInfo += "install-apks" + spaceStr
    cmdInfo += "--apks=" + apksPath + spaceStr
    cmdInfo += "--adb=" + adbPath + spaceStr
    os.system(cmdInfo)
    os.system('exit')


# 生成针对设备的json信息
def OutputJSON(jsonFilePath):
    DeleteFile(jsonFilePath)
    cmdInfo = "java -jar " + bundletoolPath + spaceStr
    cmdInfo += "get-device-spec" + spaceStr
    cmdInfo += "--output=" + jsonFilePath + spaceStr
    cmdInfo += "--adb=" + adbPath + spaceStr
    os.system(cmdInfo)
    os.system('exit')


# 根据json拆分apks
def SpliteAPKS(apksPath, jsonFilePath, splitePath):
    cmdInfo = "java -jar " + bundletoolPath + spaceStr
    cmdInfo += "extract-apks" + spaceStr
    cmdInfo += "--apks=" + apksPath + spaceStr
    cmdInfo += "--output-dir=" + splitePath + spaceStr
    cmdInfo += "--device-spec=" + jsonFilePath + spaceStr
    os.system(cmdInfo)
    os.system('exit')


# 删除文件
def DeleteFile(path):
    if (os.path.exists(path)):
        os.remove(path)


# 清理目录
def ClearDir(targetDir):
    isExists = os.path.exists(targetDir)
    if isExists:
        shutil.rmtree(targetDir)

    isExists = os.path.exists(targetDir)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(targetDir)
        print(targetDir + ' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(targetDir + ' 目录已存在')
    os.chmod(targetDir, stat.S_IWRITE)


# 普通安装
def NormalInstall(targetDir):
    cmdInfo = adbPath + spaceStr + "install -r " + targetDir
    os.system(cmdInfo)
    os.system('exit')


# 展示所有log
def ShowAllLog():
    os.system("chcp 65001")
    cmdInfo = adbPath + spaceStr + "logcat -s Unity "
    os.system(cmdInfo)
    os.system('exit')


# 展示错误log
def ShowErrorLog():
    os.system("chcp 65001")
    cmdInfo = adbPath + spaceStr + "logcat -s Unity:e"
    os.system(cmdInfo)
    os.system('exit')
	
# 展示错误log
def CleanLog():
    os.system("chcp 65001")
    cmdInfo = adbPath + spaceStr + "logcat -c"
    os.system(cmdInfo)
    os.system('exit')


# 查看安装包信息
def ShowApkInfoFromAAPT(apkPath):
    cmdInfo = aaptPath + spaceStr + "dump badging" + spaceStr + apkPath
    os.system(cmdInfo)
    os.system('exit')


# 查看安装之后的信息
def ShowInstalledInfoFromAAPT(apkPath):
    cmdInfo = adbPath + spaceStr + "shell dumpsys package" + spaceStr + apkPath
    os.system(cmdInfo)
    os.system('exit')
