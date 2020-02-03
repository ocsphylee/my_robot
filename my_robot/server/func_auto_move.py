# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/2 23:15
Descriptions:
'''

import mods_motor as move
from mods_ultra import checkdist
from mods_servo import YunTai
from mods_commands import Commands
import time





class AutoMove:

    def __init__(self):
        try:
            move.setup()
        except:
            pass

    def run(self):
        # 自动模式
        yuntai = YunTai()
        yuntai.ahead()
        time.sleep(1)
        # 超声测距
        dis_get = checkdist()

        if dis_get < 0.15:
            move.motor_stop()
            move.move(Commands.BACKWARD.value, Commands.NO.value, 100, 1)
            time.sleep(0.5)
            move.motor_stop()
            move.move(Commands.NO.value, Commands.LEFT.value, 100, 1)
            time.sleep(0.2)
            move.motor_stop()

        else:
            move.move(Commands.FORWARD.value, Commands.NO.value, 100, 1)

    def stop(self):
        move.motor_stop()


if __name__ == '__main__':
    auto = AutoMove()
    t = 0
    while t< 10:
        t += 1
        time.sleep(0.5)
        auto.run()
        print(t)
    print('stop')
    auto.stop()
    time.sleep(10)
    print('end')
