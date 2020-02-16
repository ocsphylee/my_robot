# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/1 18:18
Descriptions: 指令枚举类
'''

from enum import Enum
import RPi.GPIO as GPIO


# 继承枚举类
class Commands(Enum):
    """
    指令的枚举类
    """
    # 云台/摇臂指令控制
    LOOKLEFT = 'lookleft'  # 0号舵机(底部),左转
    LOOKRIGHT = 'lookright'  # 0号舵机(底部),右转
    UP = 'up'  # 1号舵机，上抬
    DOWN = 'down'  # 1号舵机，低头
    LOOKUP = 'lookup'  # 2号舵机，
    LOOKDOWN = 'lookdown'  # 2号舵机，
    GRAB = 'grab'  # 3号舵机，抓取（摇臂）
    LOOSE = 'loose'  # 3号舵机，放开（摇臂）
    STOP = 'stop'
    HOME = 'home'
    ARMUP = 'armup'
    ARMDOWN = 'armdown'


    # 电机指令控制
    FORWARD = 'forward'
    BACKWARD = 'backward'
    LEFT = 'left'
    RIGHT = 'right'
    NO = 'no'
    DS = 'DS'
    TS = 'TS'
    WSB = 'wsB'

    # Port 开关指令
    ON = GPIO.HIGH
    OFF = GPIO.LOW
    # Port 状态指令
    SWITCH_1_ON = 'Switch_1_on'
    SWITCH_1_OFF = 'Switch_1_off'
    SWITCH_2_ON = 'Switch_2_on'
    SWITCH_2_OFF = 'Switch_2_off'
    SWITCH_3_ON = 'Switch_3_on'
    SWITCH_3_OFF = 'Switch_3_off'

    # 功能按钮状态
    FUNCTION_1_ON = 'function_1_on'
    FUNCTION_1_OFF = 'function_1_off'
    FUNCTION_2_ON = 'function_2_on'
    FUNCTION_2_OFF = 'function_2_off'
    FUNCTION_3_ON = 'function_3_on'
    FUNCTION_3_OFF = 'function_3_off'
    FUNCTION_4_ON = 'function_4_on'
    FUNCTION_4_OFF = 'function_4_off'
    FUNCTION_5_ON = 'function_5_on'
    FUNCTION_5_OFF = 'function_5_off'
    FUNCTION_6_ON = 'function_6_on'
    FUNCTION_6_OFF = 'function_6_off'

    CVFL_ON = 'CVFL_on'
    CVFL_OFF = 'CVFL_off'
    RENDER = 'Render'
    WBSWITCH = 'WBswitch'
    LIP1 = 'lip1'
    LIP2 = 'lip2'
    ERR = 'err'

    # 屏幕指令
    WELCOME = 'welcome'
    PANEL = 'panel'

if __name__ == '__main__':
    yuntai_commands = [Commands.LOOKLEFT.value, Commands.LOOKRIGHT.value,
                       Commands.UP.value, Commands.DOWN.value,
                       Commands.LOOKUP.value, Commands.LOOKDOWN.value,
                       Commands.GRAB.value, Commands.LOOSE.value]
    print('up' in yuntai_commands)