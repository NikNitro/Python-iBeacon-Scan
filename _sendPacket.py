# -*- coding: utf-8 -*-
#To can connect
import socket
#To can read the friendlist.txt file
import fileLibrary as fl
#To use a queue
from collections import deque
#To calculate the position
import Posicionar as pos
#To do the sleep and get the date
import time
#To solve equations
from sympy import *
import numpy as np

# In this test we're gonna send packets to the client and counting the time until we recept the answer.
# It's obvius that more time means more distance.
PUERTO = 5010
MARGEN=500
MAX = 20 # Número de paquetes que vamos a guardar de cada baliza
TAMMSG = 39 # Tam del mensaje a recibir (mac+,+mac+,+txpower)
#Para los dibujos
listaPuntosX=[]
listaPuntosY=[]
total=0

friendList = fl.readFile("friendList.txt")
#macs = list(a.mac.lower() for a in friendList)
# Pero si friendlist ya es una lista de balizas. Podriamos mejorar esto
balizas = list(fl.Baliza(a.nombre.lower(), a.mac.lower(), a.posX.lower(), a.posY.lower(), a.txpower) for a in friendList)
# Creamos un diccionario en el que asignamos a cada mac la posición que tiene
#dicBalizas = dict(list((a.mac.lower(),[a.posX, a.posY]) for a in friendList))
# Creamos un diccionario en el que asignamos a cada mac la baliza que tiene
dicBalizas = dict(list((a.mac.lower(),a) for a in friendList))
print(dicBalizas[balizas[0].mac])
		
import bluetooth
# RaspiHC será la baliza.

# bd_addr = "B8:27:EB:99:23:7E"
# bd_addr = 'b8:27:eb:99:23:7e'
# bd_addr = 'b8:27:eb:66:dc:81' # Esta es la mac wifi
bd_addr = '192.168.31.162' # Ip de red
port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
print("Socket creado")
sock.connect((bd_addr, port))
print("Socket conectado")
sock.send("hello!!")

sock.close()









