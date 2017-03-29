DEBUG = False

class Baliza:
   def __init__(self, nombre, mac, posX, posY):
      self.nombre = nombre
      self.mac    = mac
      self.posX   = posX
      self.posY   = posY


def readLine(file):
   s = file.readline()
   values = s.split("@")
   nombre = values(1)
   mac = values(2)
   posX = values(3)
   posY = values(4)
   baliza = Baliza(nombre, mac, posX, posY)
   return baliza

