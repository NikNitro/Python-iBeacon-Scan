# -*- coding: utf-8 -*-

import Posicionar as p
from sympy import *
x=Symbol('x') 
y=Symbol('y')

distancias = [ x**2 - 200*x + y**2 - 400*y - 40000, x**2 - 800*x + y**2 - 10*y + 122000, x**2 - 1100*x + y**2 - 500*y + 340000, x**2 - 800*x + y**2 - 840*y + 288000]
p.Posicionar(distancias)