# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/1 23:36
Descriptions:
'''

from rpi_ws281x import *
import time
import random


class LED:
    """
    LED灯条控制
    """
    def __init__(self, led_count=3, pin=12):
        # Number of LED pixels.
        self.LED_COUNT = led_count
        # GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_PIN = pin
        # LED signal frequency in hertz (usually 800khz)
        self.LED_FREQ_HZ = 800000
        # DMA channel to use for generating signal (try 10)
        self.LED_DMA = 10
        # Set to 0 for darkest and 255 for brightest
        self.LED_BRIGHTNESS = 255
        # True to invert the signal (when using NPN transistor level shift)
        self.LED_INVERT = False
        # set to '1' for GPIOs 13, 19, 41, 45 or 53
        self.LED_CHANNEL = 0

        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(
            self.LED_COUNT,
            self.LED_PIN,
            self.LED_FREQ_HZ,
            self.LED_DMA,
            self.LED_INVERT,
            self.LED_BRIGHTNESS,
            self.LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    # Define functions which animate LEDs in various ways.

    def color_single(self, i, R, G, B):
        """
        控制单个灯
        :param i: 编号
        :return:
        """
        if i > self.strip.numPixels():

            return None
        color = Color(R, G, B)
        self.strip.setPixelColor(i, color)
        self.strip.show()

    def color_wipe(self, R, G, B):
        """
        控制全部灯条
        :return:
        """
        for i in range(self.strip.numPixels()):
            self.color_single(i, R, G, B)

    def close(self):
        """
        关闭灯条
        :return:
        """
        self.color_wipe(0, 0, 0)

    def random_color(self):
        """
        随机颜色
        :return:
        """
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        return Color(R, G, B)

    def celebrate(self):
        """
        随机闪烁模式
        :return:
        """
        color = self.random_color()
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(0.1)
        time.sleep(0.3)


if __name__ == '__main__':
    led = LED()
    led.color_wipe(0, 0, 255)
    time.sleep(3)
    led.close()
