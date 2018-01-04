import RPi.GPIO as GPIO
import datetime
import time

init = False

GPIO.setmode(GPIO.BCM)
#sensor = 14
#GPIO.setup(sensor, GPIO.IN) 

GPIO.setup(14, GPIO.OUT)
GPIO.output(14, GPIO.LOW)
GPIO.output(14, GPIO.HIGH)

def pump_on():
    GPIO.output(14, GPIO.LOW)
    time.sleep(1)
    GPIO.output(14, GPIO.HIGH)
    
print("Here we go!")

while True:    
    try:
        #time.sleep(3)
        #if GPIO.input(sensor):
        pump_on()
       # else:
        #    print("Plant watered")

    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI
