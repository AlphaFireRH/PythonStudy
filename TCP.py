#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
address=("www.sina.com.cn",80)
s.connect(address)

s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

buffer=[]
while True:
	d = s.recv(1024)
	if d:
		buffer.append(d)
	else:
		break
data=b''.join(buffer)
s.close()

header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))

