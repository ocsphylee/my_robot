# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/1/31 17:59
'''

from mpu6050 import mpu6050
import time
import numpy as np

mpu = mpu6050(0x68)
while True:

    # print(mpu.get_temp())
    accel_data = mpu.get_accel_data(g=True)
    ang = np.degrees(np.arccos(accel_data['z']-1))
    print('x: {:.4f} , y: {:.4f} , z: {:.4f} , ang: {:.4f}'.format(accel_data['x'],accel_data['y'],accel_data['z'],ang))
    # print(accel_data['y'])
    # print(accel_data['z'])
    # gyro_data = mpu.get_gyro_data()
    # print(gyro_data['x'])
    # print(gyro_data['y'])
    # print(gyro_data['z'])
    time.sleep(0.5)