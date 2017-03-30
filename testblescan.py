# test BLE Scanning software
# jcs 6/8/2014

import blescan
import fileLibrary as fl
import sys

import bluetooth._bluetooth as bluez

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
	returnedList = blescan.parse_events(sock, 10)
	print "-----1-----"
	for beacon in returnedList:
		print beacon
	returnedList = blescan.parse_events_2(sock, macs, 10)
	print "-----2-----"
	for beacon in returnedList:
		print beacon

