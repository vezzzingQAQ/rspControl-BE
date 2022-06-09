from django.http import JsonResponse
from django.shortcuts import render
import RPi.GPIO as GPIO
import time
from public.public import JWTSALT
from public.public import err_obj
from rpi_ws281x import PixelStrip, Color

SINGLE_LED_PIN = 26
SINGLE_LED_PWM = None

R_LED_PIN = 16
G_LED_PIN = 20
B_LED_PIN = 21
R_LED_PWM = None
G_LED_PWM = None
B_LED_PWM = None

GPIO.setmode(GPIO.BCM)

GPIO.setup(SINGLE_LED_PIN, GPIO.OUT)
SINGLE_LED_PWM = GPIO.PWM(SINGLE_LED_PIN, 50)
SINGLE_LED_PWM.start(0)

GPIO.setup(R_LED_PIN, GPIO.OUT)
R_LED_PWM = GPIO.PWM(R_LED_PIN, 50)
R_LED_PWM.start(0)

GPIO.setup(G_LED_PIN, GPIO.OUT)
G_LED_PWM = GPIO.PWM(G_LED_PIN, 50)
G_LED_PWM.start(0)

GPIO.setup(B_LED_PIN, GPIO.OUT)
B_LED_PWM = GPIO.PWM(B_LED_PIN, 50)
B_LED_PWM.start(0)

WS_LED_PIN = 18
WS_LED_COUNT = 16
WS_LED_PIN = 18
WS_LED_FREQ_HZ = 800000
WS_LED_DMA = 10
WS_LED_BRIGHTNESS = 255
WS_LED_INVERT = False
WS_LED_CHANNEL = 0

STRIP = PixelStrip(WS_LED_COUNT, WS_LED_PIN, WS_LED_FREQ_HZ, WS_LED_DMA,
                   WS_LED_INVERT, WS_LED_BRIGHTNESS, WS_LED_CHANNEL)
STRIP.begin()


def setBrightness(request):
    global SINGLE_LED_PWM, SINGLE_LED_PIN
    # 控制LED亮度
    try:
        brightness = request.GET.get("brightness")
        print(brightness)
        SINGLE_LED_PWM.ChangeDutyCycle(float(brightness))
        return JsonResponse({"status": 1})
    except:
        return JsonResponse(err_obj)


def setRGBLED(request):
    global R_LED_PWM, G_LED_PWM, B_LED_PWM, R_LED_PIN, G_LED_PIN, B_LED_PIN
    # 控制RGBLED颜色
    try:
        r = int(request.GET.get("r"))/255*100
        g = int(request.GET.get("g"))/255*100
        b = int(request.GET.get("b"))/255*100
        R_LED_PWM.ChangeDutyCycle(float(r))
        G_LED_PWM.ChangeDutyCycle(float(g))
        B_LED_PWM.ChangeDutyCycle(float(b))
        return JsonResponse({"status": 1})
    except:
        return JsonResponse(err_obj)


def clearGPIO(request):
    global SINGLE_LED_PWM
    # 清除GPIO资源和PWM
    if SINGLE_LED_PWM != None:
        SINGLE_LED_PWM.stop()
        SINGLE_LED_PWM = None
    GPIO.cleanup()
    return JsonResponse({"status": 1})


def setWS2812(request):
    global STRIP
    # 控制WS2812灯
    try:
        r = int(request.GET.get("r"))
        g = int(request.GET.get("g"))
        b = int(request.GET.get("b"))
        index = int(request.GET.get("index"))
        STRIP.setPixelColor(int(index), Color(int(r), int(g), int(b)))
        STRIP.show()
        return JsonResponse({"status": 1})
    except:
        return JsonResponse(err_obj)
