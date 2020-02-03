# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/1 23:30
Descriptions: 超声测距
'''

import RPi.GPIO as GPIO
import time

Tr = 11
Ec = 8

# TODO: 通过MPU6050进行三角测距，提高准确度

def checkdist():
    """
    超声测距
    :return: float, 所测距离（米）
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Tr, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(Ec, GPIO.IN)
    GPIO.output(Tr, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(Tr, GPIO.LOW)

    while not GPIO.input(Ec):  # 等待接收
        pass
    # 接到第一个信号，计时
    t1 = time.time()
    while GPIO.input(Ec):  # 等待接完
        pass
    # 接完信号，计时
    t2 = time.time()
    return round((t2-t1)*340/2, 2)

if __name__ == '__main__':
    while 1:
        print(checkdist())
        time.sleep(1)
        GPIO.cleanup()
