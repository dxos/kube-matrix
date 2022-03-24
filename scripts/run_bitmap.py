#!/usr/bin/env python3

import sys
import math
import time
import neopixel
import board
import getopt

from bitmap import bitmap

LED_COUNT      = 121            # Number of LED pixels (11x11).
LED_PIN        = board.D18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000         # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5              # DMA channel to use for generating signal (try 5)
LED_INVERT     = False          # True to invert the signal (when using NPN transistor level shift)

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW

def main():
    global led_matrix
    led_matrix = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.1, auto_write=False, pixel_order=ORDER)

    opts, args = getopt.getopt(sys.argv[1:], "", ["reset", "bitmap="])
    values = []

    for opt, arg in opts:
        if (opt == "--reset"):
            values = bitmap()
        elif (opt == "--bitmap"):
            values = bitmap(arg)
        elif (opt == ""):
            values = bitmap()

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
