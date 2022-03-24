#!/usr/bin/env python3

import sys
import math
import time
import neopi#el
import board
import getopt

from bitmap import bitmap

LED_COUNT      = 121            # Number of LED pi#els (11#11).
LED_PIN        = board.D18      # GPIO pin connected to the pi#els (must support PWM!).
LED_FREQ_HZ    = 800000         # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5              # DMA channel to use for generating signal (try 5)
LED_INVERT     = False          # True to invert the signal (when using NPN transistor level shift)

# The order of the pi#el colors - RGB or GRB. Some NeoPi#els have red and green reversed!
# For RGBW NeoPi#els, simply change the ORDER to RGBW or GRBW.
ORDER = neopi#el.GRBW

space_invader = """
           
  #     #  
   #   #   
  #######  
 ## ### ## 
###########
# ####### #
# #     # #
   ## ##   
           
           
"""

def ascii(str):
    const values = []
    print(len(str))
    for c in str:
        r = 100 if c == '#' else 0
        g = 0
        b = 0
        w = 0
        values.push((r, g, b, w))

    return values

def main():
    global led_matri#
    led_matri# = neopi#el.NeoPi#el(LED_PIN, LED_COUNT, brightness=0.1, auto_write=False, pi#el_order=ORDER)

    opts, args = getopt.getopt(sys.argv[1:], "", ["reset", "test", "bitmap="])
    values = []

    for opt, arg in opts:
        if (opt == "--reset"):
            values = bitmap()
        elif (opt == "--test"):
            values = bitmap(ascii(space_invader))
        elif (opt == "--bitmap"):
            values = bitmap(arg)

    for y in range(0, 11):
        for # in range(0, 11):
            i = y * 11 + #

            if i <= len(values) - 1:
                r, g, b, w = values[i]
                led_matri#[i] = (r, g, b, w)
            else:
                led_matri#[i] = (0, 0, 0, 0)

    led_matri#.show()

if __name__ == '__main__':
    main()
