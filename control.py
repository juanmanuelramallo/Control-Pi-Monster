import socket
from gpiozero import LED, Button
from time import sleep
from enum import Enum

# Connects the socket and send the first message "CONECTADO"
def open_connection():
    TCP_IP = '192.168.1.111'
    TCP_PORT = 5005
    global BUFFER_SIZE = 1024
    global s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send("CONECTADO")
    data = s.recv(BUFFER_SIZE)
    print "Conexión aceptada:", data

def send_command(cmd):
    s.send(cmd)
    data = s.recv(BUFFER_SIZE)
    return data

def close_connection():
    s.close()

def main():
    init_socket()
    open_connection()

    BotonFrenar = Button(21)
    BotonAcelerar = Button(20)
    BotonLuzGiroDer = Button(16)
    BotonLuzGiroIzq = Button(12)
    BotonBalizas = Button(7)
    BotonLuces = Button(8)
    BotonGiroDer = Button(11)
    BotonGiroIzq = Button(25)

    LEDon = LED(5)
    LEDstop = LED(6)
    LEDluces = LED(13)
    LEDgiroIzq = LED(19)
    LEDgiroDer = LED(26)

    speed = 0

    # estado = Enum('STOPPED', 'ACELERANDO', 'RETROCEDIENDO', 'FRENANDO')
    # estado_actual = estado.STOPPED
    # estado_anterior = estado_actual

    estado_luces = Enum('LUCES_HIGH', 'LUCES_MID', 'LUCES_OFF', 'STANDBY')
    estado_luces_actual = estado_luces.STANDBY
    # estado_luces_anterior = estado_actual

    estado_giro = Enum('IZQ_ON', 'DER_ON', 'BALIZAS_ON', 'STANDBY')
    estado_giro_actual = estado_giro.STANDBY

    while(1):
        if BotonFrenar.is_pressed:
            print("Freno activado")
            send_command("FRENAR")

            # estado_anterior = estado_actual
            # estado_actual = estado.FRENANDO

            estado_actual = estado.FRENANDO

        elif BotonAcelerar.is_pressed:
            print("Acelerar")
            send_command("ACELERAR")

            # estado_actual = estado.STANDBY

        if BotonLuzGiroDer.is_pressed:
            if (estado_giro_actual == estado_giro.STANDBY):
                print("Encender luz giro derecha")
                send_command("ENCENDER_LUZ_GIRO_DERECHA")
                estado_giro_actual = estado_giro.DER_ON
            elif (estado_giro_actual == estado_giro.DER_ON):
                print("Apagar luz de giro")
                send_command("APAGAR_LUZ_DE_GIRO")
                estado_giro_actual = estado_giro.STANDBY

        elif BotonLuzGiroIzq.is_pressed:
            if (estado_giro_actual == estado_giro.STANDBY):
                print("Encender luz giro izquierda")
                send_command("ENCENDER_LUZ_GIRO_IZQUIERDA")
                estado_giro_actual = estado_giro.IZQ_ON
            elif (estado_giro_actual == estado_giro.IZQ_ON):
                print("Apagar luz de giro izquierda")
                send_command("APAGAR_LUZ_DE_GIRO")
                estado_giro_actual = estado_giro.STANDBY

        elif BotonBalizas.is_pressed:
            if (estado_giro_actual == estado_giro.STANDBY):
                print("Encender balizas")
                send_command("ENCENDER_BALIZAS")
                estado_giro_actual = estado_giro.BALIZAS_ON
            elif (estado_giro_actual == estado_giro.BALIZAS_ON):
                print("Apagar balizas")
                send_command("APAGAR_LUZ_DE_GIRO")
                estado_giro_actual = estado_giro.STANDBY

        if BotonLuces.is_pressed:
            if (estado_actual == estado.LUCES_OFF):
                print("Luz media")
                send_command("ENCENDER_LUCES_MID")
                estado_actual = estado.LUCES_MID
            elif (estado_actual == estado.LUCES_MID):
                print("Luz alta")
                send_command("ENCENDER_LUCES_HIGH")
                estado_actual = estado.LUCES_HIGH
            elif (estado_actual == estado.LUCES_HIGH):
                print("Luz apagada")
                send_command("APAGAR_LUCES")
                estado_actual = estado.LUCES_OFF

        if BotonGiroDer.is_pressed:
            print("Girar derecha")
            send_command("GIRAR_DERECHA")
        elif BotonGiroIzq.is_pressed:
            print("Girar izquierda")
            send_command("GIRAR_IZQUIERDA")

        sleep(0.1)
