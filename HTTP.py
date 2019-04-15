#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib3

http = urllib3.PoolManager()
r=http.request('GET','https://www.baidu.com')
print(r.status)
print(r.data.decode())


