# -*- coding: utf-8 -*-
""" It is a virtual test with virtual rssi readings to prove that if the 
bluetooth technology were more precise, or if we would use another technology,
this software could run correctly """

import socket
import time
#from SocketUtilities import obtener_mac
#import blescan
import fileLibrary as fl
import sys
from Posicionar import VirtualBeacons
#import bluetooth._bluetooth as bluez

PUERTO = 5010
SERVER = '192.168.1.8'

#mi_mac = obtener_mac('eth0').lower()
#print(mi_mac)

dev_id = 0
"""
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)
"""
friendList = fl.readFile("friendList.txt")

macs = list(a.mac.lower() for a in friendList)
print macs

#blescan.hci_le_set_scan_parameters(sock)
#blescan.hci_enable_le_scan(sock)

i=0
while True:
	#Conectarlo a la central
	socket_c = socket.socket()  
	socket_c.connect((SERVER, PUERTO))  
	#returnedList = blescan.parse_events_2(sock, macs, 10)
	returnedList = VirtualBeacons(i, 8)
	i = (i+1)%3
	print "----------"
	for beacon in returnedList:
		#print "----------"
		print beacon
		socket_c.send(beacon) 
	time.sleep(1)
	#socket_c.send('END')
	socket_c.close()



