from gpiozero import AngularServo, Motor, LED, DistanceSensor
# import pygame
# import sys
from time import sleep
import socket


# VARIABLES GLOBALES

velocidad = 0.00	# Ciclo de trabajo para el motor (entre 0 y 1)
angulo = -13		# Angulo para el servo


# INICIALIZACIONES

# Pygame
# pygame.init()
# pygame.display.set_mode((100, 100))

# Motor
motor = Motor(20,21, pwm=True)
motor.stop()

# Servo
servo = AngularServo(14, min_angle=-40, max_angle=40)
servo.angle = angulo

# Sensor
sensor = DistanceSensor(echo=18 , trigger=15 )

# Luces
frontalDer = LED(2)
frontalIzq = LED(3)
frontalGiroIzq = LED(17)
frontalGiroDer = LED(4)
traseraDer = LED(26)
traseraIzq = LED(16)
traseraGiroIzq = LED(13)
traseraGiroDer = LED(19)


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

def desacelerar():
	global velocidad

	if velocidad > 0.25:
		velocidad -= 0.01
	elif velocidad <= 0.25:
		velocidad = 0

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




while True:
	sleep(0.2)

	desacelerar()
	motor.forward(velocidad)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				acelerar()
				motor.forward(velocidad)
			elif event.key == pygame.K_s:
				frenar()
				traseraDer.blink(0.5,0,1,True)
				traseraIzq.blink(0.5,0,1,True)
				motor.forward(velocidad)
			elif event.key == pygame.K_a:
				izquierda()
				servo.angle = angulo
			elif event.key == pygame.K_d:
				derecha()
				servo.angle = angulo
			elif event.key == pygame.K_l:
				frontalDer.on()
				frontalIzq.on()
			elif event.key == pygame.K_k:
				frontalIzq.off()
				frontalDer.off()
			elif event.key == pygame.K_m:
				frontalGiroIzq.blink(0.5,0.5,5,True)
				traseraGiroIzq.blink(0.5,0.5,5,True)
			elif event.key == pygame.K_n:
				frontalGiroDer.blink(0.5,0.5,5,True)
				traseraGiroDer.blink(0.5,0.5,5,True)
