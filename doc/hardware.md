## 舵机
- 舵机控制云台的上下左右转动。
- 对于多路舵机控制，我们经常使用`PCA9685`来集成控制。在Python中，我们使用`Adafruit_PCA9685`来驱动这一模块，从而达到多路舵机控制。

```python
import RPi.GPIO as GPIO
import Adafruit_PCA9685
```

- `PCA9685`将接口转换成多路3pin的PWM接口，使得我们可以同时控制多台舵机。我们利用`Adafruit_PCA9685`中的`PCA9685`对象进行控制。

```python
# 实例化PWM对象
pwm = Adafruit_PCA9685.PCA9685()
# 设置PWM频率
pwm.set_pwm_freq(50)
# 单个舵机控制
pwm.set_pwm(channel, on, off)
# 全部舵机控制
pwm.set_all_pwm(on,off)
'''
channel: PCA9685上的接口编码
on: ? 设为0
off: ? 可能是位置
'''
```


## 电机
- 电机用于小车轮子的控制，控制小车前后左右移动。
- 电机的控制是通过集成在驱动板上的`L298P`芯片来实现的。每组电机通过三个接口控制，一个PWM接口通过改变频率和占空比来调整电机的速度。另外两个用于改变电流的方向，从而实现电机向前/向后转动。

- 以其中一组电机为例：
```python
import time
import RPi.GPIO as GPIO

# PWM接口用于调整速度
Motor_A_EN = 4
# 方向接口用于调整方向，
Motor_A_Pin1  = 26 # HIGH: 顺时针转, LOW: 逆时针转
Motor_A_Pin2  = 21 # LOW:  顺时针转, HIGH: 逆时针转
```
- 设置GPIO接口，全部设为output，其中`Motor_A_EN` 还需要设为PWM。
```python
GPIO.setmode(GPIO.BCM)
GPIO.setup(Motor_A_EN, GPIO.OUT)
GPIO.setup(Motor_A_Pin1, GPIO.OUT)
GPIO.setup(Motor_A_Pin2, GPIO.OUT)
pwm_A = GPIO.PWM(Motor_A_EN, 1000)
```

- 驱动向后
```python
speed_set = 100
GPIO.output(Motor_A_Pin1, GPIO.HIGH)
GPIO.output(Motor_A_Pin2, GPIO.LOW)
pwm_A.start(0)
pwm_A.ChangeDutyCycle(speed_set)
```

## MPU6050
- `MPU6050`姿态传感器内置陀螺仪和加速度计，可以获取三轴加速度计，三轴陀螺仪的读数。常用于移动设备的GPS定位等。

- 在Python中，可以调用`mpu6050`库来实现数据的获取。
```python
from mpu6050 import mpu6050
# 实例化
mpu = mpu6050(0x68)
# 获取自身温度
temp = mpu.get_temp()
# 读取加速度计
accel_data = mpu.get_accel_data()
# 读取陀螺仪
gyro_data = mpu.get_gyro_data()
```

- 我们还可以通过以上读数，计算x,y轴的旋转角度：
```python
import math
def dist(a,b):
    return math.sqrt((a*a) + (b*b))

# x轴旋转角度
radians_x = math.atan2(y,dist(x,z))
rotation_x = math.degrees(radians_x)

# x轴旋转角度
radians_y = math.atan2(x,dist(y,z))
rotation_y = math.degrees(radians_y)
```

- 其他用法：TODO

## 超声波
- 超声波模块通过发送并接收超声波检测物体离模块的距离。

- 超声波模块拥有一个发射头，一个接收头。我们对`TRIG`接口发送超过10us的脉冲信号，然后内部模块将发出8个40kHz的周期电平并检测回波。当接收到回波信号时，`ECHO`将对设备发出高电平信号，高电平信号的宽度（即持续时间）与所测距离成正比，具体公式：
$$
distance = (during\ time \times 340M/S) /2
$$
- Python实现
```python
import RPi.GPIO as GPIO
import time
# 设置GPIO接口
Tr = 11
Ec = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(Tr, GPIO.OUT,initial=GPIO.LOW)  # TRIG
GPIO.setup(Ec, GPIO.IN)  # ECHO

# 发出15us的脉冲信号
GPIO.output(Tr, GPIO.HIGH) 
time.sleep(0.000015)
GPIO.output(Tr, GPIO.LOW)

# 获取高电平信号持续时间
while not GPIO.input(Ec): 
    pass
t1 = time.time()
while GPIO.input(Ec): 
    pass
t2 = time.time()

# 计算距离
dist = round((t2-t1)*340/2,8)
```

## LED灯条
- LED灯条与单个LED灯的控制不同，需要集成控制从而减少GPIO口的使用。

- 在Python中，我们可以使用`rpi_ws281x`来控制LED灯条，通过`Adafruit_NeoPixel`对象的控制，可以轻易的实现RGB灯条的各种控制。

```python
import time
from rpi_ws281x import *
import random
# 灯条的设置
LED_COUNT      = 3      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# 实例化
LED = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
LED.begin()

def random_color():
    R = random.randint(0, 255)
    G = random.randint(0, 255)
    B = random.randint(0, 255)
    # rpi_ws281x中的Color()函数将RBG颜色转换成16进制的颜色
    return Color(R, G, B)

# 随机刷灯效果
while 1:
    color = random_color()
    for i in range(LED.numPixels()):
        LED.setPixelColor(i,color)
        LED.show()
        time.sleep(0.1)
    time.sleep(0.3)
```

## 循迹
- 循迹模块使用CTRT5000传感器，发射红外线，当光线遇到黑色物体，会被吸收，从而接收器收不到信号，而输出高电平，从而可以用来控制小车根据固定的轨道来行驶。

```python
import RPi.GPIO as GPIO
import time

# 设置GPIO接口，三路循迹模块
line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

# 初始化配置
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)

def loop():
    # 接收信号并打印信息
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)

    if status_middle == 1:
        print('middle sensor detected blackline')
    elif status_left == 1:
        print('left sensor detected blackline')
    elif status_right == 1:
        print('right sensor detected blackline')
    else:
        print('no sensor detected blackline')

if __name__ == '__main__':
    setup()
    while 1:
        loop()
        time.sleep(0.5)

```

## 摄像头

- 树莓派4b可以接入摄像头模块。在Python中，可以通过官方模块`Picamera`来读取图像信息，我们可以结合`OpenCv2`模块来实现实时画面展示(视频)。

```python
import picamera
from picamera.array import PiRGBArray
import cv2

# 实例化
camera = picamera.PiCamera()
# 摄像头参数设置
camera.resolution = (640, 480)
camera.framerate = 32
camera.brightness = 60

"""其他参数
camera.saturation = 80 # 设置图像视频的饱和度
camera.brightness = 50 # 设置图像的亮度(50表示白平衡的状态)
camera.shutter_speed = 6000000 # 相机快门速度
camera.iso = 800 # ISO标准实际上就是来自胶片工业的标准称谓，ISO是衡量胶片对光线敏感程度的标准。如50 ISO, 64 ISO, 100 ISO表示在曝光感应速度上要比高数值的来得慢，高数值ISO是指超过200以上的标准，如200 ISO, 400 ISO
camera.sharpness = 0 #设置图像的锐度值，默认是0，取值范围是-100~100之间
camera.framrate = 32 #这里可能用的Fraction是一个分数模块来存储分数1/6，保证分数运算的精度(记得调用模块：from fractions import Fraction) 
camera.hflip = Ture # 是否进行水平翻转 
camera.vflip = False #是否进行垂直翻转 
camera.rotation = 0 #是否对图像进行旋转 
camera.resolution = (280,160) #设置图像的width和height 
a_gain = camera.analog_gain #这个值表示摄像头传感器件到数字装换之前的模拟信号的增益，格式是Fraction的格式 一般似乎也用不上
d_gain = camera.digital_gain #这个值表示摄像头的数字增益大小 一般似乎也用不上
camera.led = False #值为False那么led为关灯的状态，True为开灯的状态
"""
# 获取图像，数组形式的
rawCapture = PiRGBArray(camera, size=(640, 480))

# 获取连续图像 camera.capture_continuous()返回无限迭代对象
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # 提取图像数组
    frame_image = frame.array
    # cv2窗口显示图像
    cv2.imshow("Frame", frame_image) 
    key = cv2.waitKey(1)
    # 清除rawCapture从而展示下一图像
    rawCapture.truncate(0)
    if key == ord("q"):
        break
```

- 我们还可以利用zmq传输，实现树莓派和PC的图像传输。我们使用Publish-Subscribe模式来实现图像传输。

  - **server 端（PC上）**
    ```python
    import cv2
    import zmq
    import base64
    import numpy as np
    import time

    # 建立zmq传输的服务端
    context = zmq.Context()
    footage_socket = context.socket(zmq.SUB)  # 选择订阅模式
    footage_socket.bind('tcp://*:5555')
    footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    while 1:
        try:
            # 接收图像（字符串格式）
            frame = footage_socket.recv_string()
            # 利用base64解码
            img = base64.b64decode(frame)
            # 利用numpy转码
            npimg = np.frombuffer(img, dtype=np.uint8)
            # 利用cv2解码
            source = cv2.imdecode(npimg, 1)

            # 显示视频窗口
            cv2.imshow("Stream", source)  
            cv2.waitKey(1)
        except:
            time.sleep(0.5)
            break
    ```

   - **Client 端（树莓派上）**
    ```python
    import picamera
    from picamera.array import PiRGBArray
    import cv2
    import zmq
    import base64

    # 获取图像
    camera = picamera.PiCamera()
    camera.resolution = (1280, 720)
    camera.framerate = 32
    camera.brightness = 60
    rawCapture = PiRGBArray(camera, size=(1280, 720))

    # 建立zmq传输的客户端
    context = zmq.Context()
    footage_socket = context.socket(zmq.PUB)
    IPinver = '192.168.1.106'
    footage_socket.connect('tcp://%s:5555'%IPinver)

    # 打开连续图像流
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame_image = frame.array
        # cv2 编码
        encoded, buffer = cv2.imencode('.jpg', frame_image)
        # base64 编码成字符串
        jpg_as_text = base64.b64encode(buffer)
        # 发送图像（字符串）
        footage_socket.send(jpg_as_text)
        # 清除图片，等待下一张
        rawCapture.truncate(0)
    ```
