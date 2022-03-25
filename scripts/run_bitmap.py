#!/usr/bin/env python3

import sys
import getopt

from matrix import *

data = {
    'avatar': bitmap.ascii(art.avatar, ['FC0E8100']),
    'skull': bitmap.ascii(art.skull, ['0000FF00']),
    'hal': bitmap.ascii(art.hal, ['55555555', '22000000', 'FF000000'])
}

def main():
    opts, args = getopt.getopt(sys.argv[1:], '', ['reset', 'preset=', 'bitmap='])

    values = []
    for opt, arg in opts:
        if (opt == '--reset'):
            values = bitmap.hex()
        elif (opt == '--preset'):
            try:
                values = data[arg]
            except:
                values = data['avatar']
        elif (opt == '--bitmap'):
            values = bitmap.hex(arg)

    display.update(values)

if __name__ == '__main__':
    main()
