#!/usr/bin/env python3

import sys
import math
import time
import neopixel
import board
from random import random

UPDATE_PERIOD = 0.1
RESET_THRESHOLD = 5
TIME_BETWEEN_RESETS = 5 * 60
TIME_UNTIL_EXIT = 5

LED_COUNT      = 121            # Number of LED pixels.
LED_PIN        = board.D18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000         # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5              # DMA channel to use for generating signal (try 5)
LED_INVERT     = False          # True to invert the signal (when using NPN transistor level shift)

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW


def neighbors_alive(cells, x, y):
    def c2n(c):
        return 1 if c else 0

    def get(x, y):
        x = x % 11
        y = y % 11
        return c2n(cells[y][x])

    return sum([
        get(x - 1, y - 1),
        get(x - 1, y + 1),
        get(x + 1, y - 1),
        get(x + 1, y + 1),
        get(x - 1, y),
        get(x + 1, y),
        get(x, y - 1),
        get(x, y + 1),
    ])


def conway_update(cells):
    change_count = 0
    new_cells = [[False] * 11 for i in range(11)]

    for y in range(0, 11):
        for x in range(0, 11):
            nn = neighbors_alive(cells, x, y)
            
            if cells[y][x]:
                new_cells[y][x] = nn == 2 or nn == 3
            else:
                new_cells[y][x] = nn == 3

            if new_cells[y][x] != cells[y][x]:
                change_count += 1

    return new_cells, change_count


def randomize_cells():
    cells = [[False] * 11 for i in range(11)]

    # Randomize cells at start
    for y in range(0, 11):
        for x in range(0, 11):
            cells[y][x] = random() >= 0.7 

    return cells


def main():
    led_matrix = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.1, auto_write=False, pixel_order=ORDER)

    """
    # Glider
    cells[0][2] = True
    cells[1][0] = True
    cells[1][2] = True
    cells[2][1] = True
    cells[2][2] = True
    """

    cells = randomize_cells()

    # Time
    t = 0
    time_since_reset = 0

    while True:
        for y in range(0, 11):
            for x in range(0, 11):
                v = 255 if cells[y][x] else 0

                r = v
                g = v
                b = v
                w = 0

                led_matrix[y * 11 + x] = (int(r), int(g), int(b), int(w))

        led_matrix.show()

        cells, change_count = conway_update(cells)

        if change_count < RESET_THRESHOLD and time_since_reset < TIME_BETWEEN_RESETS - 10:
            time_since_reset = TIME_BETWEEN_RESETS - 10

        if time_since_reset > TIME_BETWEEN_RESETS:
            cells = randomize_cells()
            time_since_reset = 0

        if t > TIME_UNTIL_EXIT:
            for y in range(0, 11):
                for x in range(0, 11):
                    led_matrix[y * 11 + x] = (int(0), int(0), int(0), int(0))
            led_matrix.show()
            sys.exit()

        time.sleep(UPDATE_PERIOD)
        t += UPDATE_PERIOD
        time_since_reset += UPDATE_PERIOD


if __name__ == '__main__':
    main()

