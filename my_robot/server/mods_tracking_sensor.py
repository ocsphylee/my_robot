# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/1 23:58
Descriptions: 返回循迹模块的结果
'''

import RPi.GPIO as GPIO
import time


class Tracking:
    def __init__(self,left_pin = 20, middel_pin = 16,right_pin = 19):
        self.left_pin = left_pin
        self.middel_pin = middel_pin
        self.right_pin = right_pin
        # 设置GPIO接口
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_pin, GPIO.IN)
        GPIO.setup(self.middel_pin, GPIO.IN)
        GPIO.setup(self.right_pin, GPIO.IN)
        # 循迹结果
        self.status_right = None
        self.status_middle = None
        self.status_left = None

    def tracking_result(self):
        """
        返回三路循迹结果
        """
        self.status_right = GPIO.input(self.right_pin)
        self.status_middle = GPIO.input(self.middel_pin)
        self.status_left = GPIO.input(self.left_pin)


if __name__ == '__main__':
    tracking = Tracking()
    while 1:
        tracking.tracking_result()
        time.sleep(0.5)
        print('left:{}, middel:{}, right:{}'.format(tracking.status_left,tracking.status_middle,tracking.status_right))

