import socket

BUFFER_SIZE = 20 # Normally 1024, but we want fast response
s = None

def open_connection():
    TCP_IP = '192.168.2.2'
    TCP_PORT = 5005
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

def main():
    open_connection()

    m = "HELLO"
    conn, addr = s.accept()
    print('Connection address:', addr)

    while 1:
        data = conn.recv(BUFFER_SIZE)
        print(data)
        conn.send(m)

    conn.close()

main()
