import RPi.GPIO as GPIO 
import time

GPIO.setmode(GPIO.BCM)
sensor = 17

GPIO.setup(sensor, GPIO.IN)

while True:
	if GPIO.input(sensor):
	    print ('LED Off on sensor')
	else:
	    print ('LED On on sensor')

	time.sleep(1)
