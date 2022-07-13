#Bibliotecas
import RPi.GPIO as GPIO
from time import *
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
#set GPIO Pins


#CENTRO
GPIO_TRIGGER = 8
GPIO_ECHO = 10
 
#set GPIO direction (IN / OUT)
GPIO.setwarnings(False) # Inclui
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.output(GPIO_TRIGGER,0)

GPIO.setup(GPIO_ECHO, GPIO.IN)
 
time.sleep(0.1)

print ("Medindo")

GPIO.output(GPIO_TRIGGER,1)
time.sleep(0.00001)
GPIO.output(GPIO_TRIGGER,0)

while GPIO.input(GPIO_ECHO) == 0:
    pass
start = time.time()

while GPIO.input(GPIO_ECHO) == 1:
    pass
stop = time.time()

print ((stop - start)*17000)

resultado = (stop - start)*17000


GPIO.cleanup()
