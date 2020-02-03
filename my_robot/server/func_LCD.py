# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/2 0:51
Descriptions:
'''

import LCD1602
import time

class LCD:
    def __init__(self, addr=0x27, bg=1):
        self.addr = addr
        self.bg = bg
        # init(slave address, background light)
        LCD1602.init(self.addr, self.bg)
        LCD1602.clear()

    def write(self, x, y, text):
        """
        输出屏幕
        :param x: 横坐标：[0,16]
        :param y: 纵坐标：{0,1}
        :param text: str,输出文本
        :return:
        """
        LCD1602.write(x, y, text)

    def clear(self):
        LCD1602.clear()

if __name__ == '__main__':
    lcd = LCD()
    lcd.write(0,0,'greetings')
    time.sleep(2)
    lcd.clear()