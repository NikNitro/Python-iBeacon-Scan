# -*- coding: utf-8 -*-

from sympy import *
import mpmath as mp
from math import ceil
import sys
import numpy as num
#import matplotlib.pyplot as plt
#import bluetooth._bluetooth as bluez

# Más info sobre las constantes en la tabla de drive. 
# Es necesario calibrarlas ante cualquier cambio.
# Sería interesante automatizar este proceso
TXPOWER = -69.16666667#-72.49269311
NCONSTANT = 1#0.3886

def Posicionar(distancias, MARGEN=100):
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
						#Si es un numero imaginario, nos quedamos solo con su parte real
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
	listaY = mapObjY.keys();

	if(len(listaX)>0 and len(listaY)>0):
		elemX = listaX[0];
		numX  = mapObjX[elemX];
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

		#print(elemX)
		#print(elemY)
		return (elemX, elemY)
	else:
		return "noSoluc"

#####################################################
# Si rssi = -10 * n * log10(distancia) + txpower    #
# distancia = 10 ^ ((txpower-rssi)/10*n)            #
# La devuelvo multiplicada por 1 para obtener m	    #
#####################################################
def rssi2distance(rssi, txpower=TXPOWER, n=NCONSTANT):
	num =TXPOWER-rssi
	den = 10*NCONSTANT
	exp = num/den
	distance = pow(10, exp)


	return distance*1

"""
python
from Posicionar import *
x = rssi2distanceBook(-80)
x
exit()
"""
# La función según el libro que estoy leyendo (Valentín)
def rssi2distanceBook(rssi, txpower=TXPOWER, n=NCONSTANT):
	exp = rssi/10
	mW = pow(10, exp)

	#Aplicamos la función 2.3 del libro
	d0 = 1
	Pij = mW
	P0 = pow(10, TXPOWER/10)
	# np pertenece al rango [2,4], donde los valores bajos se utilizan en entornos abiertos o con poca
	# pérdida de potencia.
	np = 2
	# sigma es la desviación típica de la variable aleatoria distribuida de forma normal que representa
	# el efecto aleatorio producido por las sombras que originan los diferentes obstáculos.
	sigma = 18.75
	mu = 10/mp.ln(10)
	print(Pij, P0, np, sigma, mu, mp.e) 

	#Ahora montamos la función
	distancia = d0
	distancia *= pow(Pij/P0, -1/np)
	distancia *= pow(mp.e, -(sigma*sigma)/(2*mu*mu*np*np))
	return distancia


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

# Funciones para obtener la mejor n
def miMinimize(entrada, salidaDeseada, bounds, times=100):

	def f(entrada, salidaDeseada, n):
	    distanciasCalculadas = []
	    distanciasReales = salidaDeseada
	    rssis = entrada
	    distanciasCalculadas = num.array(rssi2distance(rssis,txpower=rssis[0], n=n))
	    # print('calculadaS: ' + str(distanciasCalculadas))
	    diferencia = distanciasReales - distanciasCalculadas
	    # print(diferencia, sum(diferencia))
	    return sum(diferencia)

	inicio = bounds[0]
	fin = bounds[1]
	for i in range(0,times):
		mitad = inicio + (fin-inicio)/2.
		mitad1 = inicio+(mitad-inicio)/2.
		mitad2 = mitad+(fin-mitad)/2.
		
		resAux1 = f(entrada, salidaDeseada, mitad1)
		resAux2 = f(entrada, salidaDeseada, mitad2)
		# print(resAux1, mitad1, resAux2, mitad2)
		if resAux1>resAux2:
			inicio = mitad
		else:
			fin = mitad
	return mitad
    

def ajustar(nombre, sock, macs, verGrafica=False):
    import blescan
    print("Iniciando ajuste para ", nombre)
    maxima = input("Por favor, introduzca la distancia máxima\n")
    distancias = [1, ceil(maxima/2.),maxima]
    potencias = []

    for d in distancias:
        print("Por favor, póngase a " + str(d) + " metros de la baliza y pulse enter.")
        raw_input()
        print("Por favor, espere un momento...")
        listaBeacons = []
        while len(listaBeacons)<20:
            
            returnedList = blescan.parse_events_2(sock, macs, 10)
            for beacon in returnedList:
                print(beacon)
                mac, pwr = beacon.split(",")
                listaBeacons.append(float(pwr))
        potencias.append(sum(listaBeacons)/len(listaBeacons))
    
    print("Calculando función...")
    p0 = num.poly1d(num.polyfit(potencias,distancias,30))
    
    #if verGrafica:
    #    xp = num.array([-50, -68, -70, -72, -73, -74, -78, -80.82677989, -85, -85.40515262, -88.65355977, -89, -91.17322011, -92, -96, -98])
    #    
    #    print("Imprimiendo función")
    #    plt.plot(potencias,distancias,'r*', xp, p0(xp), '--')
    #    plt.ylim ( -1,10)
    #    plt.show()
    
    return p0

    
