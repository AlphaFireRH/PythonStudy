#!use/bin/env python
# -*- coding utf-8 -*-

# 库
# pip install ffmpy3
# pip install opencv-python

import Work.ffmpeg.video as ffVideo
import os
import shutil
# import cv2
# import numpy as np
# from PIL import ImageGrab
# from threading import Thread
# import time

reCodeing = False


def PleaseInputPath():  # input
    info = 'please input package path: \n'
    return info


def GetInput():  # get input
    return input(PleaseInputPath())


def f4():
    vp = CutSplicingVdeio()  # class instance

    filePath = r"E:\my.avi"
    videoStartTime = "00:00:0.0"
    videoEndTime = "00:00:8.0"
    # videoSaveDir1=r"‪E:\animation\Wisp_03.mov"
    videoPath = r"‪E:\liucheng\emo\01.mp4"
    # filePath=r"C:\Users\Administrator\Desktop\_HUDSence24.mov"
    imageSaveDir = r"\E:\liucheng\emo"
    fileName1 = r"D:\wu.jpg"
    # print vp.instructions()#return class dercription

    # 分割视频
    # vp.cutOutVideo(ffmpegPath,filePath,videoStartTime,videoEndTime,videoSaveDir)#according to video give a StartTime and  give a EndTime segmentation video;

    # 得到视频、图片信息
    # print vp.getVideoData(CurMediaPath)#return video dercription
    # print vp.getVideoData(filePath)#return video data

    # 视频导出序列帧
    # vp.videoTransImage(videoPath,imageSaveDir)#according to give a video frames decomposition image

    # 序列帧导出视频
    # vp.ImageTransVideo(imagePath,videoSaveDir)#according to give a Sequence frames composition video

    # 截取视频某一帧作为缩略图
    # vp.cutVideoImage_resolution(videoPath,fileName,resolution)#according to give a resolution Screenshot(first key)
    # vp.cutVideoImage_reAndTime(videoPath,fileName1,"520x520",12)#according to give a resolution and time Screenshot(give time key)

    # 一段视频 转换成Gif
    # vp.videoKeyRange_Gif(videoPath,fileName,keytime)#according to give a time composition front keytime key gif

    # 图片格式转换
    # vp.imageFormatTrans("D:/1.jpg","C:/Users/Administrator/Desktop/root/text.png")#according to give a image format transform

    # 视频格式转换
    # vp.videoFormatTrans(r"E:\my.avi",r"E:\001.avi")#according to give a video format transform

    # 录屏
    # vp.transcribeScreen(r"C:\Users\Administrator\Desktop\transcribe.avi")#according to give a video filepath (transcribe Screen)

    # 实现屏幕录制
    # vp.broadcastVideo(videoSaveDir)##according to give a video filepath broadcast Video

    # 实现调用笔记本摄像头进行监控
    # vp.cameraAddVideo(filePath)##according to give a video filepath laptop camera shooting video

    # 音频格式转换
    # vp.audioTransFormat(filepath,filesavepath)##according to give  video filepath and filesavepath format transform

    # 视频格式转换
    # vp.videoFormatTrans(filePath,r"E:\Wisp_03_3.mov")

    # vp.cutVideoImage_reAndTime(filePath,r"C:\Users\Administrator\Desktop\temp\4.png","512x512",2)

    # 视频添加水印
    # vp.videoAddWatermask(r"‪E:\liucheng\emo\01.mp4",r"‪‪E:\liucheng\emo\tree.png",r"‪E:\liucheng\emo\01_1.mp4")


def GetImageForKey(videoPath):
    dirPath = os.path.dirname(videoPath) + "\\Images\\"
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    else:
        allFile = os.listdir(dirPath)
        for fileName in allFile:
            os.remove(dirPath+fileName)
    fileName = dirPath+"Image"
    state = ffVideo.video_trans_img(videoPath, fileName, "1")
    print(state)
    # ffmpeg - i inputfile.avi - r 1 - s 4cif - f image2 image-%05d.jpeg
    # 截取视频某一帧作为缩略图
    # according to give a resolution Screenshot(first key)
    # vp.cutVideoImage_resolution(videoPath, fileName, videoData.resolution)
    # vp.cutVideoImage_reAndTime(videoPath,fileName1,"520x520",12)#according to give a resolution and time Screenshot(give time key)


if __name__ == '__main__':
    # GetImageForKey("d:\\Images\item.mp4")  # GetInput()
    GetImageForKey(GetInput())
