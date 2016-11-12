from gpiozero import Button

BotonFrenar = Button(21)
BotonAcelerar = Button(20)
BotonLuzGiroDer = Button(16)
BotonLuzGiroIzq = Button(12)
BotonBalizas = Button(7)
BotonLuces = Button(8)
BotonGiroDer = Button(11)
BotonGiroIzq = Button(25)

while(1):
    if BotonFrenar.is_pressed:
        print("Freno activado")
    elif BotonAcelerar.is_pressed:
        print("Acelerar")
    elif BotonLuzGiroDer:
        print("Luz giro derecha")
    elif BotonLuzGiroIzq:
        print("Luz giro izquierda")
    elif BotonBalizas:
        print("Balizas")
    elif BotonLuces:
        print("Luces")
    elif BotonGiroDer:
        print("Girar derecha")
    elif BotonGiroIzq:
        print("Girar izquierda")
