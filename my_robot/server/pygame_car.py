# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/14 15:52
Descriptions:
'''

import pygame
import time
from mods_commands import Commands
import threading
import mods_motor as move

class XboxJoyStick:

    def __init__(self):
        self.js0 = None
        self.done = False
        self.command = None


    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.joystick.init()
        self.js0 = pygame.joystick.Joystick(0)
        self.js0.init()

        while self.done == False:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True  # Flag that we are done so we exit this loop

            # Get the name from the OS for the controller/joystick
            name = self.js0.get_name()


            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = self.js0.get_numaxes()


            for i in range(axes):
                axis = self.js0.get_axis(i)
                if i == 0:
                    if axis > 0.3:
                        self.command = Commands.RIGHT.value
                    elif axis < -0.3:
                        self.command = Commands.LEFT.value
                    else:
                        self.command = Commands.TS.value

                if i == 1:
                    if axis > 0.3:
                        self.command = Commands.BACKWARD.value
                    elif axis < -0.3:
                        self.command = Commands.FORWARD.value
                    else:
                        self.command = Commands.DS.value
                # time.sleep(0.02)

if __name__ == '__main__':

    def open_stick():
        # Open the joystick device.
        fn = '/dev/input/js0'
        js_dev = open(fn, 'rb')
        return js_dev

    def run():
        global js
        connect = False
        while not connect:
            try:
                js_dev = open_stick()
                connect = True
                break
            except:
                time.sleep(5)
                pass
        if connect:
            js = XboxJoyStick()
            js.run()


    info_threading = threading.Thread(target=run)  # Define a thread for FPV and OpenCV
    info_threading.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
    info_threading.start()  # Thread starts
    time.sleep(1)

    direction_command = 'no'
    turn_command = 'no'
    motor_speed = 100
    motor_radius = 1

    move.setup()
    while 1:
        data = js.command
        if not data:
            pass
        elif Commands.FORWARD.value == data:
            direction_command = Commands.FORWARD.value
            move.move(direction_command, turn_command, motor_speed, motor_radius)

        elif Commands.BACKWARD.value == data:
            direction_command = Commands.BACKWARD.value
            move.move(direction_command, turn_command, motor_speed, motor_radius)

        elif Commands.DS.value in data:
            direction_command = Commands.NO.value
            move.move(direction_command, turn_command, motor_speed, motor_radius)

        elif Commands.LEFT.value == data:
            turn_command = Commands.LEFT.value
            move.move(direction_command, turn_command, motor_speed, motor_radius)

        elif Commands.RIGHT.value == data:
            turn_command = Commands.RIGHT.value
            move.move(direction_command, turn_command, motor_speed, motor_radius)

        elif Commands.TS.value in data:
            turn_command = Commands.NO.value
            move.move(direction_command, turn_command, motor_speed, motor_radius)