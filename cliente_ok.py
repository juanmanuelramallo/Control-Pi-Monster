#!/usr/bin/python
# coding=UTF-8

import socket
from time import sleep
from gpiozero import LED, Button

# Definición de botones
B_Retro = Button(21)
B_Avanz = Button(20)
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
print("Recibió del autito:", data)

# Recibe la velocidad
speed = "0"
# Contador para tiempo
# c = 0
# Indicador si presionó al menos 1 botón
b = 0


while(1):
    # Duerme por 50 milisegundos
    sleep(0.05)
    # c += 1

    if B_Retro.is_pressed:
        s.send("B_Retro")
        data = s.recv(BUFFER_SIZE)
        print("Botones motor :", data)
        b = 1
    elif B_Avanz.is_pressed:
        s.send("B_Avanz")
        data = s.recv(BUFFER_SIZE)
        print("Botones motor :", data)
        b = 1

    elif B_GiroIzq.is_pressed:
        s.send("B_GiroIzq")
        data = s.recv(BUFFER_SIZE)
        print("Girando con :", data)
        b = 1
    elif B_GiroDer.is_pressed:
        s.send("B_GiroDer")
        data = s.recv(BUFFER_SIZE)
        print("Girando con :", data)
        b = 1

    elif B_LuzGiroIzq.is_pressed:
        s.send("B_LuzGiroIzq")
        data = s.recv(BUFFER_SIZE)
        print("Luz de giro/balizas :", data)
        b = 1
    elif B_LuzGiroDer.is_pressed:
        s.send("B_LuzGiroDer")
        data = s.recv(BUFFER_SIZE)
        print("Luz de giro/balizas :", data)
        b = 1
    elif B_Balizas.is_pressed:
        s.send("B_Balizas")
        data = s.recv(BUFFER_SIZE)
        print("Luz de giro/balizas :", data)
        b = 1

    elif B_Luces.is_pressed:
        s.send("B_Luces")
        data = s.recv(BUFFER_SIZE)
        print("Luces :", data)
        b = 1

    # cada 500 ms
    # elif ( c == 5 ):
    #     c = 0
    #     # Pide la velocidad
    #     s.send("SPEED")
    #     data = s.recv(BUFFER_SIZE)
    #     speed = str(data)
    #     print("La velocidad del auto es: ", speed)

    # Si no se presiono ningun boton
    if b == 0:
        # Envia la instrucción NOP
        # Para desbloquear la ejecución
        s.send("NOP")

    b = 0 # Reinicia el indicador


    # Pide estados del auto para los leds del control
    #### ####

# s.close()
