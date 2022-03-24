#!/usr/bin/env python3

import sys
import neopixel
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
ORDER = neopixel.GRBW

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
    str = str.replace('\n', '')
    values = []
    for c in str:
        r = 100 if c == '#' else 0
        g = 0
        b = 0
        w = 0
        values.append((r, g, b, w))

    return values

def main():
    global led_matrix
    led_matrix = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.1, auto_write=False, pixel_order=ORDER)

    opts, args = getopt.getopt(sys.argv[1:], "", ["reset", "test", "bitmap="])
    values = []

    for opt, arg in opts:
        if (opt == "--reset"):
            values = bitmap()
        elif (opt == "--test"):
            values = ascii(space_invader)
        elif (opt == "--bitmap"):
            values = bitmap(arg)

    for y in range(0, 11):
        for x in range(0, 11):
            i = y * 11 + x

            if i <= len(values) - 1:
                r, g, b, w = values[i]
                led_matrix[i] = (r, g, b, w)
            else:
                led_matrix[i] = (0, 0, 0, 0)

    led_matrix.show()

if __name__ == '__main__':
    main()
