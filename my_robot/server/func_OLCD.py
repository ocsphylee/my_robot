# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/16 21:06
Descriptions:
'''

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import time
from waveshare_1in8_LCD import LCD_1in8
from waveshare_1in8_LCD import LCD_Config

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor


LCD = LCD_1in8.LCD()

Lcd_ScanDir = LCD_1in8.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
LCD.LCD_Init(Lcd_ScanDir)
LCD.LCD_Clear(0xffff)


cn_font18 = ImageFont.truetype(picdir+'/Font.ttc', 10)

en_font20 = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-BoldItalic.ttf', size=20)

en_font10 = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-BoldItalic.ttf', size=10)

while 1:
    image = Image.open(picdir+'/welcome.bmp')
    draw = ImageDraw.Draw(image)
    now = time.strftime('%Y-%m-%d  %H:%M', time.localtime(time.time()))
    draw.text((0, 0), 'Time:', fill="black", font=en_font10)
    draw.text((30, 0), now, fill="black",font=en_font10)

    draw.text((0, 10),'Greetings:', fill="coral", font=en_font20)
    draw.text((20, 30),'Ocsphy & ', fill="coral", font=en_font20)
    draw.text((50, 50),'Ronustine', fill="coral", font=en_font20)

    draw.text((50, 80),'Kitten KillER', fill="red", font=en_font20)
    draw.text((80, 103),'K.K. - 1.0', fill="red", font=en_font20)

    LCD.LCD_ShowImage(image)
    time.sleep(60)