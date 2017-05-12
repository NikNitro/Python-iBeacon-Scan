import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 5, 0.1);
y = np.sin(x)
print(plt.isinteractive())
plt.plot(x, y)
#plt.interactive(True)


#Para cambiar entre modo interactivo y no: plt.ion() y plt.ioff()
# Asi separado los pone con diferentes colores.
plt.scatter(0,3,c='b')
plt.scatter(1,4,c='b')
plt.scatter(2,4,c='b')
plt.scatter(3,3,c='b')
plt.scatter(4,2,c='b')
"""
# Asi todos en la misma lista los pone del mismo color
a = [0,1,2,3,4]
b = [3,4,4,3,2]
plt.scatter(a,b)
"""


if(plt.isinteractive()):
	print("era interactivo")


plt.show()


"""
plt.figure('scatter') # Crea una ventana titulada 'scatter'
plt.figure('plot')    # Crea una ventana titulada 'plot'
a = np.random.rand(100) # Generamos un vector de valores aleatorios
b = np.random.rand(100) # Generamos otro vector de valores aleatorios
plt.figure('scatter') # Le decimos que la ventana activa en la que vamos a dibujar es la ventana 'scatter'
plt.scatter(a,b)  # Dibujamos un scatterplot en la ventana 'scatter'
plt.figure('plot') # Ahora cambiamos a la ventana 'plot'
plt.plot(a,b)
"""