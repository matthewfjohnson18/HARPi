#!/bin/python

#===============================================
# Program name: child_mqtt.py
# Desc: Connecting a child node to the parent
#       node. To publish a message to the 
#       parent, child node will send it with
#       send_msg() and the event handler will
#       take care of sending it to the publisher
#
# Author: HARPi
# Date: 11.04.18
#===============================================

# Imports
#===============================================
# MQTT package
import paho.mqtt.client as mqtt

# Socket package for IP address
import socket

# Time
from time import sleep

# Token
#===============================================
TOKENS = {"TEMP" : "Temperature is", "LIGHT" : "Light is", "UV" : "UV index is", "PIR" : "IR level is"}

class child_mqtt:
    def __init__(self, name, topic, broker_ip, token, desc):
        # Grab IP address
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        self.IP = sock.getsockname()[0]
        sock.close()

        # Initialize variable
        self.BROKER = str(broker_ip)
        self.PORT = 1883
        self.ALIVE = 60
        self.MQTTC = mqtt.Client()
        self.NAME = str(name)
        self.TOPIC = str(topic)
        self.DESC = str(desc)

        # Find the token
        for key, value in TOKENS.iteritems():
            if key == token:
                self.TOKEN = value

        # Create event handlers for MQTT
        self.MQTTC.on_connect = self.connect
        self.MQTTC.on_publish = self.publish

        # Setting up MQTT to a client and connecting
        self.MQTTC.connect(self.BROKER, self.PORT, self.ALIVE)

        # Bridge child node to parent node
        bridge = { "name" : self.NAME, "ip" : self.IP, "topic" : self. TOPIC, "token" : self.TOKEN, "desc" : self.DESC}
        for key, value in bridge.iteritems():
            tp = "HARPi/set_node" + key
            self.MQTTC.publish(tp, value)
            sleep(0.5)
        tp = "HARPi/set_node/complete"
        self.MQTTC.publish(tp, 1)

    # Subscribe to a topic
    def connect(self, mosq, obj, flag, rc):
        self.MQTTC.subscribe(self.TOPIC, 0)

    def publish(self, client, userdata, msg):
        return

    # Message event handler
    def send_msg(self, msg):
        tp = "HARPi/" + self.TOPIC
        self.MQTTC.publish(tp, msg)
        print("MSG sent: %s" %msg)

    def disconnect(self):
        self.MQTTC.disconnect()

    def get_name(self):
        return self.NAME

    def get_topic(self):
        return self.TOPIC

    def get_ip(self):
        return self.IP

    def get_broker_ip(self):
        return self.BROKER
