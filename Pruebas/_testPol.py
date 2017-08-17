# -*- coding: utf-8 -*-
import Posicionar as pos
from math import *
from sympy import *
""" Prueba para eliminar complejos """
c1 = 4 + 3j
print(type(c1))
if(type(c1) != complex):
	print('no complejo')
else:
	print('complejo')
# .real y .imag nos da las partes reales e imaginarias de un numero
print(str(c1.real) + " " + str(c1.imag))
e1 = 5

print("Ahora el real: " + str(e1.real) + " " + str(e1.imag))

#Por tanto
if(e1.imag == 0):
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