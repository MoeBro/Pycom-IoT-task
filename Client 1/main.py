import os 
import socket
import time
import struct
import machine 
import pycom
from pysense import Pysense 
from LIS2HH12 import LIS2HH12
from network import WLAN
import json 
import urequests


#Adress and port of the server
host = '192.168.0.8'
url = "http://192.168.0.8/update"
deviceID = "1"
py = Pysense()
li = LIS2HH12(py)


# This part connects the board to Wifi
wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
pycom.heartbeat(False)
antenna=WLAN.EXT_ANT
for net in nets:
    if net.ssid == 'Gronnemarken18':
        print('Network found!')
        wlan.connect(net.ssid,auth=(WLAN.WPA2,'toofan2204'), timeout=10000)
        while not wlan.isconnected():
            print('Not connected')
            time.sleep(1)
        print('WLAN connection succeeded!')
        pycom.rgbled(0x007f00) # green
        break  


#Sending the data to a server
while True:
    
    acc = li.acceleration() 
    x = acc[0]
    y = acc[1]
    z = acc[2]
    mydata = {"ID":deviceID, "x": x,"y":y,"z":z}
    urequests.post("http://192.168.0.8/update",json=mydata).close()
    time.sleep(0.5)


