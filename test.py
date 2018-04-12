#!/usr/bin/python

#=======================================================
# Program name: test_mqtt.py
# Desc: A simple test to connect a publisher MQTT
#       to a subscriber MQTT. Enter your IP address
#       in MY_IP and enter the broker IP address
#       for BROKER_IP
#
# Author: HARPi
# Date: 11.04.2018
#=======================================================

# Importing child_mqtt package
from child_mqtt import child_mqtt

NAME = "Test publisher"
<<<<<<< HEAD
TOPIC = "test/publisher"
#BROKER_IP = "<ENTER_BROKER_IP_ADDRESS>"
=======
TOPIC = "test/topic"
MY_IP = "<ENTER_YOUR_IP_ADDRESS>"
BROKER_IP = "<ENTER_BROKER_IP_ADDRESS>"
>>>>>>> 8672de61f1709c7d132febc95008a894fd6cbaf2
DESC = "A test description"

# You don't need to change this
child = child_mqtt(NAME, TOPIC, BROKER_IP, DESC)

print("My name is: %s" %child.get_name())
print("My topic is: %s" %child.get_topic())
print("My IP address: is %s" %child.get_ip())
print("I am publishing to: %s" %child.get_broker_ip())

child.send_msg("Hello other MQTT")
child.send_msg("Did you receive my message?")
child.send_msg("Disconnecting from: %s" %child.get_broker_ip())
child.disconnect()
