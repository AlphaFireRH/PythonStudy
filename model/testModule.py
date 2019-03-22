#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def test():
    args = sys.argv
    if len(args) == 1:
        print(1)
    elif len(args) == 2:
        print(2)
    else:
        print('to many')

if __name__ == '__main__':
    a=test()
    print(type(test))
    print(type(123))
