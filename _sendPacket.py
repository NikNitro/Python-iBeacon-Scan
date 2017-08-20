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
#To plot
import matplotlib.pyplot as plt
import numpy as np

# This is a script to send a beacon with our datas
x=Symbol('x') 
y=Symbol('y')
PUERTO = 5010
MARGEN=500
MAX = 20 # Número de paquetes que vamos a guardar de cada baliza
TAMMSG = 39 # Tam del mensaje a recibir (mac+,+mac+,+txpower)
socket_s = socket.socket()
ultPosEncontrada = "ninguna"
#Para los dibujos
listaPuntosX=[]
listaPuntosY=[]
total=0

#El socket se puede dejar vacío
socket_s.bind(('', PUERTO))
try:
	#Listen recibe el número máximo de conexiones simultáneas
	socket_s.listen(3);

	friendList = fl.readFile("friendList.txt")
	#macs = list(a.mac.lower() for a in friendList)
	# Pero si friendlist ya es una lista de balizas. Podriamos mejorar esto
	balizas = list(fl.Baliza(a.nombre.lower(), a.mac.lower(), a.posX.lower(), a.posY.lower(), a.txpower) for a in friendList)
	# Creamos un diccionario en el que asignamos a cada mac la posición que tiene
	#dicBalizas = dict(list((a.mac.lower(),[a.posX, a.posY]) for a in friendList))
	# Creamos un diccionario en el que asignamos a cada mac la baliza que tiene
	dicBalizas = dict(list((a.mac.lower(),a) for a in friendList))
	#print(str(balizas[0]) + " " + str(balizas[1]))
	#mac0 = balizas[0].mac
	#print(str(mac0))
	print(dicBalizas[balizas[0].mac])

	##Creamos el grafico
	for bal in balizas:
		print("Imprimiendo " + str(bal.nombre))
		plt.scatter(bal.posX,bal.posY, marker='2', label=bal.nombre)
	
	#Para que pueda seguir calculando cosas
	#plt.interactive(True)
	#Para que muestre la leyenda
	plt.legend(loc = 2)
	#Para que lo muestre
	#plt.show()

	##Creamos el fichero de log, sobreescribiendo el anterior si lo hubiera.
	f=open("centralLog.aml", "w")
	f.write("Lectura de " + time.strftime("%d/%m/%y") + "\n") #Tambien vale poner "%x"
	f.close()




	nombre, nose, ip = socket.gethostbyname_ex(socket.gethostname())
	print "Sistema '",nombre, "' esperando conexión en el puerto ", PUERTO
	#print "Y en la dirección ", ip[0]

	# Y otro diccionario para asignar, a una mac, una cola con los 10 últimos paquetes que le han llegado.
	dicRecepcion = dict(list( ( a, deque() ) for a in dicBalizas.keys() ))
	recibido = "first"
	while(recibido!='END'):
		socket_c, (host_c, puerto_c) = socket_s.accept()
		#accept se mantiene a la espera de conexiones entrantes, bloqueando la ejecución hasta que llega un mensaje
		try:
			recibido = socket_c.recv(TAMMSG)
			while(recibido):
				mac_origen, mac, pwr = recibido.split(",")

				f=open("centralLog.aml", "a") #append, para que no borre
				f.write(time.strftime("%X") + ": --" + str(dicBalizas[mac_origen].nombre) +"-- " + str(recibido) + "\n")
				f.close()

				dicRecepcion[mac_origen].append(pwr)
				# Para no consumir toda la memoria del dispositivo
				while(len(dicRecepcion[mac_origen]) > MAX):
					dicRecepcion[mac_origen].popleft()
				recibido = socket_c.recv(TAMMSG)
				if not recibido: break
			#socket_c.send("200")
		finally:
			socket_c.close()

		
finally:
	socket_s.close()
	plt.show()