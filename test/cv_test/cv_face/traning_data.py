# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/12 15:11
Descriptions:
'''

import numpy as np
from PIL import Image
import os
import cv2


# 从文件夹获取样本和标签
def get_img_label(path):
    # 遍历路径下的所有文件
    # ToDO: 改成遍历路径下的所有图片文件
    img_path = [os.path.join(path, f) for f in os.listdir(path)]

    face_samples = []
    ids = []
    for imagePath in img_path:
        # 用PIL.Image打开并转成灰度，numpy转成数组图片，
        PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')

        # 获取id和脸部图片
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        cascadePath = 'haarcascades/haarcascade_frontalcatface_extended.xml'
        detector = cv2.CascadeClassifier(cascadePath)
        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            # 提取脸部图片
            face_samples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)
    return face_samples, ids


# 开始训练
print("\n [INFO] Training faces. It will take a few seconds. Wait ...")

# 生成训练器
recognizer = cv2.face.LBPHFaceRecognizer_create()

# 获取图片和id
path = 'dataset'
faces, ids = get_img_label(path)

# 训练
recognizer.train(faces, np.array(ids))

# 保存训练模型 trainer/trainer.yml
recognizer.write('trainer/trainer.yml')  # recognizer.save() worked on Mac, but not on Pi

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))