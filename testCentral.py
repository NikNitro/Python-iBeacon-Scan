# -*- coding: utf-8 -*-
import socket
import fileLibrary as fl
from collections import deque
import Posicionar as pos
import time
from sympy import *

x=Symbol('x') 
y=Symbol('y')
PUERTO = 5010
MAX = 10 # Número de paquetes que vamos a guardar de cada baliza
socket_s = socket.socket()

#El socket se puede dejar vacío
socket_s.bind(('', PUERTO))
try:
	#Listen recibe el número máximo de conexiones simultáneas
	socket_s.listen(3);

	nombre, nose, ip = socket.gethostbyname_ex(socket.gethostname())
	print "Sistema '",nombre, "' esperando conexión en el puerto ", PUERTO
	#print "Y en la dirección ", ip[0]

	friendList = fl.readFile("friendList.txt")
	#macs = list(a.mac.lower() for a in friendList)
	balizas = list(fl.Baliza(a.nombre.lower(), a.mac.lower(), a.posX.lower(), a.posY.lower()) for a in friendList)
	# Creamos un diccionario en el que asignamos a cada mac la posición que tiene
	dicBalizas = dict(list((a.mac.lower(),[a.posX, a.posY]) for a in friendList))
	#print(str(balizas[0]) + " " + str(balizas[1]))
	#mac0 = balizas[0].mac
	#print(str(mac0))
	print(dicBalizas[balizas[0].mac])

	# Y otro diccionario para asignar, a una mac, una cola con los 10 últimos paquetes que le han llegado.
	dicRecepcion = dict(list( ( a, deque() ) for a in dicBalizas.keys() ))

	while(True):
		socket_c, (host_c, puerto_c) = socket_s.accept()
		#accept se mantiene a la espera de conexiones entrantes, bloqueando la ejecución hasta que llega un mensaje
		try:
			recibido = socket_c.recv(56)
			while(recibido):#!='END'):
				#time.sleep(1)
				#print("----------------------")
				#print "Recibido de ", host_c, " el mensaje", recibido
				# Actualmente no usamos la variable mac porque suponemos que solo hay que
				# localizar un elemento
				mac_origen, mac, valx, valy, thrash, pwr = recibido.split(",")

				dicRecepcion[mac_origen].append(pwr)
				# Para no consumir toda la memoria del dispositivo
				while(len(dicRecepcion[mac_origen]) > MAX):
					dicRecepcion[mac_origen].popleft()
				recibido = socket_c.recv(56)
				if not recibido: break
			#socket_c.send("200")
		finally:
			socket_c.close()

		macsCompletas = list( mac for mac in dicBalizas.keys() if len(dicRecepcion[mac])>=MAX )
		rssiMedia = dict( list( (mac, pos.average(dicRecepcion[mac])) for mac in macsCompletas) )
		for mac in rssiMedia.keys():
			print("VALOR MEDIA: "+str(mac) + ": " + str(rssiMedia[mac]))

		# Ahora obtendremos (si podemos) las ecuaciones
		# x^2 + y^2 -2*aux(1)*x -2*aux(2)*y + ( aux(1)^2 + aux(2)^2 - dist^2 ) 
		# pos.rssi2distance
		if len(macsCompletas) > 2:
			distancias = []
			for mac in rssiMedia.keys():
				A = int(dicBalizas.get(mac)[0])
				B = int(dicBalizas.get(mac)[1])
				C = pos.rssi2distance(rssiMedia.get(mac))

				polinomio = x**2 + y**2 - 2*A*x - 2*B*y + (A**2 + B**2 - C**2)
				distancias.append(polinomio)

			posicionFinal = pos.Posicionar(distancias)
			print("Posicion actual: ("+str(posicionFinal[0])+","+str(posicionFinal[1])+")")


finally:
	socket_s.close()