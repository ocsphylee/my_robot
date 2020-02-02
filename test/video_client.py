# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/1/31 23:38
'''

import picamera
from picamera.array import PiRGBArray
import cv2
import zmq
import base64

# 获取图像
camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 32
camera.brightness = 60
rawCapture = PiRGBArray(camera, size=(1280, 720))

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
IPinver = '192.168.1.106'
footage_socket.connect('tcp://%s:5555'%IPinver)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame_image = frame.array
    encoded, buffer = cv2.imencode('.jpg', frame_image)
    jpg_as_text = base64.b64encode(buffer)
    footage_socket.send(jpg_as_text)
    rawCapture.truncate(0)
