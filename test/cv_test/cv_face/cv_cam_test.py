# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/12 13:44
Descriptions:
'''

import picamera
from picamera.array import PiRGBArray
import cv2

faceCascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalcatface_extended.xml')

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
raw_capture = PiRGBArray(camera, size=(640, 480))

for frame in camera.capture_continuous(
        raw_capture, format="bgr", use_video_port=True):

    frame_image = frame.array
    gray = cv2.cvtColor(frame_image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(20, 20)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame_image[y:y + h, x:x + w]

    cv2.imshow('video', frame_image)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break
    raw_capture.truncate(0)