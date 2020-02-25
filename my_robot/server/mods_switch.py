# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/2 0:08
Descriptions:
'''


import RPi.GPIO as GPIO
from enum import Enum
import time
from mods_commands import Commands

class Switch:
    def __init__(self):
        """
        设置port1,2,3接口
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # Port 接口编码
        self.PORT1 = 5
        self.PORT2 = 6
        self.PORT3 = 13
        GPIO.setup(self.PORT1, GPIO.OUT)
        GPIO.setup(self.PORT2, GPIO.OUT)
        GPIO.setup(self.PORT3, GPIO.OUT)


    def switch_ctrl(self, port, status):
        """
        通过GPIO控制port接口开关
        :param port: 来自Ports，接口编码
        :param status: 来自Ports，开关指令
        """
        GPIO.output(port, status)


    def set_all_switch_on(self):
        self.switch_ctrl(self.PORT1, Commands.ON.value)
        self.switch_ctrl(self.PORT2, Commands.ON.value)
        self.switch_ctrl(self.PORT3, Commands.ON.value)

    def set_all_switch_off(self):
        self.switch_ctrl(self.PORT1, Commands.OFF.value)
        self.switch_ctrl(self.PORT2, Commands.OFF.value)
        self.switch_ctrl(self.PORT3, Commands.OFF.value)

if __name__ == '__main__':
    swtich = Switch()
    swtich.set_all_switch_on()
    time.sleep(60)
    swtich.set_all_switch_off()
