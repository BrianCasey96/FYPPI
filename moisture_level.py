import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#GPIO.setmode(GPIO.BCM)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
# Software SPI configuration:
#CLK  = 11
#MISO = 9
#MOSI = 10
#CS   = 8
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
 

def reading():
    value = mcp.read_adc(0)
    percent = int(round(100-(value/10.24)))
    return value, percent 
