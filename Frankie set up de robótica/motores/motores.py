import RPi.GPIO as GPIO
import time


#Programação Nova
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Esquerda
GPIO.setup(13,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.output(13,0)
GPIO.output(16,0)
#Direita
GPIO.setup(11,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.output(11,0)
GPIO.output(15,0)

#Velocidades
GPIO.setup(35,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)
motor_pwm1 = GPIO.PWM(35, 100)
motor_pwm1.start(100) #motor esquerdo
motor_pwm2 = GPIO.PWM(36, 100) #motor direito
motor_pwm2.start(100)

while True:
    GPIO.output(11,0)
    GPIO.output(15,0)
    GPIO.output(13,0)
    GPIO.output(16,0)
    
    N = input("Direcao:")
    if N == "t":
        GPIO.output(11,0)
        GPIO.output(15,1)
        GPIO.output(13,0)
        GPIO.output(16,1)
        time.sleep (1.0)
    elif N == "f":
        GPIO.output(11,1)
        GPIO.output(15,0)
        GPIO.output(13,1)
        GPIO.output(16,0)
        time.sleep (1.0)
    elif N == "d":
        GPIO.output(11, 0)
        GPIO.output(15, 0)
        GPIO.output(13, 1)
        GPIO.output(16, 0)
        time.sleep(0.5)
    elif N == "e":
        GPIO.output(11, 1)
        GPIO.output(15, 0)
        GPIO.output(13, 0)
        GPIO.output(16, 0)
        time.sleep(0.5)
    elif N == "e1":
        GPIO.output(11,0)
        GPIO.output(15,1)
        GPIO.output(13,0)
        GPIO.output(16,0)
        time.sleep (0.5)
    elif N == "d1":
        GPIO.output(11,0)
        GPIO.output(15,0)
        GPIO.output(13,0)
        GPIO.output(16,1)
        time.sleep (0.5)
GPIO.cleanup()