from fcntl import ioctl
from socket import socket, AF_INET, SOCK_DGRAM
from struct import pack



def obtener_mac(nom_interfaz):
    s = socket(AF_INET, SOCK_DGRAM)
    info = ioctl(s.fileno(), 0x8927,  pack('256s', nom_interfaz[:15]))
    return ':'.join(['%02X' % ord(char) for char in info[18:24]])