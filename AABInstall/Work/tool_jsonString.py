#!use/bin/env python3
# -*- coding utf-8 -*-


def StringToJsonArrayString(info):
    splitStr = ","
    arr = info.split(splitStr)
    tempStr = "["
    for word in arr:
        tempStr += word + ","
    tempStr = tempStr[:-1]
    tempStr += "]"

    return tempStr


def encode(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])


def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])
