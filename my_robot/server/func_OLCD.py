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
import func_info as info
from mods_commands import Commands


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
        self.en_font12 = ImageFont.truetype(lato_bold_italic, size=12)
        self.en_font10 = ImageFont.truetype(lato_bold_italic, size=10)

        # variables
        self.ip = '等待连接...'
        self.staus = None

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

    def panel(self):
        image = Image.new("RGB", (self.LCD.LCD_Dis_Column, self.LCD.LCD_Dis_Page), "black")
        draw = ImageDraw.Draw(image)
        now = time.strftime('%Y-%m-%d  %H:%M', time.localtime(time.time()))
        draw.text((0, 0), 'Time:', fill="white", font=self.en_font10)
        draw.text((30, 0), now, fill="white", font=self.en_font10)

        draw.line( (0, 13, 160, 13), fill='white', width=1 )
        # CPU使用
        cpu_use = info.get_cpu_use()
        draw.text((0, 15), 'CPU %: ', fill="chartreuse", font=self.en_font12)
        draw.rectangle((50, 17, int(float(cpu_use)) + 50, 27), fill="chartreuse")
        draw.text((50, 17), cpu_use, fill="darkred", font=self.en_font10)

        # RAM使用
        ram_use = info.get_ram_info()
        draw.text((0, 30), 'RAM %: ', fill="aqua", font=self.en_font12)
        draw.rectangle((50, 32, int(float(ram_use)) + 50 , 42), fill="aqua")
        draw.text((50, 32), ram_use, fill="darkred", font=self.en_font10)

        # CPU温度
        cpu_temp = info.get_cpu_tempfunc()
        draw.text((0, 45), 'CPU \'C: ', fill="lightpink", font=self.en_font12)
        draw.rectangle((50, 47, int(float(cpu_temp)) + 50, 57), fill="lightpink")
        draw.text((50, 47), cpu_temp, fill="darkred", font=self.en_font10)

        # GPU 温度
        gpu_temp = info.get_gpu_tempfunc()
        draw.text((0, 60), 'GPU \'C: ', fill="sandybrown", font=self.en_font12)
        draw.rectangle((50, 62, int(float(gpu_temp)) + 50, 72), fill="sandybrown")
        draw.text((50, 62), gpu_temp, fill="darkred", font=self.en_font10)

        draw.line((0, 76, 160, 76), fill='white', width=1)
        self.LCD.LCD_ShowImage(image)

    def run(self):
        if self.staus == Commands.WELCOME.value:
            self.welcome()
        elif self.staus == Commands.PANEL.value:
            self.panel()
        else:
            pass


if __name__ == '__main__':

    screen = Screen()
    screen.panel()

