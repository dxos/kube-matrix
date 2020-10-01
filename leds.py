#!/usr/bin/env python3

import sys, os
import neopixel
import board
import paho.mqtt.client as mqtt

# LRASPBERRED SETTINGS
LED_COUNT      = 121            # Number of LED pixels.
LED_PIN        = board.D18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000         # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5              # DMA channel to use for generating signal (try 5)
brightness     = 200            # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False          # True to invert the signal (when using NPN transistor level shift)

#global LEDMatrix
# LEDMatrix = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
#LEDMatrix = neopixel.NeoPixel(board.D18, LED_COUNT)
# LEDMatrix.begin()

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW

global LEDMatrix
LEDMatrix = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.1, auto_write=False, pixel_order=ORDER)

global LEDBuffer
global prevLEDBuffer

def renderLEDBuffer(inData):
    global strip
    parseData = inData.split(",")
    
    for x in range(0, 121):
        idx = x*4
        
        r = parseData[idx]
        g = parseData[idx+1]
        b = parseData[idx+2]
        w = parseData[idx+3]
        
        #print(r," ",g," ",b," ",w)
        
        LEDMatrix[x] = (int(r), int(g), int(b), int(w))
    
    LEDMatrix.show()

# MQTT
class mqttClient:
    def on_connect(self, master, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        #TODO use the hardware address of the RPi
        self.master.subscribe("dxos")

    def on_message(self, master, userdata, msg):
        self.topic      = str(msg.topic).split("/")[0]
        self.data        = str(msg.payload, 'UTF8').split("/")[0] # the buffer
        
        # now parse out the buffer and set the strip.
        # print ("received message: " , self.topic , " , " , self.data)
        
        # send to render
        renderLEDBuffer(self.data)


    def __init__(self, master):
        try:
            self.master=master
            self.master.on_connect=self.on_connect
            self.master.on_message=self.on_message
            self.master.connect('127.0.0.1', 1883, 60)
        except:
            e = sys.exc_info()[0]
            print (e)

# DEFINE
global server
server = '127.0.0.1'

global client
client = mqtt.Client()

# APP
def main():
    global client

    print ("main")
    
    print ("starting mqtt thread")   
    mqttObject = mqttClient(client)
    client.loop_forever()

# MAIN
if __name__ == "__main__":
    print ("Initializing...")
    main()
