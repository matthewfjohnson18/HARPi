#!/usr/bin/python

#===============================================
# Program name: bridge.py
# Desc: Linking  the  children  nodes  to  the
#       parent  node.  The  parent  node  will
#       receive the name, topic, IP, token, and
#       description of the children where. There
#       is  also  the  aspect  of  pinging  the
#       children to check if they're connected.
#
# Author: HARPi
# Date: 25.04.18
#===============================================

# Imports
#===============================================
# MQTT
import paho.mqtt.client as mqtt

# Time
from time import sleep

# Socket for IP address
import socket

# Splitting token
import shlex

# Pinging
import subprocess

class Bridge:
    def __init__(self):
        # Getting IP address
        sock = sock.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))

        # Initialize MQTT
        self.BROKER = sock.getsockname()[0]
        sock.close()
        self.PORT = 1883
        self.ALIVE = 60
        self.MQTTC = mqtt.Client()
        self.TOPIC = "HARPi/#"

        # Global Variables
        self.NODE_LIST = {}
        self.NODE_DICT = {"complete" : 0}
        self.NEW_NODE = False

        # Set up MQTT with broker
        self.MQTTC.connect(self.BROKER, self.PORT, self.ALIVE)

        # Set up event handlers
        self.MQTTC.on_connect = self.connect
        self.MQTTC.on_message = self.message

    # Subscribe to a topic
    def connect(self, mosq, obj, rc):
        self.MQTTC.subscribe(self.TOPIC, 0)

    # Print out incoming messages
    def message(self, mosq, obj, msg):
        print("%s : %s" %(msg.topic.split("HARPi/")[1], msg.payload)
        topic = msg.topic.split("HARPi/")[1]
        data = msg.payload

        if topic[:8] == "set_node":
            self.set_node(topic[9:], data)

    # Store new node values in dictionary
    def set_node(self, key, value):
        self.NODE_DICT[key] = value
        if self.NODE_DICT["complete"] == 1:
            self.NEW_NODE = True
            self.NODE_LIST.append(self.NODE_DICT.copy)

    # Return dictionary with new child values
    def get_node(self):
        self.NODE_DICT["complete"] = 0
        self.NEW_NODE = False
        return self.NODE_LIST

    # Check connection with children
    def check_connection(self):
        for i in range(0, len(self.NODE_LIST)):
            ip = self.NODE_LIST[i]['ip']
            conn = shlex.split("ping -c1 %s" %ip)
            try:
                output = subprocess.check_output(conn)
            except subprocess.CalledProcessError, e:
                # Call out to GUI letting know cannot connect to given IP
                print("Error: not able to connnect to %s" %ip)
            else:
                print("Connected: %s" %ip)
