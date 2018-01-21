#! /usr/bin/env python
from time import sleep
from gpiozero import LightSensor
import spidev
import pymysql.cursors
import os
import glob

cnx = pymysql.connect(host="sql2.freemysqlhosting.net",
                     user="sql2202637",
                     passwd="aI7%wK3%",
                     db="sql2202637")

# Establish SPI device on Bus 0,Device 0 for moisture reading
spi = spidev.SpiDev()
spi.open(0,0)

#for temperature reading
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

ldr = LightSensor(14)

def getMositureLevel(channel):
    #check valid channel
    if ((channel>7)or(channel<0)):
        return -1
    
    #Preform SPI transaction and store returned bits in 'r'
    r = spi.xfer([1, (8+channel) << 4, 0])
    
    #Filter data bits from returned bits
    adcOut = ((r[1]&3) << 8) + r[2]
    global percent
    percent = int(100- round(adcOut/10.24))
    
    #print out 0-1023 value and percentage
    print("Moisture Level: {0:4d} Mositure Percentage: {1:3}%".format (adcOut,percent))
    sleep(1)
    

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
	

def sendValues(mositure, temp, light):
    try:
        with cnx.cursor() as cursor:
            sql = "INSERT INTO Date_and_Value VALUES (null, '%d', '%lf', '%.2f')" % (mositure, temp, light)
            cursor.execute(sql)
        cnx.commit()

    finally:
        print("Values Sent")

while True:
    try:
        getMositureLevel(0)
        lightPercentage = ldr.value*100
        print("Light Level: %.2lf%%" % (lightPercentage))
        print("Temperature: %.2lf°C." % (read_temp()))
        
        sendValues(percent, read_temp(), ldr.value)
        print("\n")
        sleep(1)
        
    except KeyboardInterrupt:
        cnx.close()
##        GPIO.cleanup()






