import RPi.GPIO as GPIO
import datetime
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)
GPIO.output(17, GPIO.HIGH)

def pump_on():
    GPIO.output(17, GPIO.LOW)
    time.sleep(3)
    GPIO.output(17, GPIO.HIGH)
