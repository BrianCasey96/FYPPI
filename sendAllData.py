#! /usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
from gpiozero import LightSensor
import spidev
import pymysql.cursors
import os
import glob
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import paho.mqtt.client as mqtt

def connectionStatus(client, userdata, flags, rc):
        mqttClient.subscribe("rpi/gpio")

clientName = "RPI"
serverAddress = "35.198.67.227"
cnx = pymysql.connect(host="35.205.189.63",
		      user="root",
		      passwd="butterfly",
		      db="plant_data")
##for water pump
init = False

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)
GPIO.output(17, GPIO.HIGH)

# Establish SPI device on Bus 0,Device 0 for moisture reading
##spi = spidev.SpiDev()
##spi.open(0,0)

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
#for temperature reading
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

ldr = LightSensor(14)

def pump_on():
    GPIO.output(17, GPIO.LOW)
    sleep(3)
    GPIO.output(17, GPIO.HIGH)


def messageDecoder(client, userdata, msg):
        message = msg.payload.decode(encoding='UTF-8')
        print(message) 
        if message == "on":
                 print("on")
		 pump_on()
        else:
                print("Unknown message!")

def getMositureLevel(channel):
    #check valid channel
    if ((channel>7)or(channel<0)):
        return -1
    
    #Preform SPI transaction and store returned bits in 'r'
   # r = spi.xfer([1, (8+channel) << 4, 0])
    
    #Filter data bits from returned bits
    value = mcp.read_adc(0)
   # adcOut = ((r[1]&3) << 8) + r[2]
    global percent
    percent = int(100- round(value/10.24)) 
    #print out 0-1023 value and percentage
    print("Moisture Level: {0:4d}  Mositure Percentage: {1:3}%".format (value,percent))
##    sleep(1)


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
            sql = "INSERT INTO pidata VALUES (null, '%d', '%lf', '%f')" % (mositure, temp, light)
            cursor.execute(sql)
        cnx.commit()

    finally:
        print("Values Sent")

mqttClient = mqtt.Client(clientName)

mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

mqttClient.connect(serverAddress)
#mqttClient.loop_forever()
mqttClient.loop_start()

while True:
    try:
        getMositureLevel(0)
        lightPercentage = ldr.value*100
        print("Light Level: %.2lf%%" % (lightPercentage))
        print("Temperature: %.2lf°C." % (read_temp()))
        sendValues(percent, read_temp(), lightPercentage)
        print("\n")
        sleep(4)
        
##        if percent < 60:
##            pump_on()

##        else:
##            print("Plant already watered")
        
    except KeyboardInterrupt:
        cnx.close()
##        GPIO.cleanup()






