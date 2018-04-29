#===============================================
# Program name: global_var.py
# Desc: Initialize all global variables that are
#       and  will  be  used  in  bridge.py  and
#       child_mqtt.py.
# 
# Author: HARPi
# Date: 29.04.18
#===============================================

class Global_Var:
    def __init__(self):
        # Strings
        self.COMPLETE = "complete"
        self.SET_NODE = "set_node"
        self.NAME = "name"
        self.IP = "ip"
        self.TOPIC = "topic"
        self.TOKEN = "token"
        self.DESC = "desc"
        self.STATUS = "status"

        # Integers
        self.NEW_NODE = 1
        self.STATUS_NODE = 2
        self.CLEAR_BIT = 15

    def get_complete(self):
        return self.COMPLETE

    def get_set_node(self):
        return self.SET_NODE

    def get_name(self):
        return self.NAME

    def get_ip(self):
        return self.IP

    def get_topic(self):
        return self.TOPIC

    def get_token(self):
        return self.TOKEN

    def get_desc(self):
        return self.DESC

    def get_status(self):
        return self.STATUS

    def get_new_node(self):
        return self.NEW_NODE

    def get_status_node(self):
        return self.STATUS_NODE

    def get_clear_bit(self):
        return self.CLEAR_BIT

