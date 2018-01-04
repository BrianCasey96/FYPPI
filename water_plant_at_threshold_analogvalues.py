import RPi.GPIO as GPIO
import datetime
from time import sleep
import spidev

# Establish SPI device on Bus 0,Device 0
spi = spidev.SpiDev()
spi.open(0,0)


init = False

GPIO.setmode(GPIO.BCM)
sensor = 14
GPIO.setup(sensor, GPIO.IN) 

GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.LOW)
GPIO.output(4, GPIO.HIGH)

def pump_on():
    GPIO.output(4, GPIO.LOW)
    time.sleep(1)
    GPIO.output(4, GPIO.HIGH)

def getAdc (channel):
    #check valid channel
    if ((channel>7)or(channel<0)):
        return -1
    
    #Preform SPI transaction and store returned bits in 'r'
    r = spi.xfer([1, (8+channel) << 4, 0])
    
    #Filter data bits from returned bits
    adcOut = ((r[1]&3) << 8) + r[2]
    percent = int(round(adcOut/10.24))
    
    #print out 0-1023 value and percentage
    print("ADC Output: {0:4d} Percentage: {1:3}%".format (adcOut,percent))
    return percent
    
print("Here we go!")

while True:    
    try:
        time.sleep(2)
        percent = getAdc(0)

        if percent < 60:
            pump_on()

        else:
            print("Plant watered")

    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI



