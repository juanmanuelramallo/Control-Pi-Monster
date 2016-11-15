import socket
import select
import Queue

TCP_IP = '192.168.1.103'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.103', 5005))
s.send(m)
s.send("B_RET")
s.send("B_ACE")

# s.setblocking(0)
#
# inputs = [s]
# outpus = [s]
# message_queues = {}

s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
print("received data:", data)

MESSAGE = "FRENAR"
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
print("received data:", data)

# s.close()
