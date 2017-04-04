# -*- coding: utf-8 -*-
import socket

PUERTO = 5010
socket_s = socket.socket()

#El socket se puede dejar vacío
socket_s.bind(('', PUERTO))

#Listen recibe el número máximo de conexiones simultáneas
socket_s.listen(3);

nombre, nose, ip = socket.gethostbyname_ex(socket.gethostname())
print "Sistema '",nombre, "' esperando conexión en el puerto ", PUERTO
#print "Y en la dirección ", ip[0]

while(True):
	socket_c, (host_c, puerto_c) = socket_s.accept()
	#accept se mantiene a la espera de conexiones entrantes, bloqueando la ejecución hasta que llega un mensaje

	recibido = socket_c.recv(8000)
	while(recibido!='END'):
		print "Recibido de ", host_c, " el mensaje", recibido
		recibido = socket_c.recv(8000)
		if not recibido: break
	#socket_c.send("200")

	#socket_c.close()

socket_s.close()