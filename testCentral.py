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
import random

x=Symbol('x') 
y=Symbol('y')
PUERTO = 5010
MARGEN=0.02
#LISTA_MARGENES = [x/100 for x in range(-int(MARGEN*100),int(MARGEN*100)+1)]
MAX = 20 # Número de paquetes que vamos a guardar de cada baliza
#TAMMSG = 39 # Tam del mensaje a recibir (mac+,+mac+,+txpower)
TAMMSG = 42 # Tam del mensaje a recibir (mac+,+mac+,+distancia)
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
	print(dicBalizas)

	##Creamos el grafico
	quiere = "n"
	for bal in balizas:
		print("Imprimiendo " + str(bal.nombre))
		plt.scatter(bal.posX,bal.posY, marker='2', label=bal.nombre)
		#print("¿Quiere ajustar la baliza " + str(bal.nombre) + "? (y/n)")
		##quiere = input()
		#if quiere=="y":
        #            bal.setDistanceFunct(pos.ajustar(bal.nombre))
	
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
	print("Sistema '",nombre, "' esperando conexión en el puerto ", PUERTO)
	#print "Y en la dirección ", ip[0]

	# Y otro diccionario para asignar, a una mac, una cola con los 10 últimos paquetes que le han llegado.
	dicRecepcion = dict(list( ( a, deque() ) for a in dicBalizas.keys() ))
	recibido = "first"
	while(recibido!='END'):
		socket_c, (host_c, puerto_c) = socket_s.accept()
		#accept se mantiene a la espera de conexiones entrantes, bloqueando la ejecución hasta que llega un mensaje
		try:
			#tam_rec = int((socket_c.recv(2)).decode())
			#print('se reciben: ', tam_rec, 'bytes')
			recibido = socket_c.recv(TAMMSG)
			while(recibido):#!='END'):
				#time.sleep(1)
				#print("----------------------")
				#print "Recibido de ", host_c, " el mensaje", recibido
				# Actualmente no usamos la variable mac porque suponemos que solo hay que
				# localizar un elemento
				#mac_origen, mac, valx, valy, thrash, pwr = recibido.split(",")
				datos = recibido.decode()
				print(datos)
				mac_origen, mac, dist = datos.split(",")

				f=open("centralLog.aml", "a") #append, para que no borre
				f.write(time.strftime("%X") + ":" + mac_origen +"," + mac + ","+ dist + "\n")
				f.close()

				dicRecepcion[mac_origen].append(dist)
				# Para no consumir dtoda la memoria del dispositivo
				while(len(dicRecepcion[mac_origen]) > MAX):
					dicRecepcion[mac_origen].popleft()

				#recibido = (socket_c.recv(2)).decode()
				#print('se reciben: ', recibido, 'bytes')
				#tam_rec = int(recibido)
				#print('se reciben: ', tam_rec, 'bytes')
				recibido = socket_c.recv(TAMMSG)
				if not recibido: break
			#socket_c.send("200")
		finally:
			socket_c.close()

		macsCompletas = list( mac for mac in dicBalizas.keys() if len(dicRecepcion[mac])>=MAX )

		rssiMedia = {}
		for mac in macsCompletas:
			queue = dicRecepcion[mac]
			lista = list(queue)
			tamm = len(lista)
			# print("tamm ", tamm)
			lista.sort()
			# print("lista ", str(lista))
			listaEnMedio = lista[3:7]
			rssiMedia[mac] = float("{0:.2f}".format(pos.average(listaEnMedio)))

		# rssiMedia = dict( list( (mac, pos.average(list(dicRecepcion[mac]).sort()[3:(len(dicRecepcion[mac])-3)])) for mac in macsCompletas) )
		for mac in rssiMedia.keys():
			print("VALOR MEDIA: "+str(mac) + ": " + str(rssiMedia[mac]))

		# Ahora obtendremos (si podemos) las ecuaciones
		# x^2 + y^2 -2*aux(1)*x -2*aux(2)*y + ( aux(1)^2 + aux(2)^2 - dist^2 ) 
		# pos.rssi2distance
		if len(macsCompletas) > 2:
			distancias = []
			for mac in rssiMedia.keys():
				A = float(dicBalizas.get(mac).posX)
				B = float(dicBalizas.get(mac).posY)
				#C = pos.rssi2distance(rssiMedia.get(mac), dicBalizas.get(mac).txpower)
				#C = pos.rssi2distanceBook(rssiMedia.get(mac), dicBalizas.get(mac).txpower) * 1000 # Para que lo de en centímetros
				C = rssiMedia.get(mac)
				print('---distancia: '+str(C) + " de " + mac)

				#for mm in LISTA_MARGENES:
				polinomio = x**2 + y**2 - 2*A*x - 2*B*y + (A**2 + B**2 - C**2)
				#print(polinomio)
				distancias.append(polinomio)
			# print(distancias)

			posicionFinal = pos.Posicionar(distancias, MARGEN)
			if(posicionFinal=="noSoluc" and ultPosEncontrada == 'ninguna'):
				print("No encontrada solucion todavia")
			elif posicionFinal=="noSoluc":
				print("Posicion anterior: ("+str(ultPosEncontrada[0])+","+str(ultPosEncontrada[1])+")")
			else:
				print("Posicion actual: ("+str(posicionFinal[0])+","+str(posicionFinal[1])+")")

				listaPuntosX += [posicionFinal[0]]
				listaPuntosY += [posicionFinal[1]]
				ultPosEncontrada = posicionFinal
				total = total + 1
				if(total>0):
					#####IMPRIMIMOS
					##Creamos el grafico
					#for bal in balizas:
					#	plt.scatter(bal.posX,bal.posY, marker='2', label=bal.nombre)
					plt.scatter(listaPuntosX,listaPuntosY,c='b', label='posicion')
					plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
					plt.show()

finally:
	socket_s.close()
	plt.show()