#!/usr/bin/python
# coding=UTF-8

import socket
from time import sleep
from gpiozero import LED, Button

# Definición de botones
BotonRetro = Button(21)
BotonAcelerar = Button(20)
BotonLuzGiroDer = Button(16)
BotonLuzGiroIzq = Button(12)
BotonBalizas = Button(7)
BotonLuces = Button(8)
BotonGiroDer = Button(11)
BotonGiroIzq = Button(25)

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

Motor = Enum('STANDBY', 'ACELERANDO', 'FRENANDO', 'RETROCEDIENDO')
estado_motor = Motor.STANDBY
speed = 0

Giro = Enum('IZQ_ON', 'DER_ON', 'BALIZAS_ON', 'STANDBY')
estado_giro = Giro.STANDBY

while(1):

    # Puede frenar o acelerar pero no los dos al mismo tiempo
    if BotonRetro.is_pressed:
        # Si el motor está frenado y se pulsa el boton atras
        if estado_motor == Motor.STANDBY:
            s.send("RETROCEDER")
            speed = s.recv(BUFFER_SIZE)
            estado_motor = Motor.RETROCEDIENDO
        elif estado_motor == Motor.ACELERANDO
            s.send("FRENAR")
            speed = s.recv(BUFFER_SIZE)
            estado_motor = Motor.FRENANDO
            if speed == 0:
                estado_motor = Motor.STANDBY


        s.send("FRENAR")
        data = s.recv(BUFFER_SIZE)
        print("ECHO:", data)
    elif BotonAcelerar.is_pressed:
        s.send("ACELERAR")
        data = s.recv(BUFFER_SIZE)

    if BotonLuzGiroDer.is_pressed:
        if (estado_giro == Giro.STANDBY):
            print("Encender luz giro derecha")
            s.send("ENCENDER_LUZ_GIRO_DERECHA")
            estado_giro = Giro.DER_ON
        elif (estado_giro == Giro.DER_ON):
            print("Apagar luz de giro")
            s.send("APAGAR_LUZ_DE_GIRO")
            estado_giro = Giro.STANDBY
        data = s.recv(BUFFER_SIZE)
    elif BotonLuzGiroIzq.is_pressed:
        if (estado_giro == Giro.STANDBY):
            print("Encender luz giro izquierda")
            s.send("ENCENDER_LUZ_GIRO_IZQUIERDA")
            estado_giro = Giro.IZQ_ON
        elif (estado_giro == Giro.IZQ_ON):
            print("Apagar luz de giro izquierda")
            s.send("APAGAR_LUZ_DE_GIRO")
            estado_giro = Giro.STANDBY
        data = s.recv(BUFFER_SIZE)

    s.send("ACELERAR")
    data = s.recv(BUFFER_SIZE)
    print("received data:", data)

    sleep(2)

# s.close()
