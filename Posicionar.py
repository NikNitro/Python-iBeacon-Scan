# -*- coding: utf-8 -*-

#import blescan
#import fileLibrary as fl
#import sys

#import bluetooth._bluetooth as bluez
from sympy import *

def Posicionar(distancias):
	#POSICIONAR Recibe las distancias a cada baliza en forma de ecuación y
	# devuelve la posición del elemento a encontrar.
	#   



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
						# INICIO Update 1
						#if(mapObjX.isKey(single(solx(k)))) 
						goodKey = IsThereASimilarKey(mapObjX, solx[k]);
						if(goodKey!=-1):
							mapObjX[goodKey] = (mapObjX[goodKey] + 1);
						else:
							mapObjX[solx[k]] = 1;

		            # Y guardamos la y
					for k in range(0, len(soly)):
						goodKey = IsThereASimilarKey(mapObjY, soly[k]);
						if(goodKey!=-1):
							mapObjY[goodKey] = (mapObjY[goodKey] + 1);
						else:
							mapObjY[soly[k]]= 1;
							# FIN Update 1

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
	        print("Nuevo numX = "+ str(elemX))
	for i in range(1,len(listaY)):
	    elemAux = listaY[i];
	    numAux = mapObjY[elemAux];
	    if(numAux>numY):
	        numY = numAux;
	        elemY = elemAux;
	        print("Nuevo numY = "+ str(elemY))

	print(elemX)
	print(elemY)

def IsThereASimilarKey(mapObj, elem, margen=1):
	result = -1
	for i in range(elem-margen, elem+margen):
		if(i in mapObj.keys()):
			result = i

	return result
