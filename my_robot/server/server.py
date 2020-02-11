# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/3 0:04
Descriptions: 机器人服务端，在Pi上
'''

import socket
import threading
import os
import time

from mods_LED import LED
from func_LCD import LCD
from mods_servo import YunTai
from func_FPV import FPV
import mods_motor as move
import func_info as info
from mods_switch import Switch
from mods_commands import Commands
from func_scan import radar_scan
import mods_FPV_algorithm as FPV_func
from func_tracking import TrackingMove
from func_auto_move import AutoMove

def ap_thread():
    os.system("sudo create_ap wlan0 eth0 Groovy 12345678")


def wifi_check():
    """
    检测wifi连接
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        ipaddr_check = s.getsockname()[0]
        s.close()
        # screen.clear()
        # screen.write(0, 0, 'Find Me Here:')
        # screen.write(1, 1, ipaddr_check)
    except:
        # Define a thread for data receiving
        ap_threading = threading.Thread(target=ap_thread)
        # 'True' means it is a front thread,it would close when the mainloop() closes
        ap_threading.setDaemon(True)
        ap_threading.start()  # Thread starts
        led.celebrate()
        # screen.clear()
        # screen.write(0, 0, 'WiFi Created:')
        # screen.write(1, 1, 'Groovy  12345678')


def build_server(PORT=10223):
    # 设置地址
    HOST = ''
    ADDR = (HOST, PORT)

    # 建立网络连接，等待客户端连接。
    tcp_ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ser_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_ser_sock.bind(ADDR)
    tcp_ser_sock.listen(5)  # Start server,waiting for client
    print('waiting for connection...')
    tcp_cli_sock, addr = tcp_ser_sock.accept()
    print('...connected from :', addr)

    # screen.clear()
    # screen.write(0, 0, 'connected from :')
    # screen.write(1, 1, addr[0])
    return tcp_cli_sock, addr


def FPV_thread():
    global fpv
    fpv = FPV()
    fpv.capture_thread(addr[0])


def info_send_client():
    server_ip = addr[0]
    server_port = 2256  # Define port serial
    server_addr = (server_ip, server_port)
    # Set connection value for socket
    info_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    info_socket.connect(server_addr)
    print(server_addr)
    while True:
        try:
            info_socket.send((info.get_cpu_tempfunc() +
                              ' ' +
                              info.get_cpu_use() +
                              ' ' +
                              info.get_ram_info() +
                              ' ' +
                              str(yuntai.get_direction())).encode())
            time.sleep(1)
        except:
            time.sleep(10)
            pass


class ContinousDetect(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(ContinousDetect, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
        # 实例化功能对象
        self.tracking = TrackingMove()
        self.auto = AutoMove()
        self.yuntai_commands = [Commands.LOOKLEFT.value, Commands.LOOKRIGHT.value,
                                Commands.UP.value, Commands.DOWN.value,
                                Commands.LOOKUP.value, Commands.LOOKDOWN.value,
                                Commands.GRAB.value, Commands.LOOSE.value]

    def run(self):
        global current_command, servo_command, motor_speed
        motor_speed = 100
        servo_command = Commands.STOP.value
        current_command = None
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回

            if servo_command in self.yuntai_commands:
                yuntai.servo_turn(servo_command, servo_speed=servo_speed)

            elif servo_command == Commands.STOP.value:
                pass

            # -------红外循迹---------
            if current_command == Commands.FUNCTION_4_ON.value:
                self.tracking.run(motor_speed)
                if current_command == Commands.FUNCTION_4_OFF.value:
                    self.tracking.stop()

            # -------自动模式---------
            elif current_command == Commands.FUNCTION_5_ON.value:
                self.auto.run(motor_speed)
                if current_command == Commands.FUNCTION_5_OFF.value:
                    self.auto.stop()

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞
        # time.sleep(0.5)
        self.tracking.stop()
        self.auto.stop()


    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False

def execute_commands(bufsiz=1024):
    global current_command, servo_command, motor_speed
    # motor方向
    direction_command = 'no'
    turn_command = 'no'
    motor_speed = 100
    motor_radius = 1

    continous_detect = ContinousDetect()
    continous_detect.start()
    continous_detect.pause()

    while True:

        data = str(tcp_cli_sock.recv(bufsiz).decode())
        if not data:
            continue

        # --------------------小车移动控制----------------------
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

            # ----------------小车速度控制-----------------------
        elif Commands.WSB.value in data:
            try:
                set_b = data.split()
                motor_speed = int(set_b[1])
            except:
                pass

        # --------------------开关按钮控制----------------------

        elif Commands.SWITCH_1_ON.value in data:
            switch.switch_ctrl(switch.PORT1, Commands.ON.value)
            tcp_cli_sock.send(Commands.SWITCH_1_ON.value.encode())

        elif Commands.SWITCH_1_OFF.value in data:
            switch.switch_ctrl(switch.PORT1, Commands.OFF.value)
            tcp_cli_sock.send(Commands.SWITCH_1_OFF.value.encode())

        elif Commands.SWITCH_2_ON.value in data:
            switch.switch_ctrl(switch.PORT2, Commands.ON.value)
            tcp_cli_sock.send(Commands.SWITCH_2_ON.value.encode())

        elif Commands.SWITCH_2_OFF.value in data:
            switch.switch_ctrl(switch.PORT2, Commands.OFF.value)
            tcp_cli_sock.send(Commands.SWITCH_2_OFF.value.encode())

        elif Commands.SWITCH_3_ON.value in data:
            switch.switch_ctrl(switch.PORT3, Commands.ON.value)
            tcp_cli_sock.send(Commands.SWITCH_3_ON.value.encode())

        elif Commands.SWITCH_3_OFF.value in data:
            switch.switch_ctrl(switch.PORT3, Commands.OFF.value)
            tcp_cli_sock.send(Commands.SWITCH_3_OFF.value.encode())

        # --------------------云台控制----------------------
        elif data in continous_detect.yuntai_commands:
            servo_command = data
            continous_detect.resume()

        elif Commands.STOP.value == data:
            servo_command = Commands.STOP.value

        elif Commands.HOME.value == data:
            yuntai.ahead()

        # --------------------功能按钮----------------------
        #      --------------超声波扫描----------------
        elif Commands.FUNCTION_1_ON.value in data:
            tcp_cli_sock.send(Commands.FUNCTION_1_ON.value.encode())
            radar_send = radar_scan()
            tcp_cli_sock.sendall(radar_send.encode())
            time.sleep(0.3)
            tcp_cli_sock.send(Commands.FUNCTION_1_OFF.value.encode())

        #      --------------颜色追踪----------------
        elif Commands.FUNCTION_2_ON.value in data:
            fpv.funcs = FPV_func.FindColor()
            tcp_cli_sock.send(Commands.FUNCTION_2_ON.value.encode())

        elif Commands.FUNCTION_2_OFF.value in data:
            fpv.stop()
            switch.set_all_switch_off()
            tcp_cli_sock.send(Commands.FUNCTION_2_OFF.value.encode())

        #      --------------动作捕获----------------
        elif Commands.FUNCTION_3_ON.value in data:
            fpv.funcs = FPV_func.MotionGet()
            tcp_cli_sock.send(Commands.FUNCTION_3_ON.value.encode())

        elif Commands.FUNCTION_3_OFF.value in data:
            fpv.stop()
            tcp_cli_sock.send(Commands.FUNCTION_3_OFF.value.encode())

        #      --------------红外循迹----------------
        elif Commands.FUNCTION_4_ON.value in data:
            current_command = Commands.FUNCTION_4_ON.value
            continous_detect.resume()
            tcp_cli_sock.send(Commands.FUNCTION_4_ON.value.encode())

        elif Commands.FUNCTION_4_OFF.value in data:
            current_command = Commands.FUNCTION_4_OFF.value
            continous_detect.pause()
            tcp_cli_sock.send(Commands.FUNCTION_4_OFF.value.encode())

        #      --------------自动模式----------------
        elif Commands.FUNCTION_5_ON.value in data:
            current_command = Commands.FUNCTION_5_ON.value
            continous_detect.resume()
            tcp_cli_sock.send(Commands.FUNCTION_5_ON.value.encode())

        elif Commands.FUNCTION_5_OFF.value in data:
            current_command = Commands.FUNCTION_5_OFF.value
            continous_detect.pause()
            tcp_cli_sock.send(Commands.FUNCTION_5_OFF.value.encode())

        # ------------------图像循迹--------------------------------
        elif Commands.CVFL_ON.value in data:
            fpv.funcs = FPV_func.CvFindLine()
            tcp_cli_sock.send(Commands.CVFL_ON.value.encode())

        elif Commands.CVFL_OFF.value in data:
            fpv.stop()
            tcp_cli_sock.send(Commands.CVFL_OFF.value.encode())

        #   --------灰度图片---------
        elif Commands.RENDER.value in data:
            try:
                if fpv.funcs.frameRender:
                    fpv.funcs.frameRender = 0
                else:
                    fpv.funcs.frameRender = 1
            except:
                pass

        #  ---------切换颜色-------------
        elif Commands.WBSWITCH.value in data:
            try:
                if fpv.funcs.lineColorSet == 255:
                    fpv.funcs.lineColorSet = 0
                else:
                    fpv.funcs.lineColorSet = 255
            except:
                pass

        elif Commands.LIP1.value in data:
            try:
                set_lip1 = data.split()
                lip1_set = int(set_lip1[1])
                fpv.funcs.linePos_1 = lip1_set
            except:
                pass

        elif Commands.LIP2.value in data:
            try:
                set_lip2 = data.split()
                lip2_set = int(set_lip2[1])
                fpv.funcs.linePos_2 = lip2_set
            except:
                pass

        elif Commands.ERR.value in data:
            try:
                set_err = data.split()
                err_set = int(set_err[1])
                fpv.funcs.findLineError = err_set
            except:
                pass

        else:
            pass

        print(data)



if __name__ == '__main__':

    '''
    ---------------------初始化设置-------------------
    '''
    # 实例化云台对象
    yuntai = YunTai()
    yuntai.servo_init()
    servo_speed = 1

    # 实例化Port，关闭
    switch = Switch()
    switch.set_all_switch_off()

    # 实例化屏幕对象
    # screen = LCD()
    # screen.clear()
    # screen.write(0, 0, 'Greetings!!')
    # screen.write(4, 1, 'OCSPHY')
    # time.sleep(3)
    # screen.clear()
    # screen.write(0, 0, 'Starting Robot..')

    try:
        # 实例化LED对象，并设置颜色
        led = LED()
        led.color_wipe(255, 16, 0)
    except BaseException:
        print('Use "sudo pip3 install rpi_ws281x" to install WS_281x package')
        pass

    '''
    --------------------WiFi检测，启动服务器------
    '''
    # WiFi检测，屏幕打印IP地址/热点
    wifi_check()
    tcp_cli_sock, addr = build_server(PORT=10223)

    '''
    --------------------创建线程，等待指令-------------
    '''

    # 建立图像处理的线程, 创建视频流，等待图像处理相关指令
    # Define a thread for FPV and OpenCV
    fps_threading = threading.Thread(target=FPV_thread)
    # 'True' means it is a front thread,it would close when the mainloop() closes
    fps_threading.setDaemon(True)
    fps_threading.start()  # Thread starts

    # 建立线程，发送CPU信息
    info_threading = threading.Thread(target=info_send_client)  # Define a thread for FPV and OpenCV
    info_threading.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
    info_threading.start()  # Thread starts

    '''
    ---------------------接收指令，执行指令-----------------
    '''
    execute_commands(bufsiz=1024)