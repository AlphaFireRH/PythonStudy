#!use/bin/env python3
#-*- coding utf-8 -*-

def trim(str):
	if len(str)==0:
		return str

	if str[0:1]==' ':
		str=trim(str[1:])
	if str[0:-1]==' ':
		str=trim(str[-1:])
		
	return str
	
	
s=input()
s=trim(s);
print(s);