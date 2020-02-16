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


LCD = mods_LCD_1in8.LCD()

Lcd_ScanDir = mods_LCD_1in8.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
LCD.LCD_Init(Lcd_ScanDir)
LCD.LCD_Clear(0xffff)


cn_font18 = ImageFont.truetype('./pic/Font.ttc', 10)

en_font20 = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-BoldItalic.ttf', size=20)

en_font10 = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-BoldItalic.ttf', size=10)

while 1:
    image = Image.open('./pic/welcome.bmp')
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