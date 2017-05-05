# -*- coding: utf-8 -*-
import Posicionar as pos
from math import *
from sympy import *
""" Prueba para eliminar complejos """
c1 = 4 + 3j
if(type(c1) != complex):
	print('no complejo')
else:
	print('complejo')

""" end prueba """


""" It is a little code to prove that Posicionar function works """

x=Symbol('x') 
y=Symbol('y')

#Supongamos la baliza en el 100 0

distancias = []

A = int(0)
B = int(200)
C = sqrt(pow(200,2) + pow(100,2))

polinomio = x**2 + y**2 - 2*A*x - 2*B*y + (A**2 + B**2 - C**2)
distancias.append(polinomio)

A = int(100)
B = int(150)
C = 10

polinomio = x**2 + y**2 - 2*A*x - 2*B*y + (A**2 + B**2 - C**2)
distancias.append(polinomio)

A = int(200)
B = int(50)
C = sqrt(pow(100,2)+pow(50,2))

polinomio = x**2 + y**2 - 2*A*x - 2*B*y + (A**2 + B**2 - C**2)
distancias.append(polinomio)

posicionFinal = pos.Posicionar(distancias)