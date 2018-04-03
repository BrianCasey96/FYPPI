#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio

def connectionStatus(client, userdata, flags, rc):
        mqttClient.subscribe("rpi/gpio")

def messageDecoder(client, userdata, msg):
        message = msg.payload.decode(encoding='UTF-8')
        print(message) 
        if message == "on":
       		 print("on")
        else:
                print("Unknown message!")

clientName = "RPI"
serverAddress = "35.198.67.227"
#port = 8080
mqttClient = mqtt.Client(clientName)

mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

mqttClient.connect(serverAddress)
mqttClient.loop_forever()
