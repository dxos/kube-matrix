#!/usr/bin/env python3

import sys
import getopt
import re

# bitmap is string that contains 121 (11x11) comma delimitered strings of the form 'RRGGBBWW'
def bitmap(bitmap = ''):
    values = []
    if bitmap:
        values = bitmap.split(',')

    matrix = []
    for y in range(0, 11):
        for x in range(0, 11):
            i = y * 11 + x
            if (i <= len(values) - 1):
                # https://docs.python.org/2/library/re.html#match-objects
                match = re.search(r'^([\da-f]{2})([\da-f]{2})([\da-f]{2})([\da-f]{2})$', values[i]);
                if match:
                    r = match.group(1)
                    g = match.group(2)
                    b = match.group(3)
                    w = match.group(4)
                    matrix.append([int('0x'+r, 0), int('0x'+g, 0), int('0x'+b, 0), int('0x'+w, 0)])
                    continue

            matrix.append([int(0), int(0), int(0), int(0)])

    return matrix
