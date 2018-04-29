#!/usr/bin/python

#=======================================================
# Program name: test_mqtt.py
# Desc: A simple test to connect a publisher MQTT
#       to a subscriber MQTT. Enter your IP address
#       in MY_IP and enter the broker IP address
#       for BROKER_IP
#
# Author: HARPi
# Date: 25.04.2018
#=======================================================

# Importing child_mqtt package
from child_mqtt import child_mqtt
from time import sleep

NAME = "Test Name"
TOPIC = "test/topic"
BROKER_IP = "<ENTER_BROKER_IP_ADDRESS>"

# Tokens can be found in child_mqtt.py
TOKEN = "<ENTER_TOKEN>"
DESC = "A quick whip descript"

# You don't need to change this
child = child_mqtt(NAME, TOPIC, BROKER_IP, TOKEN, DESC)

child.send_msg("Hello other MQTT")
child.send_msg("Did you receive my message?")

print("Changing status...")
# Do not include unicode values
child.status_msg("78 *F")
child.status_msg("ON")
child.status_msg("2")
