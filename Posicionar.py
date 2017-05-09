# -*- coding: utf-8 -*-

#import blescan
#import fileLibrary as fl
#import sys

#import bluetooth._bluetooth as bluez
from sympy import *

# Más info sobre las constantes en la tabla de drive. 
# Es necesario calibrarlas ante cualquier cambio.
# Sería interesante automatizar este proceso
TXPOWER = -69.16666667#-72.49269311
NCONSTANT = 1#0.3886

def Posicionar(distancias):
	#POSICIONAR Recibe las distancias a cada baliza en forma de ecuación y
	# devuelve la posición del elemento a encontrar.
	#   

	MARGEN=100

	## Obtenemos los valores dos a dos y los resolvemos, guardándolos en 
	# un mapa de resultados
	numDist = len(distancias);
	#numDist = numDist(2);

	#Creamos un mapa con los elementos a añadir
	#mapObj = containers.Map;
	#Los Mapas por defecto son de caracteres. Definimos uno de enteros.
	mapObjX = {}#containers.Map('KeyType','single','ValueType','single');
	mapObjY = {}#containers.Map('KeyType','single','ValueType','single');

	x=Symbol('x') 
	y=Symbol('y')
	for i in range(0, numDist):
		for j in range(i, numDist):
			if i != j:
				#print(distancias[i])
				#print(distancias[j])
				resAux = solve([distancias[i], distancias[j]], [x,y])
				print('Ecuaciones: \n')
				print(str(distancias[i]))
				print(str(distancias[j]))
				print('Soluciones:\n')
				print(str(resAux))
				if(len(resAux)!=0):
					# Hay que guardar los resultados dependiendo del número de soluciones
					if(len(resAux)==1):
						(solx, soly) = resAux[0]
						solx = [solx]
						soly = [soly]
					else:
						#Else tiene dos soluciones
						(solx, soly) = resAux[0]
						(auxsolx, auxsoly) = resAux[1]
						solx = [solx,auxsolx]
						soly = [soly,auxsoly]

					#Estas asignaciones son mas extrañas que las de MatLab porque en MatLab solve
					# te devuelve una lista con las 'X' y otra con las 'Y' mientras que en Python
					# te devuelve las soluciones en tuplas
					#print(solx)
					#print(soly)
					# Guardamos la x
					for k in range(0, len(solx)):
						""" Vamos a añadir clausulas para ignorar las soluciones complejas """
						a = complex(solx[k])
						#print("El tipo es: " + str(type(a)))
						if(a.imag == 0):
							# INICIO Update 1
							#if(mapObjX.isKey(single(solx(k)))) 
							#print("solx vale " + str(a))
							goodKey = IsThereASimilarKey(mapObjX, solx[k], MARGEN);
							#print("Encontrada ke X similar a "+ str(solx[k]) + ': '+str(goodKey)+'\n')
							if(goodKey!=-1):
								mapObjX[goodKey] = (mapObjX[goodKey] + 1);
							else:
								mapObjX[int(solx[k])] = 1;

						""" ñañaña """
		            # Y guardamos la y
					for k in range(0, len(soly)):
						""" Vamos a añadir clausulas para ignorar las soluciones complejas """
						a = complex(soly[k])
						if(a.imag == 0):
							#print("soly vale " + str(a))
							goodKey = IsThereASimilarKey(mapObjY, soly[k], MARGEN);
							#print("Encontrada key Y similar a "+ str(soly[k]) + ': '+str(goodKey)+'\n')
							if(goodKey!=-1):
								mapObjY[goodKey] = (mapObjY[goodKey] + 1);
							else:
								mapObjY[int(soly[k])]= 1;
								# FIN Update 1

						""" ñañaña """
	## Elegimos a los valores de x y de y resultantes, tomando los que tienen 
	# más coincidencias

	listaX = mapObjX.keys();
	elemX = listaX[0];
	numX  = mapObjX[elemX];
	listaY = mapObjY.keys();
	elemY = listaY[0];
	numY  = mapObjY[elemY];

	for i in range(1,len(listaX)):
	    elemAux = listaX[i];
	    numAux = mapObjX[elemAux];
	    if(numAux>numX):
	        numX = numAux;
	        elemX = elemAux;
	        #print("Nuevo numX = "+ str(elemX))
	for i in range(1,len(listaY)):
	    elemAux = listaY[i];
	    numAux = mapObjY[elemAux];
	    if(numAux>numY):
	        numY = numAux;
	        elemY = elemAux;
	        #print("Nuevo numY = "+ str(elemY))

	print(elemX)
	print(elemY)
	return (elemX, elemY)

#####################################################
# Si rssi = -10 * n * log10(distancia) + txpower    #
# distancia = 10 ^ ((txpower-rssi)/10*n)			#
# La devuelvo multiplicada por 10 para obtener mm	#
#####################################################
def rssi2distance(rssi):
	num =TXPOWER-rssi
	den = 10*NCONSTANT
	exp = num/den
	distance = pow(10, exp)
	return distance#*100 


def IsThereASimilarKey(mapObj, elem, margen=1):
	result = -1
	for i in range(elem-margen, elem+margen):
		if(i in mapObj.keys()):
			result = i

	return result

def average(lista):
	suma = 0.0
	for n in lista:
		suma += float(n)
	return suma/len(lista)

#To use it in virtualScan
def VirtualBeacons(cual, cuantas):
	beacons = ['b8:27:eb:33:89:d4', 'b8:27:eb:ba:32:52', 'b8:27:eb:f9:5f:fe']
	rests   = [',d0:c9:79:93:d8:94,51577,37848,-108,-90',#.67181664', 
	           ',d0:c9:79:93:d8:94,51577,37848,-108,-94',#.77774606', 
	           ',d0:c9:79:93:d8:94,51577,37848,-108,-98']#.23123345']

	stri = str(beacons[cual]) + str(rests[cual])
	li=[]
	for i in range(cuantas):
		li +=[stri]
	print(li)
	return li