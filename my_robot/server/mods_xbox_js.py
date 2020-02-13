# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/13 20:48
Descriptions:
'''

import os, struct, array
from fcntl import ioctl
import time
from mods_commands import Commands
import threading
import mods_motor as move

# These constants were borrowed from linux/input.h
axis_names = {
    0x00: 'x',
    0x01: 'y',
    0x02: 'z',
    0x03: 'rx',
    0x04: 'ry',
    0x05: 'rz',
    0x06: 'trottle',
    0x07: 'rudder',
    0x08: 'wheel',
    0x09: 'gas',
    0x0a: 'brake',
    0x10: 'hat0x',
    0x11: 'hat0y',
    0x12: 'hat1x',
    0x13: 'hat1y',
    0x14: 'hat2x',
    0x15: 'hat2y',
    0x16: 'hat3x',
    0x17: 'hat3y',
    0x18: 'pressure',
    0x19: 'distance',
    0x1a: 'tilt_x',
    0x1b: 'tilt_y',
    0x1c: 'tool_width',
    0x20: 'volume',
    0x28: 'misc',
}

button_names = {
    0x120: 'trigger',
    0x121: 'thumb',
    0x122: 'thumb2',
    0x123: 'top',
    0x124: 'top2',
    0x125: 'pinkie',
    0x126: 'base',
    0x127: 'base2',
    0x128: 'base3',
    0x129: 'base4',
    0x12a: 'base5',
    0x12b: 'base6',
    0x12f: 'dead',
    0x130: 'a',
    0x131: 'b',
    0x132: 'c',
    0x133: 'x',
    0x134: 'y',
    0x135: 'z',
    0x136: 'tl',
    0x137: 'tr',
    0x138: 'tl2',
    0x139: 'tr2',
    0x13a: 'select',
    0x13b: 'start',
    0x13c: 'mode',
    0x13d: 'thumbl',
    0x13e: 'thumbr',

    0x220: 'dpad_up',
    0x221: 'dpad_down',
    0x222: 'dpad_left',
    0x223: 'dpad_right',

    # XBox 360 controller uses these codes.
    0x2c0: 'dpad_left',
    0x2c1: 'dpad_right',
    0x2c2: 'dpad_up',
    0x2c3: 'dpad_down',
}

def open_stick():
    # Open the joystick device.
    fn = '/dev/input/js0'
    js_dev = open(fn, 'rb')
    return js_dev


def get_btn_ax(jsdev):
    axis_map = []
    button_map = []
    # Get number of axes and buttons.
    buf = array.array('B', [0])
    ioctl(jsdev, 0x80016a11, buf)  # JSIOCGAXES
    num_axes = buf[0]

    buf = array.array('B', [0])
    ioctl(jsdev, 0x80016a12, buf)  # JSIOCGBUTTONS
    num_buttons = buf[0]

    # Get the axis map.
    buf = array.array('B', [0] * 0x40)
    ioctl(jsdev, 0x80406a32, buf)  # JSIOCGAXMAP

    for axis in buf[:num_axes]:
        axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
        axis_map.append(axis_name)

    # Get the button map.
    buf = array.array('H', [0] * 200)
    ioctl(jsdev, 0x80406a34, buf)  # JSIOCGBTNMAP

    for btn in buf[:num_buttons]:
        btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
        button_map.append(btn_name)

    return button_map, axis_map


class XboxJoyStick:
    def __init__(self, jsdev):
        self.jsdev = jsdev
        self.button_map, self.axis_map = get_btn_ax(self.jsdev)
        self.command = ''

    def event_detected(self):
        evbuf = self.jsdev.read(8)
        time, value, type, number = struct.unpack('IhBB', evbuf)
        return value, type, number

    def run(self):
        while 1:
            value, type, number = self.event_detected()
            contrl = None
            if type == 1:
                # buttom
                contrl = self.button_map[number]


            elif type == 2:
                # axis
                contrl = self.axis_map[number]
                fvalue = value / 32767.0
                # ---------axis commands------------

                if contrl == 'x':
                    if fvalue >  0.4:
                        self.command = Commands.RIGHT.value
                    elif fvalue < -0.4:
                        self.command = Commands.LEFT.value
                    else:
                        self.command = Commands.TS.value

                if contrl == 'y':
                    if fvalue >  0.4:
                        self.command = Commands.BACKWARD.value
                    elif fvalue < -0.4:
                        self.command = Commands.FORWARD.value
                    else:
                        self.command = Commands.DS.value
            else:
                pass







if __name__ == '__main__':

    def run():
        global stick
        while 1:
            try:
                js_dev = open_stick()
                break
            except:
                time.sleep(5)
                pass
        stick = XboxJoyStick(js_dev)
        stick.run()

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
        data = stick.command
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