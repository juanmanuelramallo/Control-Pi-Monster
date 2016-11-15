import socket
from time import sleep


TCP_IP = '192.168.1.103'
TCP_PORT = 5005
BUFFER_SIZE = 40  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

c1 = ""
c2 = ""

print("INICIA SERVER")

conn, addr = s.accept()
print('Connection address:', addr)
while 1:
    print("RECIBE")
    data = conn.recv(BUFFER_SIZE)
    longitud = len(data)
    if longitud > 0:
        c1 = data[0:5]
    if longitud > 5:
        c2 = data[5:10]

    print("received data:", data)

    if c1 == b'B_ACE' or c2 == b'B_ACE':
        print("Hay que acelerar!")

    if c1 == b'B_RET' or c2 == b'B_RET':
        print("Hay que frenar!")

    if c1 == b'EXIT':
        print("CIERRA CONEXION")
        conn.close()
        break
    else:
        c1 = ""
        c2 = ""

        # data = bytes(str(BUFFER_SIZE))
        conn.send(data)  # echo
        sleep(3)
