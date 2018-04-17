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

# Splitting token
import shlex

# Pinging
import subprocess

class child_mqtt:
    def __init__(self, name, topic, broker_ip, desc):
        # Grab IP address
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        self.IP = sock.getsockname()[0]
        sock.close()

        # Initialize variable
        self.BROKER = str(broker_ip)
        self.PORT = 1883
        self.ALIVE = 60
        self.NAME = str(name)
        self.TOPIC = str(topic)
        self.DESC = str(desc)

        # Setting up MQTT to a client and connecting
        self.MQTTC = mqtt.Client()
        self.MQTTC.connect(self.BROKER, self.PORT, self.ALIVE)

        # Event handler for every publish
        self.MQTTC.on_publish = self.publish

    def publish(self, client, userdata, msg):
        return

    def send_msg(self, msg):
        self.MQTTC.publish(self.TOPIC, msg)
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

    def check_connection(self):
        conn = shlex.split("ping -c1 %s" %self.IP)
        try:
            output = subprocess.check_output(conn)
        except subprocess.CalledProcessError, e:
            print("ERROR: not able to connect to %s" %self.IP)
        else:
            print("Connected to: %s" %self.IP)
