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
                         Commands.LOOKDOWN.value, Commands.LOOSE.value]
        self.nagetive = [Commands.LOOKRIGHT.value, Commands.UP.value,
                         Commands.LOOKUP.value, Commands.GRAB.value]

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
        self.pwm1_max = 480
        self.pwm1_min = 160
        self.pwm1_pos = self.pwm1_init

        self.pwm2_init = 300
        self.pwm2_max = 700
        self.pwm2_min = 100
        self.pwm2_pos = self.pwm2_init

        self.pwm3_init = 300
        self.pwm3_max = 500
        self.pwm3_min = 300
        self.pwm3_pos = self.pwm3_init

        self.pwm0 = Servo(0, self.pwm0_init, self.pwm0_max, self.pwm0_min)
        self.pwm1 = Servo(1, self.pwm1_init, self.pwm1_max, self.pwm1_min)
        self.pwm2 = Servo(2, self.pwm2_init, self.pwm2_max, self.pwm2_min)
        self.pwm3 = Servo(3, self.pwm3_init, self.pwm3_max, self.pwm3_min)

    def servo_init(self):
        """
        设置初始位置
        """
        self.pwm0_pos = self.pwm0_init
        self.pwm1_pos = self.pwm1_init
        self.pwm2_pos = self.pwm2_init
        self.pwm3_pos = self.pwm3_init
        self.pwm0.servo_pos(self.pwm0_pos)
        self.pwm1.servo_pos(self.pwm1_pos)
        self.pwm2.servo_pos(self.pwm2_pos)
        self.pwm3.servo_pos(self.pwm3_pos)


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

        else:
            pass

    def ahead(self):
        """
        控制云台达到指定位置
        :return:
        """
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
    yuntai = YunTai()
    yuntai.servo_init()

    while True:
        print('please input command')
        command = input()
        yuntai.servo_turn(command, servo_speed=30)

        if command == 'q':
            yuntai.servo_init()
            break
        elif command == 'ahead':
            yuntai.ahead()

    # yuntai.servo_init()
    time.sleep(2)
    # clean_all()


'''
def servo_init():
    """
    设置初始位置
    """
    pwm.set_pwm(0, 0, pwm0_init)
    pwm.set_pwm(1, 0, pwm1_init)
    pwm.set_pwm(2, 0, pwm2_init)
    pwm.set_pwm(3, 0, pwm3_init)


def servo_turn(servo_command, servo_speed=1):
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

    if servo_command in ctrl_0:
        servo_0(servo_command, servo_speed)

    elif servo_command in ctrl_1:
        servo_1(servo_command, servo_speed)

    elif servo_command in ctrl_2:
        servo_2(servo_command, servo_speed)

    elif servo_command in ctrl_3:
        servo_3(servo_command, servo_speed)

    else:
        pass
'''

'''
def servo_0(pwm0_direction, speed=1):
    """
    0号舵机，控制水平方向左右转动
    :param pwm0_direction: 方向控制，string: {'lookleft','lookright'}
    :param speed: 速度
    :return: None
    """
    global pwm0_pos
    if pwm0_direction == Commands.LOOKLEFT.value:
        pwm0_pos += speed
        pwm0_pos = ctrl_range(pwm0_pos, pwm0_max, pwm0_min)
        pwm.set_pwm(0, 0, pwm0_pos)
    elif pwm0_direction == Commands.LOOKRIGHT.value:
        pwm0_pos -= speed
        pwm0_pos = ctrl_range(pwm0_pos, pwm0_max, pwm0_min)
        pwm.set_pwm(0, 0, pwm0_pos)
    else:
        pass


def servo_1(pwm1_direction, speed=1):
    """
    1号舵机，控制云台的上下转动
    :param pwm1_direction: 方向，string: {'up','down'}
    :param speed: 速度
    :return:
    """
    global pwm1_pos
    if pwm1_direction == Commands.UP.value:
        pwm1_pos -= speed
        pwm1_pos = ctrl_range(pwm1_pos, pwm1_max, pwm1_min)
        pwm.set_pwm(1, 0, pwm1_pos)
    elif pwm1_direction == Commands.DOWN.value:
        pwm1_pos += speed
        pwm1_pos = ctrl_range(pwm1_pos, pwm1_max, pwm1_min)
        pwm.set_pwm(1, 0, pwm1_pos)
    else:
        pass


def servo_2(pwm2_direction, speed=1):
    """
    2号舵机，控制摇臂摄像头
    :param pwm2_direction: 方向，string: ['lookup', 'lookdown']
    :param speed: 速度
    :return:
    """
    global pwm2_pos
    if pwm2_direction == Commands.LOOKUP.value:
        pwm2_pos -= speed
        pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, pwm2_min)
        pwm.set_pwm(2, 0, pwm2_pos)
    elif pwm2_direction == Commands.LOOKDOWN.value:
        pwm2_pos += speed
        pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, pwm2_min)
        pwm.set_pwm(2, 0, pwm2_pos)
    else:
        pass


def servo_3(pwm3_direction, speed):
    """
    3号舵机，控制摇臂钳抓取和放开。
    :param pwm3_direction: ['grab', 'loose']
    :param speed:
    :return:
    """
    global pwm3_pos
    if pwm3_direction == Commands.GRAB.value:
        pwm3_pos -= speed
        pwm3_pos = ctrl_range(pwm3_pos, pwm3_max, pwm3_min)
        pwm.set_pwm(3, 0, pwm3_pos)
    elif pwm3_direction == Commands.LOOSE.value:
        pwm3_pos += speed
        pwm3_pos = ctrl_range(pwm3_pos, pwm3_max, pwm3_min)
        pwm.set_pwm(3, 0, pwm3_pos)
    else:
        pass
'''