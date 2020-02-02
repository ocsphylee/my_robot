# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/2 21:03
Descriptions: 红外循迹，电机控制
'''


from mods_tracking_sensor import Tracking
import mods_motor as move
from mods_commands import Commands


class TrackingMove:
    def __init__(self):
        self.sensor = Tracking()
        try:
            move.setup()
        except:
            pass

    def run(self):

        self.sensor.tracking_result()

        if self.sensor.status_middle:
            move.move(Commands.FORWARD.value, Commands.NO.value, 100,  1)
        elif self.sensor.status_left == 1:
            move.move(Commands.FORWARD.value, Commands.RIGHT.value, 100, 1)
        elif self.sensor.status_right == 1:
            move.move(Commands.FORWARD.value, Commands.LEFT.value, 100, 1)
        else:
            move.move(Commands.BACKWARD.value, Commands.NO.value, 100, 1)

    def stop(self):
        self.sensor.destroy()
        move.motor_stop()

if __name__ == '__main__':

    while 1:
        tracking()