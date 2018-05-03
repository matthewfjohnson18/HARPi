# HARPi
Home Automation with Raspberry Pi (HARPi) makes it easy to connect different nodes to a single home node.

# Install
Run the `install.sh` script to install the requirements
```
 $ ./install.sh
```

# child_mqtt:
Python class that is added to a python program intended to connect to the parent.

### child_mqtt how-to:
Initialize _child_mqtt()_ to a object with a given name, topic, token, and description. You will also need to enter the brokers IP address, that should be the one you're connecting to. See _test.py_ for example.

# Bridge:
Python class that connects the children to the parent. This program runs in the background of _child_mqtt.py_, once a new object of  _child_mqtt.py_ is created, it will be sent to _bridge.py_ where it will add the new node in. _bridge.py_ is the middle program between the children and the parent, where the children talk to and only to the parent. As of this very moment, the children cannot talk to each other

# MattsHARPi:
Python script to run various sensors through an ADC breakout board from Adafruit. Must import the ADC's library from Adafruit before use. Also must install MQTT child information and scripts from Loerac. To run the program from a terminal go to..
```
$ ~/Documents/HARPi/
```
And run the following script to activate the sensor node...
```
$ python3 MattsHARPi.py
```
The screen should start reading output in sentence format and show that STATUS updates are being sent.
