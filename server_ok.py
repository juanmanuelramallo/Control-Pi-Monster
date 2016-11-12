from gpiozero import AngularServo, Motor, LED, DistanceSensor, PWMLED
# import pygame
# import sys
from time import sleep
import socket
import Enum


# VARIABLES GLOBALES

velocidad = 0.00	# Ciclo de trabajo para el motor (entre 0 y 1)
angulo = -13		# Angulo para el servo


# INICIALIZACIONES

# Motor
motor = Motor(20,21, pwm=True)
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

# Conexión TCP_IP
TCP_IP = '192.168.2.2'
TCP_PORT = 5005
BUFFER_SIZE = 40  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)
data = conn.recv(BUFFER_SIZE)
print("Recibió del control:", data)
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

	if velocidad > 0.25:
		velocidad -= 0.10
	elif velocidad <= 0.25:
		velocidad = 0
		estadoMotor = Motor.STANDBY

def desacelerar():
	global velocidad

	if velocidad > 0.25:
		velocidad -= 0.03
	elif velocidad <= 0.25:
		velocidad = 0
		estadoMotor = Motor.STANDBY

def derecha():
	global angulo

	if angulo >= 0:
		angulo = 0
		print("No da mas a derecha")
	elif angulo < 0:
		angulo += 1

def izquierda():
	global angulo

	if angulo <= -26:
		angulo = -26
		print("No da mas a izquierda")
	elif angulo > -26:
		angulo -= 1

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
	frontalDer.value = 0.5
	frontalIzq.value = 0.5

def luces_altas():
	frontalIzq.value = 1.0
	frontalDer.value = 1.0

def toogle_luz_giro_derecha():
	if estadoLucesGiro == LucesGiro.STANDBY or estadoLucesGiro == LucesGiro.IZQ:
		parpadear_giro_derecha()
		estadoLucesGiro = LucesGiro.DER
	elif estadoLucesGiro == LucesGiro.DER:
		frontalGiroDer.off()
		traseraGiroDer.off()
		estadoLucesGiro = LucesGiro.STANDBY
	elif estadoLucesGiro == LucesGiro.BALIZAS:
		print("Primero desactivar balizas")

def toogle_luz_giro_izquierda():
	if estadoLucesGiro == LucesGiro.STANDBY or estadoLucesGiro == LucesGiro.DER:
		parpadear_giro_izquierda()
		estadoLucesGiro = LucesGiro.IZQ
	elif estadoLucesGiro == LucesGiro.IZQ:
		apagar_giro_izquierda()
		estadoLucesGiro = LucesGiro.STANDBY
	elif estadoLucesGiro == LucesGiro.BALIZAS:
		print("Primero desactivar balizas")

def toogle_balizas():
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

while True:
	# Duerme por 50 milisegundos
	sleep(0.05)
	# c += 1

	motor.forward(velocidad)

	data = conn.recv(BUFFER_SIZE)

	# Gracias a python que no tiene switch-case les presento un gran if-elif statement
	# PRESIONA BOTON DE AVANZAR
	if data == b'B_Avanz':
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
	elif data == b'B_Retro':
		# Si el motor estaba quieto
		if estadoMotor == Motor.STANDBY:
			# Debe acelerar e ir hacia atrás
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
			motor.forward(velocidad)

	# PRESIONA GIRAR A DERECHA
	elif data == b'B_GiroDer':
		derecha()
		servo.angle = angulo

	# PRESIONA GIRAR A IZQUIERDA
	elif data == b'B_GiroIzq':
		izquierda()
		servo.angle = angulo

	# PRESIONA ENCENDER LUZ GIRO DERECHA
	elif data == b'B_LuzGiroDer':
		toogle_luz_giro_derecha()

	# PRESIONA ENCENDER LUZ GIRO IZQUIERDA
	elif data == b'B_LuzGiroIzq':
		toogle_luz_giro_izquierda()

	# PRESIONA ENCENDER BALIZAS
	elif data == b'B_Balizas':
		toogle_balizas()

	# PRESIONA ENCENDER LUCES
	elif data == b'B_Luces':
		toogle_luces()

	# EL CONTROL PIDE LA VELOCIDAD
	# elif data == b'SPEED':
	# 	data = bytes(str(velocidad), 'utf-8')

	########### termina el gran if-elif-elif-elif ... ###########

	# Echo to the client - al Monster Pi Pad
	# Si pidió la velocidad se le envia la velocidad
	conn.send(data)

	# Cada 100 milisegundos
	# Si no se presiono ninguna tecla para avanzar o retroceder el autito
	# deberá ir disminuyendo su velocidad lentamente hasta llegar a cero
	if data != b'B_Avanz' and data != b'B_Retro':
		if estadoMotor != Motor.STANDBY:
			desacelerar()
			if estadoMotor == Motor.ADELANTE:
				motor.forward(velocidad)
			elif estadoMotor == Motor.ATRAS:
				motor.backward(velocidad)
