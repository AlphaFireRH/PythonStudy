#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import json

class testClass(object):
    name=''

print(os.name)
print(os.environ)
print(os.path.join('/Users/michael/testdir/','file.txt'))
print(os.path.split('/Users/michael/testdir/file.txt'))
print(os.path.splitext('/Users/michael/testdir/file.txt'))
print(os.path.splitdrive('/Users/michael/testdir/file.txt'))
print(os.path.splitunc('/Users/michael/testdir/file.txt'))

d = dict(name='Bob', age=20, score=88)
print(json.dumps(d))


def testClass2dict(std):
    return {
        'name': std.name,
    }
test=testClass()
test.name='123'
info = json.dumps(test,default=testClass2dict)
print(info)
info = json.dumps(test,default=lambda obj: obj.__dict__)
print(info)