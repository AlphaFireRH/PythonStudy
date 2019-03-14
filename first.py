#!use/bin/env python3
#-*- coding utf-8 -*-

str_list = ['a', 'a', 'b', 'a', 'b', 'c']
dic = {}
for temp in str_list:
	if(temp in dic):
		dic[temp]+=1
	else:
		dic[temp]=1
print(dic)