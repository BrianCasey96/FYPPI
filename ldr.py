import time
from gpiozero import LightSensor, Buzzer

ldr = LightSensor(14) 
while True:
    print(ldr.value)
    if ldr.value > .3:
   	print("light")
    else:
	print("covered")
    print("--------")
    time.sleep(0.5)
