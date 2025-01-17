# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/1/31 22:32
Description: LED灯条
'''


import time
from rpi_ws281x import *
import argparse
import random


# LED strip configuration:
LED_COUNT      = 3      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


LED = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
LED.begin()

def random_color():
    R = random.randint(0, 255)
    G = random.randint(0, 255)
    B = random.randint(0, 255)
    return Color(R, G, B)

while 1:
    color = random_color()
    for i in range(LED.numPixels()):
        LED.setPixelColor(i,color)
        LED.show()
        time.sleep(0.1)
    time.sleep(0.3)