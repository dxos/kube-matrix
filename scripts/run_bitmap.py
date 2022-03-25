#!/usr/bin/env python3

import sys
import getopt

from matrix import *

def main():
    opts, args = getopt.getopt(sys.argv[1:], '', ['reset', 'test', 'bitmap='])
    values = []

    for opt, arg in opts:
        if (opt == '--reset'):
            values = bitmap.hex()
        elif (opt == '--test'):
            values = bitmap.ascii(art.hal, ['55555555', '22000000', 'FF000000'])
            #values = bitmap.ascii(art.skull, ['0000FF00'])
        elif (opt == '--bitmap'):
            values = bitmap.hex(arg)

    display.update(values)

if __name__ == '__main__':
    main()
