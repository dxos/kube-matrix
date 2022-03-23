#!/usr/bin/env python3

import math
import time
import neopixel
import board

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

    for y in range(0, 11):
        for x in range(0, 11):
            led_matrix[y * 11 + x] = (int(0), int(0), int(0), int(0))

    led_matrix.show()

if __name__ == '__main__':
    main()
