#!/usr/bin/env python3

import socket
import base64
import hashlib
from time import time, sleep
import sys

try:
 HOST = sys.argv[1]            # The server's hostname or IP address
 TCP_PORT = int(sys.argv[2])   # The port used by the server
 UDP_PORT = int(sys.argv[3])  
 USER=sys.argv[4] 
 CLIENT_IP = '127.0.0.1'
except:
  print('Error al introducir los argumentos. Asegurese de los introduzca de la forma:\nclient.py -HOST -TCP_PORT -UDP_PORT -USER\nDonde:\n  -HOST: string\n  -TCP_PORT: number\n  -UDP_PORT: number\n  -USER: string')
  exit()

def sendMessage(command, parameter=""):
  finalCommand = ""
  if parameter != "":
    finalCommand = bytes(command + ' ' + parameter,'utf-8')
  else:
    finalCommand = bytes(command,'utf-8')
  tcpSocket.sendall(finalCommand)
  return tcpSocket.recv(1024)

def listenForUdpMessage():
  timeToWait = time() + 20
  dataUDP=""
  checksum=""
  udpSocket.settimeout(20)
  try:
    dataUDP, addr = udpSocket.recvfrom(1024)
  except:
    print('Se agotó el tiempo de espera')
    closeConnection()
    exit()
  if dataUDP=="":
    print('No se recivió ningún mensaje')
    closeConnection()
    exit()
  else:
    m = hashlib.md5()
    m.update(base64.b64decode(dataUDP))
    checksum=m.hexdigest()
  return checksum, base64.b64decode(dataUDP).decode("utf-8")

def closeConnection():
  udpSocket.close()
  tcpSocket.close()

def main():
  print('\nObteniendo el mensaje...')
  # Initialize UDP socket
  global udpSocket
  try:
    udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udpSocket.bind((CLIENT_IP, UDP_PORT))
  except:
    print('Error al conectar con el servidor, revise que la direción IP y el puerto para conexión UDP esten correctos')
    exit()

  # Initialize TCP socket
  global tcpSocket
  try:
    tcpSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.connect((HOST, TCP_PORT))
  except:
    print('Error al conectar con el servidor, revise que la direción IP y el puerto para conexión TCP esten correctos')
    exit()


  # Executes helloiam command to authenticate the user
  receivedMessage = sendMessage('helloiam', USER)
  if receivedMessage == bytes('error invalid user name\n','utf-8'):
    print('Nombre de usuario no registrado en el servidor')
    exit()
  elif receivedMessage == bytes('error invalid src ip\n','utf-8'):
    print('La dirección IP del cliente no coincide con el registro del usuario')
    closeConnection()
    exit()


  # Executes msglen command to obtain message length
  receivedMessage = sendMessage('msglen')

  # Executes givememsg command to obtain message trought the UDP client
  receivedMessage = sendMessage('givememsg', str(UDP_PORT))


  # Executes enables the UDP client listener and returns the checksum
  checksum, message=listenForUdpMessage()

  # Executes chkmsg command to obtain validate the message is complete
  receivedMessage = sendMessage('chkmsg', checksum)
  if receivedMessage == bytes('error bad checksum\n','utf-8'):
    print('Ha ocurrido un error y no se ha recibido el mensaje completo')
    closeConnection()
    exit()

  # Executes bye command to close the connection
  receivedMessage = sendMessage('bye')

  print('Mensaje: ',message)
  closeConnection()

# Execute program
main()