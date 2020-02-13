# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/12 15:13
Descriptions:
'''

import picamera
from picamera.array import PiRGBArray
import cv2
import numpy as np
import os


# 读取训练好的模型和分类器
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = 'haarcascades/haarcascade_frontalcatface_extended.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)

# 设置显示字体
font = cv2.FONT_HERSHEY_SIMPLEX

# 初始ID
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'DaYe', 'ErYe']

# 获取图像
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
raw_capture = PiRGBArray(camera, size=(640, 480))


for frame in camera.capture_continuous(
        raw_capture, format="bgr", use_video_port=True):

    # 获取图片
    frame_image = frame.array
    # 转成灰度
    gray = cv2.cvtColor(frame_image, cv2.COLOR_BGR2GRAY)
    # 识别出人脸
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20),
        )

    # 标出人脸
    for (x, y, w, h) in faces:
        cv2.rectangle(frame_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # 向模型传入人脸，返回预测值
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        # 显示id对应的名字和匹配度
        cv2.putText(frame_image, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(frame_image, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', frame_image)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break
    raw_capture.truncate(0)

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")


