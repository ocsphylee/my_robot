# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/1/31 23:38
'''

import cv2
import zmq
import base64
import numpy as np
import time

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

while 1:
    try:
        frame = footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.frombuffer(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)

        cv2.imshow("Stream", source)  # 显示视频窗口
        cv2.waitKey(1)

    except:
        time.sleep(0.5)
        break
