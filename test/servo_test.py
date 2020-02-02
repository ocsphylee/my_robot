# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/1/31 14:25
Description: 舵机控制测试
'''

from __future__ import division
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import time

# 设置默认值
# 左右
pwm0_init = 300
pwm0_max = 450
pwm0_min = 150
pwm0_pos = pwm0_min
pos = 3

# 上下
pwm1_init = 300
pwm1_max = 480
pwm1_min = 160
pwm1_pos = pwm1_init

# 实例化PWM对象
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)
pwm.set_pwm(1, 0, pwm1_min)


def loop():
    global pwm1_pos, pos

    tmp = pwm1_pos + pos
    if tmp > pwm1_max or tmp < pwm1_min:
        pos = -pos

    pwm1_pos += pos
    pwm.set_pwm(1, 0, pwm1_pos)
    time.sleep(0.1)


if __name__ == '__main__':
    while 1:
        loop()
