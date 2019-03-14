#!use/bin/env python3
#-*- coding utf-8 -*-

list = range(10)
dic = {0:'p',1:'q',2:'w',3:'e'}
for i,value in enumerate(list):
	print(i,value)
for x,y in dic.items():
	print(x,y)
	
print(dic[3])