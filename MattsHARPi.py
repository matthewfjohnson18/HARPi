#!/user/bin/python

############################################################################ 
# File: MattsHARPi.py
# Author: Matthew Johnson
# Description: This program uses a Raspberry Zero W to read an ADS1X15
# 	breakout board (ADC) that is converting inputs from a TMP36 
#	temperature sensor, PIR motion detector and UV sensor. It then
#	transmits the collected to another Pi via MQTT sockets through the
#	DuckDNS server.
# Last Update: 5/2/18
############################################################################

import time
import RPi.GPIO as GPIO

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Import required libraries for PIR sensor.
# import board
# import digitalio

# Create an ADS1115 ADC (16-bit) instance.
#adc = Adafruit_ADS1x15.ADS1115()

# Or create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.

# Set up GPIO pin reference mode.
GPIO.setmode(GPIO.BCM)
IN1 = 19
IN2 = 16
IN3 = 26
IN4 = 20
PIRIN = 37

cur_temp = 0
turn_on = False
turn_off = False
# user_input = ""
cur_UVI = 0
cur_PIR = 1111

# Importing child_mqtt package
from child_mqtt import child_mqtt
from time import sleep

NAME = "Matts_Node"
TOPIC1 = "Matt/Temperature"
TOPIC2 = "Matt/UVSensor"
TOPIC3 = "Matt/PIRReading"
BROKER_IP = "harpio.duckdns.org"

# Tokens can be found in child_mqtt.py
TOKEN1 = "TEMP"
TOKEN2 = "UV"
TOKEN3 = "PIR"
DESC1 = "The current temperature."
DESC2 = "The current UV index."
DESC3 = "Motion detector."

# I did change this to include multiple instances
child1 = child_mqtt(NAME, TOPIC1, BROKER_IP, TOKEN1, DESC1) 
child2 = child_mqtt(NAME, TOPIC2, BROKER_IP, TOKEN2, DESC2) 
child3 = child_mqtt(NAME, TOPIC3, BROKER_IP, TOKEN3, DESC3) 

GPIO.setwarnings(False)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
# GPIO.setup(PIRIN, GPIO.IN)

# GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN1, GPIO.LOW)

GAIN = 1

print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#print('|  TEMP  |  UVI   |  PIR   |'.format(*range(4)))
#print('-' * 37)

values = [0]*4
# Main loop.
while True:
    # Read all the ADC channel values in a list.
    
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        if i==0: # This is the port for the UV sensor and output is UV index.
            temp = adc.read_adc(i, gain=1)
            values[i] = (temp - 327)*10/17
            # print('This is working')
        if i==1:
            values[i] = adc.read_adc(i, gain=GAIN)
        if i==2:
            values[i] = adc.read_adc(i, gain=1)
        if i==3:
            values[i] = i
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 12 or 16 bit signed integer value depending on the
        # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).

    if int(values[0]) != int(cur_temp) :
	# Here is where I'll report the updated temperature.
        cur_temp = values[0]
        child1.status_msg("{:.0f}".format(cur_temp))
	# Update the stored temp to the new value
        print("The current temperature is: " + str(int(cur_temp)) + " deg C")

    if int(values[1]) != int(cur_UVI) :
        cur_UVI = values[1]
        print("The current UV index is: " + str(cur_UVI))
        child2.status_msg("{:.0f}".format(cur_UVI))
	
    if int(values[2]) != int(cur_PIR) :
        cur_PIR = values[2]
        print("The current status of the PIR is: " + str(cur_PIR))
        child3.status_msg("{:.0f}".format(cur_PIR))

    # Print the ADC values.
    # print('| {0:>6} | {1:>6} | {2:>6} |'.format(*values))

    if turn_on == True:
        GPIO.output(IN1, GPIO.LOW)
    if turn_off == True:
        GPIO.output(IN1, GPIO.HIGH)

    # If UV index is high turn relay off.
    #if values[1] > 3 :
    #    GPIO.output(IN1, GPIO.LOW)
    #if values[1] <=3 :
    #    GPIO.output(IN1, GPIO.HIGH)

    # print("Would you like to continue (y to continue)? ")
    user_input = "y" # raw_input()
    if user_input == "y" :
        turn_on = False
        #print("Continuing... ")
    else :
        print("Exiting ")
        GPIO.cleanup()
        break

    # Pause for five seconds.
    time.sleep(2)
