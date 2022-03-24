#!/usr/bin/env python3

import time

from matrix import *

def main():
    values = bitmap.ascii(art.avatar, "FC0E8100")
    display.update(values)
    time.sleep(3)
    display.update()

if __name__ == '__main__':
    main()
