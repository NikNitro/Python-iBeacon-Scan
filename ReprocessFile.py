# -*- coding: utf-8 -*-
import socket
import time
import sys
from datetime import timedelta

PUERTO = 5010
SERVER = '192.168.31.116'
REALISTICMODE = True

lastTime=-1
newTime=-1


infile=open("centralLog.aml", "r")
primera = True
#Para cada linea del log 
for line in infile:
  #En la primera solo esta la fecha
  if(primera):
    primera = False
    print(line)

    #Aqui se ejecuta lo importante
  else:
    #print("---" + str(int(line[0:2])) + " "+ str(int(line[3:5]))+ " "+str(int(line[6:8])))
    newTime = timedelta(hours=int(line[0:2]), minutes=int(line[3:5]), seconds=int(line[6:8]))
    if(lastTime==-1 or not REALISTICMODE):
      lastTime=newTime


    else:
      a = (newTime-lastTime).total_seconds()
      #print(str(a))
      time.sleep(a) # Tengo que restar los dos tiempos. Esperar y luego (fuera del ifelse) envial por socket
      lastTime=newTime

    #Tras definir la espera, vamos a enviar los datos a la central:
    #print(line[-40: -1])

    #Conectarlo a la central
    socket_c = socket.socket()  
    socket_c.connect((SERVER, PUERTO))  
    socket_c.send(line[9: -1].encode('utf-8'))
    socket_c.close()
"""
socket_c = socket.socket()  
socket_c.connect((SERVER, PUERTO))  
socket_c.send('END')
"""
socket_c.close()
infile.close()
