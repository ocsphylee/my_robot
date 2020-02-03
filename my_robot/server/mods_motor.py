# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/1 21:59
Descriptions: 电机控制
'''


import time
import RPi.GPIO as GPIO
from enum import Enum
from mods_commands import Commands

# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

# pwm 接口用于调整速度
Motor_A_EN = 4
Motor_B_EN = 17

# 调整方向的接口
Motor_A_Pin1 = 26  # HIGH: 顺时针转, LOW: 逆时针转
Motor_A_Pin2 = 21  # LOW:  顺时针转, HIGH: 逆时针转
Motor_B_Pin1 = 27  # HIGH: 顺时针转, LOW: 逆时针转
Motor_B_Pin2 = 18  # LOW:  顺时针转, HIGH: 逆时针转


def motor_stop():  # Motor stops
    """
    停止运动
    :return:
    """
    motor_ctrl('left', Rotate.STOP.value, 0)
    motor_ctrl('right', Rotate.STOP.value, 0)


def setup():
    """
    初始化，设置GPIO接口
    :return:
    """
    global pwm_A, pwm_B
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_B_EN, GPIO.OUT)
    GPIO.setup(Motor_A_Pin1, GPIO.OUT)
    GPIO.setup(Motor_A_Pin2, GPIO.OUT)
    GPIO.setup(Motor_B_Pin1, GPIO.OUT)
    GPIO.setup(Motor_B_Pin2, GPIO.OUT)
    pwm_A = GPIO.PWM(Motor_A_EN, 1000)
    pwm_B = GPIO.PWM(Motor_B_EN, 1000)

    motor_stop()



# 继承枚举类
class Rotate(Enum):
    """
    电机控制命令
    """
    STOP = 'stop'
    BACKWARD = 'backward'
    FORWARD = 'forward'


def motor_ctrl(pin, status, speed):
    """
        电机控制
        :param pin: str,{'left','right'}表示，左边电机或右边电机
        :param status: str,{'stop','clockwise','anticlockwise'}，表示停止，顺时针，逆时针
        :param speed: 速度（PWM占空比）
        :return: None
        """
    global pins
    pins = {'left': [Motor_B_Pin1, Motor_B_Pin2, Motor_B_EN, pwm_B],
            'right': [Motor_A_Pin1, Motor_A_Pin2, Motor_A_EN, pwm_A]}
    motor = pins[pin]

    if status == Rotate.STOP.value:  # stop
        GPIO.output(motor[0], GPIO.LOW)
        GPIO.output(motor[1], GPIO.LOW)
        GPIO.output(motor[2], GPIO.LOW)

    elif status == Rotate.BACKWARD.value:
        GPIO.output(motor[0], GPIO.HIGH)
        GPIO.output(motor[1], GPIO.LOW)
        motor[3].start(100)
        motor[3].ChangeDutyCycle(speed)

    elif status == Rotate.FORWARD.value:
        GPIO.output(motor[0], GPIO.LOW)
        GPIO.output(motor[1], GPIO.HIGH)
        motor[3].start(0)
        motor[3].ChangeDutyCycle(speed)

    else:
        pass


def move(direction, turn, speed, radius=0.6):   # 0 < radius <= 1
    """
    控制小车移动
    :param direction: 前后，{'forward','backward'}
    :param turn: 左右, {'left','right'}
    :param speed: 速度（占空比） [0,100]
    :param radius: 降速比，[0,1]
    :return:
    """
    if direction == Commands.FORWARD.value:
        if turn == Commands.RIGHT.value:
            motor_ctrl('left',Rotate.STOP.value, int(speed * radius))
            motor_ctrl('right', Rotate.FORWARD.value, speed)

        elif turn == Commands.LEFT.value:
            motor_ctrl('left', Rotate.FORWARD.value, speed)
            motor_ctrl('right', Rotate.STOP.value, int(speed * radius))

        else:
            motor_ctrl('left', Rotate.FORWARD.value, speed)
            motor_ctrl('right', Rotate.FORWARD.value, speed)

    elif direction == Commands.BACKWARD.value:
        if turn == Commands.RIGHT.value:
            motor_ctrl('left', Rotate.STOP.value, speed)
            motor_ctrl('right', Rotate.BACKWARD.value, speed)

        elif turn == Commands.LEFT.value:
            motor_ctrl('left', Rotate.BACKWARD.value, speed)
            motor_ctrl('right', Rotate.STOP.value, int(speed * radius))

        else:
            motor_ctrl('left', Rotate.BACKWARD.value, speed)
            motor_ctrl('right', Rotate.BACKWARD.value, speed)

    elif direction == Commands.NO.value:
        if turn == Commands.RIGHT.value:
            motor_ctrl('left', Rotate.BACKWARD.value, speed)
            motor_ctrl('right', Rotate.FORWARD.value, speed)

        elif turn == Commands.LEFT.value:
            motor_ctrl('left', Rotate.FORWARD.value, speed)
            motor_ctrl('right', Rotate.BACKWARD.value, speed)
        else:
            motor_stop()
    else:
        pass


def destroy():
    """
    停止程序，释放接口
    :return:
    """
    motor_stop()
    GPIO.cleanup()             # Release resource


if __name__ == '__main__':
    try:
        speed_set = 100
        setup()
        move('no', 'left',speed_set, 0.9)
        time.sleep(10)
        motor_stop()
        destroy()
    except KeyboardInterrupt:
        destroy()
