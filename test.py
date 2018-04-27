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

NAME = "Test publisher"
TOPIC = "test/publisher"
BROKER_IP = "<ENTER_BROKER_IP_ADDRESS>"

# Tokens can be found in child_mqtt.py
TOKEN = "<ENTER_TOKEN>"
DESC = "A test description"

# You don't need to change this
child = child_mqtt(NAME, TOPIC, BROKER_IP, TOKEN, DESC)

print("My name is: %s" %child.get_name())
print("My topic is: %s" %child.get_topic())
print("My IP address: is %s" %child.get_ip())
print("I am publishing to: %s" %child.get_broker_ip())

child.check_connection()
child.send_msg("Hello other MQTT")
sleep(1)
child.send_msg("Did you receive my message?")
sleep(1)
child.send_msg("Disconnecting from: %s" %child.get_broker_ip())
sleep(1)
child.disconnect()
sleep(1)
child.send_msg("Did this message go to the broker - surprise, no it didn't")
