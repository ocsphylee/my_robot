# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/2 21:35
Descriptions: 超声扫描成像
'''


from mods_ultra import checkdist
from mods_servo import YunTai
from mods_commands import Commands
import time


def radar_scan():
    """

    :return:
    """
    yuntai = YunTai()

    scan_result = 'U: '
    scan_speed = 1
    yuntai.scan_pos()
    time.sleep(0.5)

    scan_result += str(checkdist())
    scan_result += ' '

    while yuntai.pwm0_pos > yuntai.pwm0_min:
        yuntai.servo_turn(Commands.LOOKRIGHT.value,servo_speed=scan_speed)
        scan_result += str(checkdist())
        scan_result += ' '

    yuntai.servo_init()
    return scan_result


if __name__ == '__main__':
    re = radar_scan()
    print(re)