#!use/bin/env python
# -*- coding utf-8 -*-

import CenterController
import time

oneDayTime = 1


def main():
    while(True):
        try:
            CenterController.TrySomething()
        except Exception as e:
            print(str(e))
        time.sleep(oneDayTime)


if __name__ == '__main__':
    main()
