#!use/bin/env python
# -*- coding utf-8 -*-

# pip3 install pillow
# pip3 install numpy

import os
import numpy
from PIL import Image, ImageDraw

path = os.path.split(os.path.realpath(__file__))[0]


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


def ImageAlphaOutLine(imagePath, round, targetColor):  # 图片增加 指定长度  指定颜色 描边
    img = Image.open(imagePath)
    size = img.size
    width = size[0]+round*2
    height = size[1]+round*2
    image = Image.new('RGBA', (width, height))
    for x in range(width):
        for y in range(height):
            if x < round or x > size[0]+round-1 or y < round or y > size[1]+round-1:
                image.putpixel((x, y), targetColor)
            else:
                image.putpixel((x, y), img.getpixel((x-round, y-round)))
    image.save(imagePath)


def main():
    print("\n\n-------------Finish-------------\n\n")


if __name__ == '__main__':
    main()
