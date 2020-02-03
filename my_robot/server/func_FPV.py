# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/2 15:00
Descriptions: 图像处理功能调用，图像发送
'''

import cv2
import zmq
import base64
import picamera
from picamera.array import PiRGBArray
import datetime
import mods_FPV_algorithm as FPV_func
import time
import threading

class FPV:

    def __init__(self):
        self.funcs = FPV_func.PicFunction()
        self.frame_num = 0
        self.fps = 0

    def capture_thread(self, ip_inver):
        global frame_image

        # 获取树莓派摄像头图像
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 20
        raw_capture = PiRGBArray(camera, size=(640, 480))

        # 建立zmq连接, 客户端
        context = zmq.Context()
        footage_socket = context.socket(zmq.PUB)
        print(ip_inver)
        footage_socket.connect('tcp://%s:5555' % ip_inver)

        for frame in camera.capture_continuous(
                raw_capture, format="bgr", use_video_port=True):
            frame_image = frame.array

            # 执行功能
            frame_image = self.funcs.run(frame_image)
            if frame_image is None:
                raw_capture.truncate(0)
                continue

            cv2.line(frame_image, (300, 240), (340, 240), (128, 255, 128), 1)
            cv2.line(frame_image, (320, 220), (320, 260), (128, 255, 128), 1)

            encoded, buffer = cv2.imencode('.jpg', frame_image)
            jpg_as_text = base64.b64encode(buffer)
            footage_socket.send(jpg_as_text)
            raw_capture.truncate(0)

            # 显示视频窗口(测试用）
            # cv2.imshow("Frame", frame_image)
            # key = cv2.waitKey(1)
            # raw_capture.truncate(0)

    def stop(self):
        self.funcs.stop()
        self.funcs = FPV_func.PicFunction()

if __name__ == '__main__':

    def FPV_thread():
        global fpv
        fpv = FPV()
        fpv.capture_thread(1)

    fps_threading = threading.Thread(target=FPV_thread)
    fps_threading.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
    fps_threading.start()
    time.sleep(10)

    print('find line mode')
    fpv.funcs = FPV_func.CvFindLine() # 开启功能
    time.sleep(15)
    fpv.stop()  # 结束功能

    print('motion get')
    fpv.funcs = FPV_func.MotionGet()
    time.sleep(15)
    fpv.stop()

    print('find color')
    fpv.funcs = FPV_func.FindColor()
    time.sleep(15)
    fpv.stop()
