# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/1/31 23:48
'''

import picamera
from picamera.array import PiRGBArray
import cv2

# 获取图像
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.brightness = 60
rawCapture = PiRGBArray(camera, size=(640, 480))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame_image = frame.array
    cv2.imshow("Frame", frame_image) # 显示视频窗口
    key = cv2.waitKey(1)
    rawCapture.truncate(0)
    if key == ord("q"):
        break
