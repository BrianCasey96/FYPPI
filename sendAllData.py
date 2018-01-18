#! /usr/bin/env python
from time import sleep
from gpiozero import LightSensor
import MySQLdb
import spidev

cnx = MySQLdb.connect(host="sql2.freemysqlhosting.net",
                      user="sql2202637",
                      passwd="aI7%wK3%",
                      db="sql2202637")

# Establish SPI device on Bus 0,Device 0
spi = spidev.SpiDev()
spi.open(0,0)

ldr = LightSensor(14)

def getAdc (channel):
    #check valid channel
    if ((channel>7)or(channel<0)):
        return -1
    
    #Preform SPI transaction and store returned bits in 'r'
    r = spi.xfer([1, (8+channel) << 4, 0])
    
    #Filter data bits from returned bits
    adcOut = ((r[1]&3) << 8) + r[2]
    global percent
    percent = int(round(adcOut/10.24))
    sendValues(percent)

    
    #print out 0-1023 value and percentage
    print("ADC Output: {0:4d} Percentage: {1:3}%".format (adcOut,percent))
    sleep(1)


def sendValues(values):
    cur = cnx.cursor()

    sql = "INSERT INTO Test(Number) VALUE ('%d' )" % (percent)
    cur.execute(sql)

    #cur.execute("INSERT INTO `Test` (`Number`) VALUE('11')")
    cnx.commit()

    cur.execute("SELECT * FROM Test")
    for row in cur.fetchall():
        print(row[0])

    cnx.close()

while True:
    getAdc(0)
    print(ldr.value)







