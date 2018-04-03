#! /usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
from gpiozero import LightSensor
import pymysql.cursors
import os
import sys
import glob
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

import temp
import moisture_level
import water

user = config.user()
passwd = config.returnPassword()
db = config.db()

#subprocess.call(['./cloudproxy.sh'])

#os.system('cd Code/FYPPI/')
os.system('./cloudproxy.sh')
sleep(3)

def connectionStatus(client, userdata, flags, rc):
       mqttClient.subscribe("rpi/gpio")

clientName = "RPI"
serverAddress = "35.198.67.227"

cnx = pymysql.connect(host="127.0.0.1",
		      user=user,
		      passwd=passwd,
		      db=db,
		      port = 3307 )

##for water pump
GPIO.setmode(GPIO.BCM)

global percent
global adc_output
adc_output, percent = moisture_level.reading()

ldr = LightSensor(14)

def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    print(message) 
    if message == "on":
           print("on")
           water.pump_on() #pump water
	   sleep(2)
	   sendValues(percent, temp.read_temp(), lightPercentage)
	   print("Values Updated after plant watered")
	#send conformation back and swift update itself

    else:
           print("Unknown message!")

def sendValues(mositure, temp, light):
     try:
        with cnx.cursor() as cursor:
           sql = "INSERT INTO pidata VALUES (null, '%d', '%lf', '%f')" % (mositure, temp, light)
           cursor.execute(sql)
        cnx.commit()

     finally:
        print("Values Sent")
#  query.Query("INSERT INTO pidata VALUES (null, '%d', '%lf', '%f')" % (mositure, temp, light))

mqttClient = mqtt.Client(clientName)

mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

mqttClient.connect(serverAddress)
##mqttClient.loop_forever()
mqttClient.loop_start()

def main():
#    try:
     while 1==1:
     	print("ADC Output: {0:4d} Percentage: {1:3}%".format (adc_output,percent))
	global lightPercentage
     	lightPercentage = ldr.value*100
     	print("Light Level: %.2lf%%" % (lightPercentage))
     	print("Temperature: %.2lf°C." % (temp.read_temp()))
     	sendValues(percent, temp.read_temp(), lightPercentage)
     	print("\n")
     	sleep(300)

##        if percent < 60:
##            water.pump_on()

##        else:
##            print("Plant already watered")

 #   except KeyboardInterrupt:
  #      cnx.close()
   #     GPIO.cleanup()
if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()
