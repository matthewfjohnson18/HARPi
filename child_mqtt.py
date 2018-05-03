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

# global_var.py
from global_var import Global_Var

# Token
#===============================================
TOKENS = {"TEMP" : "Temperature is ", "LIGHT" : "Light is ", "UV" : "UV index is ", "PIR" : "IR level is "}

class child_mqtt:
    def __init__(self, name, topic, broker_ip, token, desc):
        # Grab IP address
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        self.IP = sock.getsockname()[0]
        sock.close()

        # Create object of global_variables
        self.gv = Global_Var()

        # Initialize variable
        self.BROKER = str(broker_ip)
        self.PORT = 1883
        self.ALIVE = 60
        self.MQTTC = mqtt.Client()
        self.NAME = str(name)
        self.TOPIC = str(topic)
        self.DESC = str(desc)

        # Find the token
        for key, value in TOKENS.items():
            if key == token:
                self.TOKEN = value

        # Create event handlers for MQTT
        self.MQTTC.on_connect = self.connect
        self.MQTTC.on_publish = self.publish

        # Setting up MQTT to a client and connecting
        self.MQTTC.connect(self.BROKER, self.PORT, self.ALIVE)

        # Bridge child node to parent node
        bridge = { self.gv.get_name() : self.NAME, self.gv.get_ip() : self.IP, self.gv.get_topic() : self.TOPIC, self.gv.get_token() : self.TOKEN, self.gv.get_desc() : self.DESC}
        for key, value in bridge.items():
            tp = "HARPi/" + self.gv.get_set_node() + "/" + key
            self.MQTTC.publish(tp, value)
            sleep(0.5)
        tp = "HARPi/" + self.gv.get_set_node() + "/" + self.gv.get_complete()
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

    # Status event handler
    def status_msg(self, msg):
        tp = "HARPi/" + self.gv.get_status() + "/" + self.TOPIC
        st = self.TOKEN + msg
        self.MQTTC.publish(tp, st)
        print("Status : %s" %(st))

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
