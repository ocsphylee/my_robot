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
from socket import *

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
        name = self.js0.get_name()

        print('{} is connected'.format(name))

        while self.done == False:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True  # Flag that we are done so we exit this loop

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = self.js0.get_numaxes()
            for i in range(axes):
                axis = self.js0.get_axis(i)

                # --------左侧摇杆控制小车移动----------

                #    ----控制左右移动----
                if i == 0:
                    if axis > 0.3:
                        # self.command = Commands.RIGHT.value
                        s.send(Commands.RIGHT.value.encode())
                    elif axis < -0.3:
                        # self.command = Commands.LEFT.value
                        s.send(Commands.LEFT.value.encode())
                    else:
                        # self.command = Commands.TS.value
                        s.send(Commands.TS.value.encode())

                #    ----控制前后移动----
                if i == 1:
                    if axis > 0.3:
                        # self.command = Commands.BACKWARD.value
                        s.send(Commands.BACKWARD.value.encode())
                    elif axis < -0.3:
                        # self.command = Commands.FORWARD.value
                        s.send(Commands.FORWARD.value.encode())
                    else:
                        # self.command = Commands.DS.value
                        s.send(Commands.DS.value.encode())

                # --------左侧摇杆控制云台----------

                #    ----控制左右转动----
                if i == 2:
                    if axis > 0.3:
                        s.send(Commands.LOOKRIGHT.value.encode())
                    elif axis < -0.3:
                        s.send(Commands.LOOKLEFT.value.encode())
                    else:
                        s.send(Commands.STOP.value.encode())

                #    ----控制摇臂上下转动----
                if i == 3:
                    if axis > 0.3:
                        s.send(Commands.DOWN.value.encode())
                    elif axis < -0.3:
                        s.send(Commands.UP.value.encode())
                    else:
                        s.send(Commands.STOP.value.encode())

                #    ----控制摄像头上下转动----
                if i == 4:
                    if axis > -0.8:
                        s.send(Commands.LOOKUP.value.encode())
                    else:
                        s.send(Commands.STOP.value.encode())

                if i == 5:
                    if axis > -0.8:
                        s.send(Commands.LOOKDOWN.value.encode())
                    else:
                        s.send(Commands.STOP.value.encode())

                # 控制摇臂抓取，放松


if __name__ == '__main__':

    def open_stick():
        # Open the joystick device.
        fn = '/dev/input/js0'
        js_dev = open(fn, 'rb')
        return js_dev


    def socket_connect():
        global s
        s = socket()  # 创建 socket 对象
        host = gethostname()  # 获取本地主机名
        port = 10220  # 设置端口号
        s.connect((host, port))


    sc = threading.Thread(target=socket_connect)  # Define a thread for connection
    sc.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
    sc.start()

    connect = False
    while not connect:
        try:
            js_dev = open_stick()
            if js_dev.read(8):
                connect = True
                break
        except:
            time.sleep(5)
            pass
    if connect:
        js = XboxJoyStick()
        js.run()




