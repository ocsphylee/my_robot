#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_1in8_LCD import LCD_1in8
from waveshare_1in8_LCD import LCD_Config

from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

def main():
    LCD = LCD_1in8.LCD()
    
    print ("**********Init LCD**********")
    Lcd_ScanDir = LCD_1in8.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
    LCD.LCD_Init(Lcd_ScanDir)
    LCD.LCD_Clear(0xffff)
    image = Image.new("RGB", (LCD.LCD_Dis_Column, LCD.LCD_Dis_Page), "WHITE")
    draw = ImageDraw.Draw(image)
    font18 = ImageFont.truetype(picdir+'/Font.ttc', 18)
    if (Lcd_ScanDir == LCD_1in8.L2R_U2D) or (Lcd_ScanDir == LCD_1in8.L2R_D2U) or (Lcd_ScanDir == LCD_1in8.R2L_U2D) or (Lcd_ScanDir == LCD_1in8.R2L_D2U) :
        print ("***draw")
        draw.line([(0,0),(127,0)], fill = "BLUE",width = 5)
        draw.line([(127,0),(127,159)], fill = "BLUE",width = 5)
        draw.line([(127,159),(0,159)], fill = "BLUE",width = 5)
        draw.line([(0,159),(0,0)], fill = "BLUE",width = 5)
        draw.rectangle([(18,10),(110,20)],fill = "RED")
        draw.rectangle((50, 85, 85, 120), outline = "Pink")
        draw.arc((55, 90, 80, 115), 0, 360, fill = 0)
        draw.line([(50,85),(85,120)], fill = "BLUE",width = 2)
        draw.line([(50,120),(85,85)], fill = "BLUE",width = 2)
        
        print ("***draw text")
        draw.text((33, 22), 'WaveShare ', fill = "purple")
        draw.text((33, 36), 'Electronic ', fill = "Orange")
        draw.text((33, 48), '1234567890', fill = "BLUE")
        draw.text((33, 62), u'微雪电子', font = font18, fill = "red")
        LCD.LCD_ShowImage(image)
        LCD_Config.Driver_Delay_ms(3000)

        draw = ImageDraw.Draw(image)
        image = Image.open(picdir+'/Himage.bmp')
        LCD.LCD_ShowImage(image)
        # LCD_Config.Driver_Delay_ms(3000)
    else:
        print ("***draw")
        draw.line([(0,0),(159,0)], fill = "BLUE",width = 5)
        draw.line([(159,0),(159,127)], fill = "BLUE",width = 5)
        draw.line([(159,127),(0,127)], fill = "BLUE",width = 5)
        draw.line([(0,127),(0,0)], fill = "BLUE",width = 5)
        draw.rectangle([(18,10),(142,20)],fill = "RED")
        
        draw.rectangle((50, 85, 85, 120), outline = "Pink")
        draw.arc((55, 90, 80, 115), 0, 360, fill = 0)
        draw.line([(50,85),(85,120)], fill = "BLUE",width = 2)
        draw.line([(50,120),(85,85)], fill = "BLUE",width = 2)
        
        print ("***draw text")
        draw.text((33, 22), 'WaveShare ', fill = "purple")
        draw.text((33, 36), 'Electronic ', fill = "Orange")
        draw.text((33, 48), '1234567890', fill = "BLUE")
        draw.text((33, 62), u'微雪电子', font = font18, fill = "red")
        LCD.LCD_ShowImage(image)
        LCD_Config.Driver_Delay_ms(3000)
        
        draw = ImageDraw.Draw(image)
        image = Image.open(picdir+'/Limage.bmp')
        LCD.LCD_ShowImage(image)
        # LCD_Config.Driver_Delay_ms(3000)
    
    # LCD.LCD_Clear(0xffff);
    #while (True):
try:
    if __name__ == '__main__':
        main()
except:
   print("except")
