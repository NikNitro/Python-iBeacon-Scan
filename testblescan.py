# -*- coding: utf-8 -*-
import socket
import time
from SocketUtilities import obtener_mac
import blescan
import fileLibrary as fl
import sys
import bluetooth._bluetooth as bluez
from Posicionar import ajustar

PUERTO = 5010
SERVER = '192.168.31.116'

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

ajustar(mi_mac, sock, macs, verGrafica=True):


while True:
	#Conectarlo a la central
	socket_c = socket.socket()  
	socket_c.connect((SERVER, PUERTO))  
	returnedList = blescan.parse_events_2(sock, macs, 10)
	for beacon in returnedList:
		#print "----------"
		#print beacon
		socket_c.send(mi_mac+","+beacon) 
	#socket_c.send('END')
	socket_c.close()
	time.sleep(1)


