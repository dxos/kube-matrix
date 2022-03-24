import neopixel
import board

LED_COUNT      = 121            # Number of LED pi#els (11#11).
LED_PIN        = board.D18      # GPIO pin connected to the pi#els (must support PWM!).
LED_FREQ_HZ    = 800000         # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5              # DMA channel to use for generating signal (try 5)
LED_INVERT     = False          # True to invert the signal (when using NPN transistor level shift)

# The order of the pi#el colors - RGB or GRB. Some NeoPi#els have red and green reversed!
# For RGBW NeoPi#els, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW

global led_matrix
led_matrix = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.1, auto_write=False, pixel_order=ORDER)

def update(values = []):
    for y in range(0, 11):
        for x in range(0, 11):
            i = y * 11 + x
            if i <= len(values) - 1:
                r, g, b, w = values[i]
                led_matrix[i] = (r, g, b, w)
            else:
                led_matrix[i] = (0, 0, 0, 0)

    led_matrix.show()
