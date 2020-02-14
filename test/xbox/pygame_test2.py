# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/14 15:46
Descriptions:
'''

import pygame

# 模块初始化
pygame.init()
pygame.joystick.init()

done = False

clock = pygame.time.Clock()

joystick_count = pygame.joystick.get_count()

while not done:
    # 遍历每一个手柄
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()

        for event_ in pygame.event.get():
            print(name)
            # 退出事件
            if event_.type == pygame.QUIT:
                done = True
            # 按键按下或弹起事件
            elif event_.type == pygame.JOYBUTTONDOWN or event_.type == pygame.JOYBUTTONUP:
                buttons = joystick.get_numbuttons()
                # 获取所有按键状态信息
                for i in range(buttons):
                    button = joystick.get_button(i)
                    print("button " + str(i) + ": " + str(button))
            # 轴转动事件
            elif event_.type == pygame.JOYAXISMOTION:
                axes = joystick.get_numaxes()
                # 获取所有轴状态信息
                for i in range(axes):
                    axis = joystick.get_axis(i)
                    print("axis " + str(i) + ": " + str(axis))
            # 方向键改变事件
            elif event_.type == pygame.JOYHATMOTION:
                hats = joystick.get_numhats()
                # 获取所有方向键状态信息
                for i in range(hats):
                    hat = joystick.get_hat(i)
                    print("hat " + str(i) + ": " + str(hat))

pygame.quit()
