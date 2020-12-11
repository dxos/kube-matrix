#!/usr/bin/env python3

import math
import time
import neopixel
import board

LED_COUNT      = 121            # Number of LED pixels.
LED_PIN        = board.D18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000         # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5              # DMA channel to use for generating signal (try 5)
LED_INVERT     = False          # True to invert the signal (when using NPN transistor level shift)

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW

ANIM_DURATION = 0.5
ANIM_FRAME_DURATION = 0.03

def main():
    led_matrix = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.1, auto_write=False, pixel_order=ORDER)

    # Time
    t = 0

    while t < ANIM_DURATION:
        for y in range(0, 11):
            for x in range(0, 11):
                if t < ANIM_DURATION / 2.0:
                    st = t / ANIM_DURATION * 2
                else:
                    st = (ANIM_DURATION - t) / ANIM_DURATION * 2

                v = st * 255

                r = v
                g = v
                b = v

                w = 0

                led_matrix[y * 11 + x] = (int(r), int(g), int(b), int(w))

        led_matrix.show()

        time.sleep(ANIM_FRAME_DURATION)
        t += ANIM_FRAME_DURATION

    for i in range(0, 11 * 11):
        led_matrix[i] = (0, 0, 0, 0)
    led_matrix.show()

if __name__ == '__main__':
    main()
