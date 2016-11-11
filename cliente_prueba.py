#!/usr/bin/python

import socket
# from gpiozero import LED, Button
from time import sleep
# from enum import Enum

# Connects the socket and send the first message "CONECTADO"
BUFFER_SIZE = 1024
s = None

def open_connection():
    TCP_IP = '192.168.2.2'
    TCP_PORT = 5005
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    m = "CONECTADO"
    s.send(m)
    data = s.recv(BUFFER_SIZE)
    print("Conexión aceptada:", data)

def send_command(cmd):
    s.send(cmd)
    data = s.recv(BUFFER_SIZE)
    return data

def close_connection():
    s.close()

def main():
    open_connection()

    m = "HOLA"
    r = send_command(m)
    print(r)

    m = "CHAU"
    r = send_command(m)
    print(r)

main()
