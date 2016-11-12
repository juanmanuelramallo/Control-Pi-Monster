from gpiozero import LED, Button
from time import sleep

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

while(1):
    if BotonFrenar.is_pressed:
        print("Freno activado")
        LEDstop.on()
    elif BotonAcelerar.is_pressed:
        print("Acelerar")
        LEDstop.off()
    elif BotonLuzGiroDer.is_pressed:
        print("Luz giro derecha")
        LEDstop.off()
        LEDgiroDer.blink(0.5,0.3)
    elif BotonLuzGiroIzq.is_pressed:
        print("Luz giro izquierda")
        LEDstop.off()
        LEDgiroIzq.blink(0.5,0.3)
    elif BotonBalizas.is_pressed:
        print("Balizas")
        LEDgiroIzq.blink(0.5,0.3)
        LEDgiroDer.blink(0.5,0.3)
    elif BotonLuces.is_pressed:
        print("Luces")
        LEDluces.on()
    elif BotonGiroDer.is_pressed:
        print("Girar derecha")
    elif BotonGiroIzq.is_pressed:
        print("Girar izquierda")

    sleep(0.2)
