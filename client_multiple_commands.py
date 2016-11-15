#!/usr/bin/python
# coding=UTF-8

import socket
from time import sleep
from gpiozero import LED, Button

# Definición de botones
B_RET = Button(21)
B_AVA = Button(20)
B_LGD = Button(16)
B_LGI = Button(12)
B_BAL = Button(7)
B_LUC = Button(8)
B_GDE = Button(11)
B_GIZ = Button(25)

# Definición de LEDs
LEDon = LED(5)
LEDstop = LED(6)
LEDluces = LED(13)
LEDgiroIzq = LED(19)
LEDgiroDer = LED(26)

# Configuración de conexión TCP/IP
TCP_IP = '192.168.43.163'
TCP_PORT = 5005
BUFFER_SIZE = 20
MESSAGE = b"CONECTAR"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
print("Recibio del autito:", data)

# Recibe la velocidad
speed = "0"
# Contador para tiempo
# c = 0
# Indicador si presionó al menos 1 botón
b = 0




while(1):
    # Duerme por 150 milisegundos
    sleep(0.15)
    # c += 1

    # AVANZAR O RETROCEDER
    if B_RET.is_pressed:
        s.send("B_RET")
        data = s.recv(BUFFER_SIZE)
        print("Botones motor :", data)
        b = 1
    elif B_AVA.is_pressed:
        s.send("B_AVA")
        data = s.recv(BUFFER_SIZE)
        print("Botones motor :", data)
        b = 1

    # GIRAR DERECHA O IZQUIERDA
    if B_GIZ.is_pressed:
        s.send("B_GIZ")
        data = s.recv(BUFFER_SIZE)
        print("Girando con :", data)
        b = 1
    elif B_GDE.is_pressed:
        s.send("B_GDE")
        data = s.recv(BUFFER_SIZE)
        print("Girando con :", data)
        b = 1

    # LUZ DE GIRO IZQ O DER O BALIZAS
    if B_LGI.is_pressed:
        s.send("B_LGI")
        data = s.recv(BUFFER_SIZE)
        print("Luz de giro/balizas :", data)
        b = 1
    elif B_LGD.is_pressed:
        s.send("B_LGD")
        data = s.recv(BUFFER_SIZE)
        print("Luz de giro/balizas :", data)
        b = 1
    elif B_BAL.is_pressed:
        s.send("B_BAL")
        data = s.recv(BUFFER_SIZE)
        print("Luz de giro/balizas :", data)
        b = 1

    # LUCES FRONTALES
    if B_LUC.is_pressed:
        s.send("B_LUC")
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
    #     print("La velocidad deluto es: ", speed)

    # Si no se presiono ningun boton
    if b == 0:
        # Envia la instrucción NOP
        # Para desbloquear la ejecución
        s.send("NOP")

    b = 0 # Reinicia el indicador


    # Pide estados del auto para los leds del control
    #### ####

# s.close()
