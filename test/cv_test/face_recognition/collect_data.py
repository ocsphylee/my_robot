# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/12 14:46
Descriptions:
'''

import picamera
from picamera.array import PiRGBArray
import cv2
import os


# 输入采集样本的数量和目标样本的id
max_count = int(input('\n enter number of samples end press <return> ==>  '))
face_id = input('\n enter user id end press <return> ==>  ')

# -----开始采集----
print("\n [INFO] Initializing face capture. Look the camera and wait ...")

# 生成Haar分类器
cascadePath = 'haarcascades/haarcascade_frontalcatface_extended.xml'
face_detector = cv2.CascadeClassifier(cascadePath)

# 用Picam采集图像
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
raw_capture = PiRGBArray(camera, size=(640, 480))

# 设置样本数量标记
count = 0

for frame in camera.capture_continuous(
        raw_capture, format="bgr", use_video_port=True):
    # 获取图片
    frame_image = frame.array
    # 转成灰度
    gray = cv2.cvtColor(frame_image, cv2.COLOR_BGR2GRAY)
    # 人脸识别
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,  # 图像缩小的比例
        minNeighbors=5,  # 每个目标至少被检测到5次
        minSize=(20, 20)  # 最小的检测目标尺寸
        )

    # 用矩形标记人脸
    for (x, y, w, h) in faces:
        cv2.rectangle(frame_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1

        # 保存图像
        cv2.imwrite("./dataset/User.{}.{}.jpg".format(face_id, count), gray[y:y + h, x:x + w])

    cv2.imshow('image', frame_image)

    k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= max_count:  # Take 30 face sample and stop video
        break
    raw_capture.truncate(0)

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
