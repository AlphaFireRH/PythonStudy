#!use/bin/env python
# -*- coding utf-8 -*-

from PIL import Image, ImageFilter


# input
def PleaseInputPath():
    info = 'please input Image path: \n'
    return info


# get input
def GetInput():
    return input(PleaseInputPath())

# 改变图像尺寸
def ResizeImage(wValue,hValue):
    path=GetInput()
    im=Image.open(path)

    w, h = im.size
    # 缩放
    im.thumbnail((w*wValue, h*hValue))

    # 把缩放后的图像用jpeg格式保存:
    im.save(path+'resize.jpg', 'jpeg')

# 图片增加滤镜
def FilterForImage(imageFilter):
    path=GetInput()
    im=Image.open(path)
    print('123')
    # 应用模糊滤镜:
    im = im.filter(imageFilter)

    # 把缩放后的图像用jpeg格式保存:
    im.save(path[0:-4]+'Filter.jpg', 'jpeg')





def main():
    #ResizeImage(3,3)
    FilterForImage(ImageFilter.BLUR)
    

if __name__ == '__main__':
    main()
