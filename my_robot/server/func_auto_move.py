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
        self.safety_dist = 0.4
        try:
            move.setup()
        except:
            pass

    def run(self, speed):
        # 自动模式
        yuntai = YunTai()
        yuntai.ahead()
        # 超声测距
        dis_get = checkdist()

        if dis_get < self.safety_dist:
            move.motor_stop()
            # 左看
            yuntai.pwm0.servo_pos(400)
            time.sleep(1)
            left_dist = checkdist()
            # 右看
            yuntai.pwm0.servo_pos(200)
            time.sleep(1)
            right_dist = checkdist()
            # 居中
            yuntai.ahead()
            if left_dist < self.safety_dist and right_dist < self.safety_dist:
                move.move(Commands.BACKWARD.value, Commands.NO.value, speed, 1)
                time.sleep(1)
                move.motor_stop()
            else:
                if left_dist >= right_dist :
                    move.move(Commands.NO.value, Commands.LEFT.value, speed, 1)
                    time.sleep(0.8)
                    move.motor_stop()
                else:
                    move.move(Commands.NO.value, Commands.RIGHT.value, speed, 1)
                    time.sleep(0.8)
                    move.motor_stop()
        else:
            move.move(Commands.FORWARD.value, Commands.NO.value, speed, 1)

    def stop(self):
        move.motor_stop()


if __name__ == '__main__':
    auto = AutoMove()
    t = 0
    try:
        while 1:
            auto.run(80)
    except KeyboardInterrupt:
        auto.stop()
