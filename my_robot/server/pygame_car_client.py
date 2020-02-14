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
                        # self.command = Commands.RIGHT.value
                        s.send(Commands.RIGHT.value.encode())
                    elif axis < -0.3:
                        # self.command = Commands.LEFT.value
                        s.send((Commands.LEFT.value).encode())
                    else:
                        # self.command = Commands.TS.value
                        s.send((Commands.TS.value).encode())
                if i == 1:
                    if axis > 0.3:
                        # self.command = Commands.BACKWARD.value
                        s.send((Commands.BACKWARD.value).encode())

                    elif axis < -0.3:
                        # self.command = Commands.FORWARD.value
                        s.send((Commands.FORWARD.value).encode())

                    else:
                        # self.command = Commands.DS.value
                        s.send((Commands.DS.value).encode())
                # time.sleep(0.02)

if __name__ == '__main__':

    def open_stick():
        # Open the joystick device.
        fn = '/dev/input/js0'
        js_dev = open(fn, 'rb')
        return js_dev

    def run():
        global js, connect
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


    def socket_connect():
        global s
        s = socket()  # 创建 socket 对象
        host = gethostname()  # 获取本地主机名
        port = 10220  # 设置端口号
        s.connect((host, port))


    sc = threading.Thread(target=socket_connect)  # Define a thread for connection
    sc.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
    sc.start()

    info_threading = threading.Thread(target=run)  # Define a thread for FPV and OpenCV
    info_threading.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
    info_threading.start()  # Thread starts
    time.sleep(1)

