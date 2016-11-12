#!/usr/bin/python
# coding=UTF-8

import socket
from time import sleep
from gpiozero import LED, Button

# Definición de botones
B_Retro = Button(21)
B_Acel = Button(20)
B_LuzGiroDer = Button(16)
B_LuzGiroIzq = Button(12)
B_Balizas = Button(7)
B_Luces = Button(8)
B_GiroDer = Button(11)
B_GiroIzq = Button(25)

# Definición de LEDs
LEDon = LED(5)
LEDstop = LED(6)
LEDluces = LED(13)
LEDgiroIzq = LED(19)
LEDgiroDer = LED(26)

# Configuración de conexión TCP/IP
TCP_IP = '192.168.2.2'
TCP_PORT = 5005
BUFFER_SIZE = 40
MESSAGE = "CONECTAR"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
print("received data:", data)

speed = 0


while(1):

    if B_Retro.is_pressed:
        s.send("B_Retro")
        data = s.recv(BUFFER_SIZE)
        print("Botones motor :", data)
    elif B_Acel.is_pressed:
        s.send("B_Acel")
        data = s.recv(BUFFER_SIZE)
        print("Botones motor :", data)

    if B_GiroIzq.is_pressed:
        s.send("B_GiroIzq")
        data = s.recv(BUFFER_SIZE)
        print("Girando con :", data)
    elif B_GiroDer.is_pressed:
        s.send("B_GiroDer")
        data = s.recv(BUFFER_SIZE)
        print("Girando con :", data)

    if B_LuzGiroIzq.is_pressed:
        s.send("B_LuzGiroIzq")
        data = s.recv(BUFFER_SIZE)
        print("Luz de giro/balizas :", data)
    elif B_LuzGiroDer.is_pressed:
        s.send("B_LuzGiroDer")
        data = s.recv(BUFFER_SIZE)
        print("Luz de giro/balizas :", data)
    elif B_Balizas.is_pressed:
        s.send("B_Balizas")
        data = s.recv(BUFFER_SIZE)
        print("Luz de giro/balizas :", data)

    if B_Luces.is_pressed:
        s.send("B_Luces")
        data = s.recv(BUFFER_SIZE)
        print("Luces :", data)

    # Pide la velocidad
    s.send("SPEED")
    data = s.recv(BUFFER_SIZE)
    speed = int(data)

    # Pide estados del auto para los leds del control

    sleep(0.1)

# s.close()
