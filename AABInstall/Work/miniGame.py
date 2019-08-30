#!use/bin/env python
# -*- coding utf-8 -*-

import Work.myopenpyxl
import json
import stat
import codecs
import Work.tool_jsonString
import Work.tool_file


def LevelDataToJson(filePath):
	wb = Work.myopenpyxl.OpenXlsxFullName(filePath)
	ws = Work.myopenpyxl.GetTargetSheet(wb, 'Sheet1')
	len = Work.myopenpyxl.GetMaxRow(ws)
	
	packageDict={}
	for i in range(len):
		index = i+1
		if index > 3:
			pos="B{0}:L{1}".format(str(index),str(index))
			list=Work.myopenpyxl.GetTargetCells(ws,pos)[0]
			
			levelTargetData = {}
			levelTargetData['levelId']=GetIntValue(list[4])
			levelTargetData['targetId']=GetIntValue(list[6])
			
			packageId=GetIntValue(list[0])
			packageName=GetStringValue(list[1])
			chapterId=GetIntValue(list[2])
			passInfo=GetStringValue(list[3])
			reward=GetIntValue(list[5])
			cost=GetIntValue(list[7])
			costStep=GetIntValue(list[8])
			video=GetIntValue(list[9])
			videoStep=GetIntValue(list[10])
			
			ownChapter = False
			if packageId in packageDict.keys():
				packageTargetData=packageDict[packageId]
				chapterTargetData={}
				ownChapter = False
				for j in packageTargetData['chapterData']:
					if j['chapterId'] == chapterId:
						chapterTargetData = j
						ownChapter = True
						break
				
				if ownChapter:
					chapterTargetData['levelData'].append(levelTargetData)
				else:
					chapterTargetData['chapterId']=chapterId
					chapterTargetData['reward']=reward
					chapterTargetData['pass']=passInfo
					chapterTargetData['levelData']=[]
					chapterTargetData['levelData'].append(levelTargetData)
					
					packageTargetData['chapterData'].append(chapterTargetData)
			else:
				packageTargetData={}
				chapterTargetData={}
				
				packageDict[packageId]=packageTargetData
				
				packageTargetData['packageId']=packageId
				packageTargetData['packageName']=packageName
				packageTargetData['cost']=cost
				packageTargetData['costStep']=costStep
				packageTargetData['video']=video
				packageTargetData['videoStep']=videoStep
				packageTargetData['chapterData']=[]
				
				chapterTargetData['chapterId']=chapterId
				chapterTargetData['reward']=reward
				chapterTargetData['pass']=passInfo
				chapterTargetData['levelData']=[]
				chapterTargetData['levelData'].append(levelTargetData)
				
				packageTargetData['chapterData'].append(chapterTargetData)
			
	Work.tool_file.WriteText(json.dumps(packageDict), filePath + "config.txt")
	print("OK")
	
	
	
def WordDataToJson(filePath):
	wb = Work.myopenpyxl.OpenXlsxFullName(filePath)
	ws = Work.myopenpyxl.GetTargetSheet(wb, 'Sheet1')
	len = Work.myopenpyxl.GetMaxRow(ws)
	
	tempArr=[]
	for i in range(len):
		index = i+1
		if (index > 3):
			pos="B{0}:F{1}".format(str(index),str(index))
			list=Work.myopenpyxl.GetTargetCells(ws,pos)[0]
			dictData = {}
			dictData['id']=list[0].value
			dictData['answer']=str(list[1].value)
			dictData['image']=str(list[2].value)
			dictData['letters']=str(list[3].value)
			dictData['group']=list[4].value
			tempArr.append(dictData)
	Work.tool_file.WriteText(json.dumps(tempArr), filePath + "config.txt")
	print("OK")
	
def GetIntValue(obj):
	return obj.value
	
def GetStringValue(obj):
	return str(obj.value)