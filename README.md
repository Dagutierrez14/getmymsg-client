# getmymsg-client
## Requisitos
Se utilizó la version 3.9 de Python por lo que debe instalarlo para correr el cliente.

## Incialización del Cliente
Se debe ubicar en la carpeta donde haya clonado el repositorio (aquella que contiene el archivo client.py) y luego debe ejecutar el siguiente comando:

`$ py client.py HOST TCP_PORT UDP_PORT USER`

o

`$ python client.py HOST TCP_PORT UDP_PORT USER`

Donde:
- **HOST**: es de tipo string y es la ip del servidor
- **TCP_PORT**: es de tipo int y es el puerto TCP por donde se realizará la conexión
- **UDP_PORT**: es de tipo int y es el puerto UDP por donde se realizará la conexión
- **USER**: es de tipo string y es l usuario utilizado en la autenticación

Ejemplo:

`$ python client.py 127.0.0.1 19876 5001 usuario_2`
