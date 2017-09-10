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

#Leemos el archivo por si ya hemos ajustado antes esa función
func = 0
f=open("ajustes.aml", "ra") #append, para que no borre
linea = f.readline()
while linea != "" and linea.split('/')[0] != mi_mac:
	linea = f.readline()

if linea == "":
	func = ajustar(mi_mac, sock, macs, verGrafica=True)
else:
	func = linea.split('/')[1]
	func = num.poly1d(num.array([num.float64(s) for s in func[1:-1].replace('\n', '').split('  ')]))
	f.write(str(func))


while True:
	#Conectarlo a la central
	socket_c = socket.socket()  
	socket_c.connect((SERVER, PUERTO))  
	returnedList = blescan.parse_events_2(sock, macs, 10)
	for beacon in returnedList:
		#print "----------"
		#print beacon
		mac, pwr = beacon.split(',')
		print("distancia: ", str(func(float(pwr))))
		#print("distancia: ", "{:10.4f}".format(16.469849301549))
		mensaje= str(mi_mac+","+mac+","+"{:2.4f}".format(func(float(pwr))))
                #mensaje= str(mi_mac+","+mac+","+"{:2.4f}".format(16.469849301549)) 
		#print("\tSe envian " + str(len(mensaje)) + " bytes que son " + mensaje)
		#socket_c.send(str(len(mensaje)))
		if func(float(pwr))<10:
			socket_c.send(mensaje) 
	#socket_c.send('END')
	socket_c.close()
	time.sleep(1)


