import socket
from time import sleep


TCP_IP = '192.168.2.2'
TCP_PORT = 5005
BUFFER_SIZE = 40  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)
while 1:
    data = conn.recv(BUFFER_SIZE)
    print("received data:", data)

    if data == b'ACELERAR':
        print("Hay que acelerar!")

    if data == b'FRENAR':
        print("Hay que frenar!")

    # data = bytes(str(BUFFER_SIZE))
    conn.send(data)  # echo
    sleep(0.1)
conn.close()
