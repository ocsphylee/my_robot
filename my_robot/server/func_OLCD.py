# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/16 21:06
Descriptions:
'''


import mods_LCD_1in8
import mods_LCD_Config
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor



class Screen:

    def __init__(self):
        self.LCD = mods_LCD_1in8.LCD()
        Lcd_ScanDir = mods_LCD_1in8.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear(0xffff)

        # fonts
        self.cn_font15 = ImageFont.truetype('./pic/Font.ttc', size=15)
        lato_bold_italic = '/usr/share/fonts/truetype/lato/Lato-BoldItalic.ttf'
        self.en_font20 = ImageFont.truetype(lato_bold_italic, size=20)
        self.en_font15 = ImageFont.truetype(lato_bold_italic, size=15)
        self.en_font10 = ImageFont.truetype(lato_bold_italic, size=10)

        # variables
        self.ip = '等待连接...'

    def welcome(self):
        image = Image.open('./pic/welcome.bmp')
        draw = ImageDraw.Draw(image)
        now = time.strftime('%Y-%m-%d  %H:%M', time.localtime(time.time()))
        draw.text((0, 0), 'Time:', fill="black", font=self.en_font10)
        draw.text((30, 0), now, fill="black",font=self.en_font10)

        draw.text((0, 10), 'Greetings:', fill="coral", font=self.en_font20)
        draw.text((20, 30), 'Ocsphy & ', fill="coral", font=self.en_font20)
        draw.text((50, 50), 'Ronustine', fill="coral", font=self.en_font20)

        draw.text((50, 80), 'Kitten KillER', fill="red", font=self.en_font20)

        if self.ip == '等待连接...':
            draw.text((50, 103), self.ip, fill="coral", font=self.cn_font15)
        else:
            draw.text((50, 103), self.ip, fill="coral", font=self.en_font15)

        self.LCD.LCD_ShowImage(image)


if __name__ == '__main__':
    screen = Screen()
    t = 0
    while 1:
        t += 1
        screen.welcome()
        time.sleep(5)
        if t == 2:
            screen.ip = '192.168.1.108'

