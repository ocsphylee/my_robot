# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/2 15:00
Descriptions: 图像处理功能的算法
'''


from mods_commands import Commands
import mods_motor as move
import cv2
from mods_LED import LED
from mods_servo import YunTai
import time
import numpy as np
import argparse
from collections import deque
import mods_switch
import datetime
import imutils


'''
---------------PID-------------
'''


class PID:
    def __init__(self):
        self.Kp = 0
        self.Kd = 0
        self.Ki = 0
        self.Initialize()

    def SetKp(self, invar):
        self.Kp = invar

    def SetKi(self, invar):
        self.Ki = invar

    def SetKd(self, invar):
        self.Kd = invar

    def SetPrevError(self, preverror):
        self.prev_error = preverror

    def Initialize(self):
        self.currtime = time.time()
        self.prevtime = self.currtime

        self.prev_error = 0

        self.Cp = 0
        self.Ci = 0
        self.Cd = 0

    def GenOut(self, error):
        self.currtime = time.time()
        dt = self.currtime - self.prevtime
        de = error - self.prev_error

        self.Cp = self.Kp * error
        self.Ci += error * dt

        self.Cd = 0
        if dt > 0:
            self.Cd = de / dt

        self.prevtime = self.currtime
        self.prev_error = error

        return self.Cp + (self.Ki * self.Ci) + (self.Kd * self.Cd)


'''
--------------setup-----------
'''

# motor
move.setup()
# PID
pid = PID()
pid.SetKp(0.5)
pid.SetKd(0)
pid.SetKi(0)
# LED
led = LED()
# yuntai
yuntai = YunTai()
yuntai.servo_init()
# swtich
switch = mods_switch.Switch()

Y_lock = 0
X_lock = 0
tor = 17
UltraData = 3


class PicFunction:

    def run(self, frame_image):
        return frame_image

    def stop(self):
        pass


class CvFindLine(PicFunction):
    """
    图像循迹
    """

    def __init__(self):
        self.frameRender = 1
        self.speed = 90
        self.lineColorSet = 255
        self.linePos_1 = 440
        self.linePos_2 = 380
        self.findLineError = 20
        self.CVrun = 1

        self.left_pos_1 = None
        self.right_pos_1 = None
        self.left_pos_2 = None
        self.right_pos_2 = None
        self.center = 320

    def find_line_ctrl(self, pos_input):
        """
        电机控制：通过控制小车移动，使线的中心和指定的点重合（在一定范围内），从而实现图像循迹。
        :param pos_input: 当前的线的中心
        :return:
        """
        if pos_input:
            if pos_input > (self.center + self.findLineError):
                # 右转
                move.motor_stop()
                error = (pos_input - self.center) / 5
                outv = int(round((pid.GenOut(error)), 0))
                move.move(Commands.NO.value, Commands.RIGHT.value, self.speed, 0.5)
                time.sleep(0.05)
                move.motor_stop()
                pass
            elif pos_input < (self.center - self.findLineError):
                # 左转
                move.motor_stop()
                error = (self.center - pos_input) / 5
                outv = int(round((pid.GenOut(error)), 0))
                move.move(Commands.NO.value, Commands.LEFT.value, self.speed, 0.5)
                time.sleep(0.05)
                move.motor_stop()
                pass
            else:
                if self.CVrun:
                    # 向前
                    move.move(
                        Commands.FORWARD.value,
                        Commands.NO.value,
                        self.speed,
                        0.5)
                pass
        else:
            if self.CVrun:
                move.motor_stop()
                move.move(
                    Commands.BACKWARD.value,
                    Commands.NO.value,
                    self.speed,
                    0.5)
            pass

    def get_center(self, line_1, line_2):
        try:
            # 计算两行中lineColorSet的像素点数量
            line_color_count_pos_1 = np.sum(line_1 == self.lineColorSet)
            line_color_count_pos_2 = np.sum(line_2 == self.lineColorSet)

            # 获取lineColorSet点的索引值
            line_index_pos_1 = np.where(line_1 == self.lineColorSet)
            line_index_pos_2 = np.where(line_2 == self.lineColorSet)

            # 为了索引不出错
            if line_color_count_pos_1 == 0:
                line_color_count_pos_1 = 1
            if line_color_count_pos_2 == 0:
                line_color_count_pos_2 = 1

            # 对于给定的这两行，取第一个和最后一个满足lineColorSet的像素点，并求均值
            self.left_pos_1 = line_index_pos_1[0][line_color_count_pos_1 - 1]
            self.right_pos_1 = line_index_pos_1[0][0]
            center_pos_1 = int((self.left_pos_1 + self.right_pos_1) / 2)

            self.left_pos_2 = line_index_pos_2[0][line_color_count_pos_2 - 1]
            self.right_pos_2 = line_index_pos_2[0][0]
            center_pos_2 = int((self.left_pos_2 + self.right_pos_2) / 2)

            # 求给定范围内的lineColorSet区域的（左右）中心
            center_pos = int((center_pos_1 + center_pos_2) / 2)
        except:
            center_pos = None
            pass

        return center_pos

    def draw_lines_text(self, img, center_pos):
        cv2.line(img, (self.left_pos_1, (self.linePos_1 + 30)),
                 (self.left_pos_1, (self.linePos_1 - 30)), (255, 128, 64), 1)
        cv2.line(img, (self.right_pos_1, (self.linePos_1 + 30)),
                 (self.right_pos_1, (self.linePos_1 - 30)), (64, 128, 255), )
        cv2.line(img, (0, self.linePos_1),
                 (640, self.linePos_1), (255, 255, 64), 1)

        cv2.line(img, (self.left_pos_2, (self.linePos_2 + 30)),
                 (self.left_pos_2, (self.linePos_2 - 30)), (255, 128, 64), 1)
        cv2.line(img, (self.right_pos_2, (self.linePos_2 + 30)),
                 (self.right_pos_2, (self.linePos_2 - 30)), (64, 128, 255), 1)
        cv2.line(img, (0, self.linePos_2),
                 (640, self.linePos_2), (255, 255, 64), 1)

        cv2.line(img, ((center_pos - 20), int((self.linePos_1 + self.linePos_2) / 2)),
                 ((center_pos + 20), int((self.linePos_1 + self.linePos_2) / 2)), (0, 0, 0), 1)
        cv2.line(img, (center_pos, int((self.linePos_1 + self.linePos_2) / 2 + 20)),
                 (center_pos, int((self.linePos_1 + self.linePos_2) / 2 - 20)), (0, 0, 0), 1)

        if self.lineColorSet == 255:
            cv2.putText(img, 'Following White Line', (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (128, 255, 128), 1, cv2.LINE_AA)

        else:
            cv2.putText(img, 'Following Black Line', (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (128, 255, 128), 1, cv2.LINE_AA)

    def run(self, frame_image):
        """
        执行CVFindline命令
        """
        global frame_findline
        # 转成灰度
        frame_findline = cv2.cvtColor(frame_image, cv2.COLOR_BGR2GRAY)
        # 用大津算法转成二值图像
        retval, frame_findline = cv2.threshold(
            frame_findline, 0, 255, cv2.THRESH_OTSU)
        # 侵蚀：用于降噪
        frame_findline = cv2.erode(frame_findline, None, iterations=6)
        # 取指定两行
        color_pos_1 = frame_findline[self.linePos_1]
        color_pos_2 = frame_findline[self.linePos_2]

        center_pos = self.get_center(color_pos_1, color_pos_2)

        self.find_line_ctrl(center_pos)

        # 画线和文字，返回图片
        if self.frameRender:
            try:
                self.draw_lines_text(frame_image, center_pos)
            except :
                pass
            finally:
                return frame_image

        else:
            try:
                self.draw_lines_text(frame_findline, center_pos)
            except :
                pass
            finally:
                return frame_findline

    def stop(self):
        move.motor_stop()


class FindColor(PicFunction):

    def __init__(self):
        self.colorUpper = (44, 255, 255)
        self.colorLower = (24, 100, 100)

    def run(self, frame_image):
        ap = argparse.ArgumentParser()  # OpenCV initialization
        ap.add_argument("-b", "--buffer", type=int, default=64,
                        help="max buffer size")
        args = vars(ap.parse_args())
        pts = deque(maxlen=args["buffer"])

        font = cv2.FONT_HERSHEY_SIMPLEX
        # 启动颜色追踪
        ####>>>OpenCV Start<<<####
        hsv = cv2.cvtColor(frame_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            cv2.putText(frame_image, 'Target Detected', (40, 60),
                        font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            X = int(x)
            Y = int(y)
            if radius > 10:
                cv2.rectangle(frame_image, (int(x - radius), int(y + radius)),
                              (int(x + radius), int(y - radius)), (255, 255, 255), 1)

            if Y < (240 - tor):
                error = (240 - Y) / 5
                outv = int(round((pid.GenOut(error)), 0))
                yuntai.servo_turn(Commands.LOOKUP.value, servo_speed=outv)
                Y_lock = 0
            elif Y > (240 + tor):
                error = (Y - 240) / 5
                outv = int(round((pid.GenOut(error)), 0))
                yuntai.servo_turn(Commands.LOOKDOWN.value, servo_speed=outv)
                Y_lock = 0
            else:
                Y_lock = 1

            if X < (320 - tor * 3):
                error = (320 - X) / 5
                outv = int(round((pid.GenOut(error)), 0))
                yuntai.servo_turn(Commands.LOOKLEFT.value, servo_speed=outv)
                # move.move(70, 'no', 'left', 0.6)
                X_lock = 0
            elif X > (330 + tor * 3):
                error = (X - 240) / 5
                outv = int(round((pid.GenOut(error)), 0))
                yuntai.servo_turn(Commands.LOOKRIGHT.value, servo_speed=outv)
                # move.move(70, 'no', 'right', 0.6)
                X_lock = 0
            else:
                # move.motorStop()
                X_lock = 1

            if X_lock == 1 and Y_lock == 1:
                switch.set_all_switch_on()
            else:
                switch.set_all_switch_off()

        else:
            cv2.putText(frame_image, 'Target Detecting', (40, 60),
                        font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            move.motor_stop()

        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame_image, pts[i - 1], pts[i], (0, 0, 255), thickness)

        return frame_image
    ####>>>OpenCV Ends<<<####

    def stop(self):
        move.motor_stop()
        yuntai.servo_init()
        switch.set_all_switch_off()


class MotionGet(PicFunction):
    def __init__(self):
        self.avg = None
        self.motionCounter = 0
        # time.sleep(4)
        self.lastMovtionCaptured = datetime.datetime.now()
        self.timestamp = datetime.datetime.now()

    def run(self, frame_image):

        # 动作捕获
        gray = cv2.cvtColor(frame_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.avg is None:
            print("[INFO] starting background model...")
            self.avg = gray.copy().astype("float")
            return None
            # TODO rawCapture.truncate(0)
            # 					continue

        cv2.accumulateWeighted(gray, self.avg, 0.5)
        frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))

        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frame_delta, 5, 255,
                               cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # print('x')
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 5000:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(
                frame_image, (x, y), (x + w, y + h), (128, 255, 0), 1)
            text = "Occupied"
            self.motionCounter += 1

            led.color_wipe(255, 16, 0)
            self.lastMovtionCaptured = self.timestamp
            switch.set_all_switch_on()

        if (self.timestamp - self.lastMovtionCaptured).seconds >= 0.5:
            led.color_wipe(255, 255, 0)
            switch.set_all_switch_off()

        return frame_image

    def stop(self):
        led.color_wipe(0, 0, 0)
        switch.set_all_switch_off()
