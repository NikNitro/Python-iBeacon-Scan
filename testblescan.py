# -*- coding: utf-8 -*-
import socket
import time
from SocketUtilities import obtener_mac
import blescan
import fileLibrary as fl
import sys
import bluetooth._bluetooth as bluez

PUERTO = 5010
RASPI_IP = '192.168.1.14'
mi_mac = obtener_mac('eth0').lower()
print(mi_mac)

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)
friendList = fl.readFile("friendList.txt")

macs = list(a.mac.lower() for a in friendList)
print macs

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)


while True:
	#Conectarlo a la central
	socket_c = socket.socket()  
	socket_c.connect((RASPI_IP, PUERTO))  
	returnedList = blescan.parse_events_2(sock, macs, 10)
	for beacon in returnedList:
		#print "----------"
		#print beacon
		socket_c.send(mi_mac+","+beacon) 
	#time.sleep(5)
	#socket_c.send('END')
	socket_c.close()


