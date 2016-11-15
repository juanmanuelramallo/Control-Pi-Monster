from gpiozero import AngularServo, Motor, LED, DistanceSensor, PWMLED
# import pygame
# import sys
from time import sleep
import socket
from enum import Enum


# VARIABLES GLOBALES

velocidad = 0.00	# Ciclo de trabajo para el motor (entre 0 y 1)
angulo = -13		# Angulo para el servo


# INICIALIZACIONES

# Motor
motor = Motor(20,21)
motor.stop()

# Servo
servo = AngularServo(14, min_angle=-40, max_angle=40)
servo.angle = angulo

# Sensor
sensor = DistanceSensor(echo=18 , trigger=15 )

# Luces
frontalDer = PWMLED(2)
frontalIzq = PWMLED(3)
frontalGiroIzq = LED(17)
frontalGiroDer = LED(4)
traseraDer = LED(26)
traseraIzq = LED(16)
traseraGiroIzq = LED(13)
traseraGiroDer = LED(19)

# Conexion TCP_IP
TCP_IP = '192.168.43.163'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)
data = conn.recv(BUFFER_SIZE)
print("Recibio del control:", data)
conn.send("CONECTADO")

# Estados del motor
Motor = Enum('STANDBY', 'ADELANTE', 'ATRAS') # 'DESACELERANDO', 'FRENANDO')
estadoMotor = Motor.STANDBY
estadoMotorAnterior = estadoMotor

# Estados de las luces de giro
LucesGiro = Enum('IZQ', 'DER', 'BALIZAS', 'STANDBY')
estadoLucesGiro = LucesGiro.STANDBY

# Estados de las luces
Luces = Enum('STANDBY', 'ALTAS', 'BAJAS')
estadoLuces = Luces.STANDBY

# CODIGO PRINCIPAL
def acelerar():
	global velocidad

	if velocidad < 0.25:
		velocidad = 0.25
	elif velocidad <= 0.95:
		velocidad += 0.05
	elif velocidad > 0.95:
		velocidad = 1

def frenar():
	global velocidad
	global estadoMotor

	if velocidad > 0.25:
		velocidad -= 0.2
	elif velocidad <= 0.25:
		velocidad = 0
		estadoMotor = Motor.STANDBY

def desacelerar():
	global velocidad
	global estadoMotor

	if velocidad > 0.25:
		velocidad -= 0.1
	elif velocidad <= 0.25:
		velocidad = 0
		estadoMotor = Motor.STANDBY

def derecha():
	global angulo

	if angulo >= 0:
		angulo = 0
		print("No da mas a derecha")
	elif angulo < 0:
		angulo += 6

def izquierda():
	global angulo

	if angulo <= -26:
		angulo = -26
		print("No da mas a izquierda")
	elif angulo > -26:
		angulo -= 6

def vuelve_a_centro():
	global angulo

	if angulo > -13:
		angulo -= 3
	elif angulo < -13:
		angulo += 3

def parpadear_giro_derecha():
	frontalGiroDer.blink(0.5,0.5)
	traseraGiroDer.blink(0.5,0.5)

def apagar_giro_derecha():
	frontalGiroDer.off()
	traseraGiroDer.off()

def parpadear_giro_izquierda():
	frontalGiroIzq.blink(0.5,0.5)
	traseraGiroIzq.blink(0.5,0.5)

def apagar_giro_izquierda():
	frontalGiroIzq.off()
	traseraGiroIzq.off()

def apagar_luces():
	frontalDer.off()
	frontalIzq.off()

def luces_bajas():
	frontalDer.value = 0.15
	frontalIzq.value = 0.15

def luces_altas():
	frontalIzq.value = 1.0
	frontalDer.value = 1.0

def luces_traseras():
	traseraDer.value = 1.0
	traseraIzq.value = 1.0

def apagar_luces_traseras():
	traseraDer.off()
	traseraIzq.off()

def toogle_luz_giro_derecha():
	global estadoLucesGiro
	if estadoLucesGiro == LucesGiro.STANDBY or estadoLucesGiro == LucesGiro.IZQ:
		parpadear_giro_derecha()
		apagar_giro_izquierda()
		estadoLucesGiro = LucesGiro.DER
	elif estadoLucesGiro == LucesGiro.DER:
		frontalGiroDer.off()
		traseraGiroDer.off()
		estadoLucesGiro = LucesGiro.STANDBY
	elif estadoLucesGiro == LucesGiro.BALIZAS:
		print("Primero desactivar balizas")

def toogle_luz_giro_izquierda():
	global estadoLucesGiro
	if estadoLucesGiro == LucesGiro.STANDBY or estadoLucesGiro == LucesGiro.DER:
		parpadear_giro_izquierda()
		apagar_giro_derecha()
		estadoLucesGiro = LucesGiro.IZQ
	elif estadoLucesGiro == LucesGiro.IZQ:
		apagar_giro_izquierda()
		estadoLucesGiro = LucesGiro.STANDBY
	elif estadoLucesGiro == LucesGiro.BALIZAS:
		print("Primero desactivar balizas")

def toogle_balizas():
	global estadoLucesGiro
	if estadoLucesGiro == LucesGiro.BALIZAS:
		apagar_giro_izquierda()
		apagar_giro_derecha()
		estadoLucesGiro = LucesGiro.STANDBY
	else:
		apagar_giro_derecha()
		apagar_giro_izquierda()
		parpadear_giro_izquierda()
		parpadear_giro_derecha()
		estadoLucesGiro = LucesGiro.BALIZAS

def toogle_luces():
	global estadoLuces
	if estadoLuces == Luces.STANDBY:
		luces_bajas()
		estadoLuces = Luces.BAJAS
	elif estadoLuces == Luces.BAJAS:
		luces_altas()
		estadoLuces = Luces.ALTAS
	elif estadoLuces == Luces.ALTAS:
		apagar_luces()
		estadoLuces = Luces.STANDBY

# Contador para tiempo
# c = 0

# Comandos del buffer
c1 = ""
c2 = ""
c3 = ""
c4 = ""
comandos = ["","","",""]

def limpiar_comandos():
    global c1, c2, c3, c4, comandos
    c1 = ""
    c2 = ""
    c3 = ""
    c4 = ""
	comandos = ["","","",""]

def asignar_comandos(datos):
	global c1, c2, c3, c4, comandos
	longitud = len(datos)

	# Si se envio un comando (mide 5)
	if longitud > 3:
		c1 = datos[0:5]
		comandos[0] = c1
	if longitud > 5:
		c2 = datos[5:10]
		comandos[1] = c2
	if longitud > 10:
		c3 = datos[10:15]
		comandos[2] = c3
	if longitud > 15:
		c4 = datos[15:20]
		comandos[3] = c4

while True:
	# Duerme por 150 milisegundos
	sleep(0.15)
	# c += 1

	# print("Velocidad es: ", velocidad)
	# print("Distancia a objeto es: ", sensor.distance )

	# Bloqueante
	data = conn.recv(BUFFER_SIZE)

	# Busca comandos en el buffer y los guarda en un arreglo
	asignar_comandos(data)

	# Apaga luces traseras por si estuvieron encendidas durante un frenado
	if 'B_RET' not in comandos:
		apagar_luces_traseras()

	# Gracias a python que no tiene switch-case les presento un gran if-elif statement
	# PRESIONA BOTON DE AVANZAR
	if 'B_AVA' in comandos:
		# Si el motor estaba quieto
		if estadoMotor == Motor.STANDBY:
			# Debe acelerar e ir para adelante
			acelerar()
			motor.forward(velocidad)
			estadoMotorAnterior = estadoMotor
			estadoMotor = Motor.ADELANTE
		# Si el motor iba hacia adelante acelerando
		elif estadoMotor == Motor.ADELANTE:
			# Debe seguir haciendolo
			acelerar()
			motor.forward(velocidad)
		# Ahora bien, si el motor iba hacia atras
		elif estadoMotor == Motor.ATRAS:
			# Debe frenar desacelarando fuertemente
			frenar()
			motor.backward(velocidad)
	# PRESIONA BOTON DE RETROCEDER
	elif 'B_RET' in comandos:
		# Si el motor estaba quieto
		if estadoMotor == Motor.STANDBY:
			# Debe acelerar e ir hacia atras
			acelerar()
			motor.backward(velocidad)
			estadoMotor = Motor.ATRAS
		# Si el motor estaba yendo hacia atras
		elif estadoMotor == Motor.ATRAS:
			# Debe continuar haciendolo aumentando su velocidad
			acelerar()
			motor.backward(velocidad)
		# Si el motor iba hacia adelante
		elif estadoMotor == Motor.ADELANTE:
			# Debe primero frenar
			frenar()
			luces_traseras()
			motor.forward(velocidad)

	# PRESIONA GIRAR A DERECHA
	if 'B_GDE' in comandos:
		derecha()
		servo.angle = angulo
	# PRESIONA GIRAR A IZQUIERDA
	elif 'B_GIZ' in comandos:
		izquierda()
		servo.angle = angulo

	# PRESIONA ENCENDER LUZ GIRO DERECHA
	if 'B_LGD' in comandos:
		toogle_luz_giro_derecha()
	# PRESIONA ENCENDER LUZ GIRO IZQUIERDA
	elif 'B_LGI' in comandos:
		toogle_luz_giro_izquierda()
	# PRESIONA ENCENDER BALIZAS
	elif 'B_BAL' in comandos:
		toogle_balizas()

	# PRESIONA ENCENDER LUCES
	if 'B_LUC' in comandos:
		toogle_luces()

	# EL CONTROL PIDE LA VELOCIDAD
	# elif data == b'SPEED':
	# 	data = bytes(str(velocidad), 'utf-8')

	########### termina el gran if-elif-elif-elif ... ###########

	# Echo to the client - al Monster Pi Pad
	# Si pidio la velocidad se le envia la velocidad
	conn.send(data)

	# Cada 100 milisegundos
	# Si no se presiono ninguna tecla para avanzar o retroceder el autito
	# debera ir disminuyendo su velocidad lentamente hasta llegar a cero
	if 'B_AVA' in comandos and 'B_RET' in comandos:
		desacelerar()
		if estadoMotor == Motor.ADELANTE:
			motor.forward(velocidad)
		elif estadoMotor == Motor.ATRAS:
			motor.backward(velocidad)
		elif estadoMotor == Motor.STANDBY:
			motor.stop()

	# Cada ciclo va corrigiendo el angulo de la direccion para volver a 0
	if 'B_GDE' in comandos and 'B_GIZ' in comandos and 'B_AVA' in comandos and 'B_RET' in comandos:
		vuelve_a_centro()
		servo.angle = angulo

	# El sensor haciendo estragos
	if estadoMotor == Motor.ADELANTE:
		if( sensor.distance < 0.6 ):
			if( velocidad >= 0.7 ):
				motor.backward(velocidad)
				estadoMotor = Motor.ATRAS
				print("Objeto a distancia menor a 60cm - Velocidad ALTA - freno forzoso")
			else:
				motor.stop()
				luces_traseras()
				print("Objeto a distancia menor a 60cm - Velocidad baja: frena ")

	# Limpia el buffer de comandos
	limpiar_comandos()
	data = ""

# FIN DEL WHILE TRUE
