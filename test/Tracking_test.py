# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/1/31 23:09
'''

import RPi.GPIO as GPIO
import time

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)

def loop():
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)

    if status_middle == 1:
        print('middle sensor detected blackline')
    elif status_left == 1:
        print('left sensor detected blackline')
    elif status_right == 1:
        print('right sensor detected blackline')
    else:
        print('no sensor detected blackline')

if __name__ == '__main__':
    setup()
    while 1:
        loop()
        time.sleep(0.5)