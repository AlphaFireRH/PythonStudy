#!use/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from alive_progress import alive_bar

# pip install alive-progress


def Test(numbers):
    items = range(numbers)                  # retrieve your set of items
    with alive_bar(len(items)) as bar:   # declare your expected total
        for item in items:               # iterate as usual
            # process each item
            bar()
            time.sleep(0.1)


def main():
    Test(1000)                       # call after consuming one item
    print("\n\n-------------Finish-------------\n\n")
    os.system("pause")


if __name__ == '__main__':
    main()
