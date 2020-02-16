# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/1 17:24
Descriptions: PWM舵机控制
'''

from __future__ import division
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import time
from mods_commands import Commands


# 实例化PWM对象
global pwm
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


class Servo:
    """
    舵机对象
    """
    def __init__(self, pwm_pin,pwm_init,pwm_max,pwm_min):
        self.pwm_pin = pwm_pin
        self.pwm_init = pwm_init
        self.pwm_max = pwm_max
        self.pwm_min = pwm_min
        self.pwm_pos = pwm_init
        self.positive = [Commands.LOOKLEFT.value, Commands.DOWN.value,
                         Commands.LOOKDOWN.value, Commands.GRAB.value,
                         Commands.ARMDOWN.value]
        self.nagetive = [Commands.LOOKRIGHT.value, Commands.UP.value,
                         Commands.LOOKUP.value, Commands.LOOSE.value,
                         Commands.ARMUP.value]

    def ctrl_range(self, raw, max_genout, min_genout):
        """
        控制角度，防止转动超过指定位置
        :param raw: 原始输入角度
        :param max_genout: 最大角度
        :param min_genout: 最小角度
        :return: 允许执行的转动值
        """
        if raw > max_genout:
            raw_output = max_genout
        elif raw < min_genout:
            raw_output = min_genout
        else:
            raw_output = raw
        return int(raw_output)

    def servo_pos(self, pos):
        self.pwm_pos = self.ctrl_range(pos, self.pwm_max, self.pwm_min)
        pwm.set_pwm(self.pwm_pin, 0, self.pwm_pos)

    def servo_ctrl(self, command, speed=1):
        if command in self.positive:
            self.pwm_pos += speed
            self.servo_pos(self.pwm_pos)
        elif command in self.nagetive:
            self.pwm_pos -= speed
            self.servo_pos(self.pwm_pos)
        else:
            pass


class YunTai:
    def __init__(self):
        # 设置默认值
        # pwm0: 底部舵机，左右方向
        self.pwm0_init = 300
        self.pwm0_max = 450
        self.pwm0_min = 150
        self.pwm0_pos = self.pwm0_init

        self.pwm1_init = 300
        self.pwm1_max = 450
        self.pwm1_min = 160
        self.pwm1_pos = self.pwm1_init

        self.pwm2_init = 450
        self.pwm2_max = 700
        self.pwm2_min = 10
        self.pwm2_pos = self.pwm2_init

        self.pwm3_init = 300
        self.pwm3_max = 500
        self.pwm3_min = 300
        self.pwm3_pos = self.pwm3_init

        self.pwm4_init = 150
        self.pwm4_max = 390
        self.pwm4_min = 100
        self.pwm4_pos = self.pwm4_init

        self.pwm0 = Servo(0, self.pwm0_init, self.pwm0_max, self.pwm0_min)
        self.pwm1 = Servo(1, self.pwm1_init, self.pwm1_max, self.pwm1_min)
        self.pwm2 = Servo(2, self.pwm2_init, self.pwm2_max, self.pwm2_min)
        self.pwm3 = Servo(3, self.pwm3_init, self.pwm3_max, self.pwm3_min)
        self.pwm4 = Servo(4, self.pwm4_init, self.pwm4_max, self.pwm4_min)

    def servo_init(self):
        """
        设置初始位置
        """
        self.pwm0_pos = self.pwm0_init
        self.pwm1_pos = self.pwm1_init
        self.pwm2_pos = self.pwm2_init
        self.pwm3_pos = self.pwm3_init
        self.pwm4_pos = self.pwm4_init

        self.pwm0.servo_pos(self.pwm0_pos)
        self.pwm1.servo_pos(self.pwm1_pos)
        self.pwm2.servo_pos(self.pwm2_pos)
        self.pwm3.servo_pos(self.pwm3_pos)
        time.sleep(1)
        self.pwm4.servo_pos(self.pwm4_pos)

    def servo_turn(self, servo_command, servo_speed=1):
        """
        云台/摇臂控制
        :param servo_command: str, 云台/摇臂转动指令
        :param servo_speed: int, 移动速度
        :return: None
        """
        ctrl_0 = [Commands.LOOKLEFT.value, Commands.LOOKRIGHT.value]
        ctrl_1 = [Commands.UP.value, Commands.DOWN.value]
        ctrl_2 = [Commands.LOOKUP.value, Commands.LOOKDOWN.value]
        ctrl_3 = [Commands.GRAB.value, Commands.LOOSE.value]
        ctrl_4 = [Commands.ARMDOWN.value, Commands.ARMUP.value]

        if servo_command in ctrl_0:
            self.pwm0.servo_ctrl(servo_command, servo_speed)
            self.pwm0_pos = self.pwm0.pwm_pos

        elif servo_command in ctrl_1:
            self.pwm1.servo_ctrl(servo_command, servo_speed)
            self.pwm1_pos = self.pwm1.pwm_pos

        elif servo_command in ctrl_2:
            self.pwm2.servo_ctrl(servo_command, servo_speed)
            self.pwm2_pos = self.pwm2.pwm_pos

        elif servo_command in ctrl_3:
            self.pwm3.servo_ctrl(servo_command, servo_speed)
            self.pwm3_pos = self.pwm3.pwm_pos

        elif servo_command in ctrl_4:
            self.pwm4.servo_ctrl(servo_command, servo_speed)
            self.pwm4_pos = self.pwm4.pwm_pos

        else:
            pass

    def ahead(self):
        """
        控制云台达到指定位置
        :return:
        """
        self.pwm4_pos = self.pwm4_init
        self.pwm4.servo_pos(self.pwm4_pos)
        time.sleep(1)
        self.pwm0_pos = self.pwm0_init
        self.pwm1_pos = self.pwm1_max - 20
        self.pwm0.servo_pos(self.pwm0_pos)
        self.pwm1.servo_pos(self.pwm1_pos)

    def get_direction(self):
        """
        获取云台左右旋转的位置
        """
        return self.pwm0_pos - self.pwm0_init

    def scan_pos(self):
        """
        超声测距扫描的初始位置
        :return:
        """
        self.pwm4_pos = self.pwm4_init
        self.pwm4.servo_pos(self.pwm4_pos)
        time.sleep(1)
        self.pwm0_pos = self.pwm0_max
        self.pwm1_pos = self.pwm1_max - 20
        self.pwm0.servo_pos(self.pwm0_pos)
        self.pwm1.servo_pos(self.pwm1_pos)

def clean_all():
    """
    清除设置，释放PWM接口
    :return:
    """
    global pwm
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(50)
    pwm.set_all_pwm(0, 0)


if __name__ == '__main__':
    # arm = Servo(4, 100, 370, 100)
    # arm.servo_pos(100)
    yuntai = YunTai()
    yuntai.servo_init()
    # yuntai.pwm4.servo_pos(390)
    # while True:
    #     print('please input command')
    #     command = input()
    #     yuntai.servo_turn(command, servo_speed=30)
    #
    #     if command == 'q':
    #         yuntai.servo_init()
    #         break
    #     elif command == 'ahead':
    #         yuntai.ahead()
    #
    # time.sleep(2)

