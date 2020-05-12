#!use/bin/env python3
# -*- coding utf-8 -*-

import re
import Work.tool_file as toolfile


def TestNumber(info):
    number = []
    targetNumber = re.compile(
        r'><figure aria-label=".*?" id="')
    tupleNumber = re.findall(targetNumber, info)
    for index in range(len(tupleNumber)):
        data = tupleNumber[index]
        if data != None:
            tempValue = str(data)
            tempValue = tempValue.replace('><figure aria-label="', '')
            tempValue = tempValue.replace('" id="', '')
            number.append(tempValue)
    print(number)
    return number


def TestDate(info):
    targetDate = re.compile(
        r'class="we-customer-review__date">.*?</time>')
    tupleDate = re.findall(targetDate, info)
    date = []
    for index in range(len(tupleDate)):
        data = tupleDate[index]
        if data != None:
            tempValue = str(data)
            tempValue = tempValue.replace(
                'class="we-customer-review__date">', '')
            tempValue = tempValue.replace('</time>', '')
            date.append(tempValue)
    print(date)
    return date


def TestTitle(info):
    targetTitle = re.compile(
        r'ember-view we-customer-review__title">.*?</h3>', re.S)
    tupleTitle = re.findall(targetTitle, info)
    title = []
    for index in range(len(tupleTitle)):
        data = tupleTitle[index]
        if data != None:
            tempValue = str(data)
            tempValue = tempValue.replace(
                'ember-view we-customer-review__title">', '')
            tempValue = tempValue.replace('</h3>', '')
            tempValue.replace('\n', '')
            title.append(tempValue)
    print(title)
    return title


def TestInfo(info):
    targetInfo = re.compile(
        r'<p dir="ltr" data-test-bidi="">.*?</p>')
    tupleInfo = re.findall(targetInfo, info)
    info = []
    for index in range(len(tupleInfo)):
        data = tupleInfo[index]
        if data != None:
            tempValue = str(data)
            tempValue = tempValue.replace(
                '<p dir="ltr" data-test-bidi="">', '')
            tempValue = tempValue.replace('</p>', '')
            tempValue.replace('\n', '')
            info.append(tempValue)
    print(info)
    return info


def InputFile():
    path = input("input path\n\n")
    fo = open(path, encoding='gbk', errors='ignore')
    info = fo.read()
    fo.close()
    stringValue = ""
    number = TestNumber(info)
    date = TestDate(info)
    title = TestTitle(info)
    info = TestInfo(info)
    for index in range(len(number)):
        stringValue += str(number[index])
        stringValue += "\n"
        stringValue += str(date[index])
        stringValue += "\n"
        stringValue += str(title[index])
        stringValue += "\n"
        stringValue += str(info[index])
        stringValue += "\n\n\n"

    fo = open("D://log.txt", "w+", errors='ignore')
    fo.write(stringValue)
    fo.close()
    #toolfile.WriteText(stringValue, "D://log.txt")
    print("ok")


InputFile()
