# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/14 17:04
Descriptions:
'''

from mods_commands import Commands
import threading
import mods_motor as move
import socket


# 设置地址
HOST = ''
PORT = 10220
ADDR = (HOST, PORT)

# 建立网络连接，等待客户端连接。
tcp_ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_ser_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_ser_sock.bind(ADDR)
tcp_ser_sock.listen(5)  # Start server,waiting for client
print('waiting for connection...')
tcp_cli_sock, addr = tcp_ser_sock.accept()
print('...connected from :', addr)


direction_command = 'no'
turn_command = 'no'
motor_speed = 100
motor_radius = 1
bufsiz=1024

move.setup()
while 1:

    data = str(tcp_cli_sock.recv(bufsiz).decode())
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
else:
    pass