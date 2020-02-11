# coding = utf-8
# /usr/bin/env/ python

'''
Author:Ocsphy
Date:2020/2/8 17:36
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


font18 = ImageFont.truetype(picdir+'/Font.ttc', 10)

while 1:
    image = Image.new("RGB", (LCD.LCD_Dis_Column, LCD.LCD_Dis_Page), "WHITE")
    draw = ImageDraw.Draw(image)
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    draw.text((0, 0), 'Time:', fill="black")
    draw.text((30, 0), now, fill="red")
    LCD.LCD_ShowImage(image)
    # time.sleep(1)