import paho.mqtt.client as mqtt

import socket

class child_mqtt:
    def __init__(self, name, topic, broker_ip, ip, desc):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        self.ip = sock.getsockname()[0]
        sock.close()

        self.BROKER = str(broker_ip)
        self.PORT = 1883
        self.ALIVE = 60
        self.NAME = str(name)
        self.TOPIC = str(topic)
        self.IP = str(ip)
        self.DESC = str(desc)
        self.MQTTC = mqtt.Client()
        self.MQTTC.connect(self.BROKER, self.PORT, self.ALIVE)
        self.MQTTC.on_publish = self.publish

    def publish(self, client, userdata, msg):
        #print("Client %s" %client)
        #print("Userdata %s" %userdata)
        #print("MSG count %s" %msg)
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
