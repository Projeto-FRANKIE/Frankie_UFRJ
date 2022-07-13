#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import wisardpkg as wp
import cv2
import RPi.GPIO as GPIO
#
from time import *
import time    #OKOKOOK
import sys

from picamera import PiCamera
from time import sleep

import Adafruit_GPIO.SPI as SPI    
import Adafruit_SSD1306    

from PIL import Image    
from PIL import ImageDraw    
from PIL import ImageFont    

#Tela OLED
disp = Adafruit_SSD1306.SSD1306_128_64(rst=23)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('fonte.ttf', 10)

draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((28, 12), 'FRANKIE UFRJ',  font=font, fill=255) #x de 0 a 127 e y de 0 a 63
draw.text((28, 36), 'IA na Escola', font=font, fill=255)
disp.image(image)
disp.display()
disp.display()

#Interações

def speak(text, speed):
    for i in range(len(text)):
        print(text[i], sep='', end='', flush=True);
        sleep(speed)


#Câmera --------------------------------------
def connect_cam(source):
    cam = cv2.VideoCapture(source)
    if cam is None or not cam.isOpened():
        print("Atenção: a câmera de indice " + str(source) + " não está disponível")
        sys.exit(1) #alterei
    else:
        cv2.namedWindow("Imagem")
        ret,frame = cam.read()      
        cv2.imshow("Imagem", frame)
        k = cv2.waitKey(1) #alterei
        return cam

#Reconhecimento Imagem --------------------------------------
def get_pic_and_rec(camera):
    Z=[]
    print("Obtendo foto...")
    for i in range (100): #fica mostrando a imagem durante um tempo antes de fotografar
        ret,frame = camera.read()       
        cv2.imshow("Imagem", frame)
        k = cv2.waitKey(1) #alterei

    retorno_tratamento = process_image (frame) #tenta isolar a imagem dentro do foto
    image_to_rec = retorno_tratamento['imagem']
    resultado = retorno_tratamento['resultado']
    if resultado == 0:
        #transforma a imagem da openCV em um vetor de entrada para WiSARD
        input_data = [(1 if e==255 else 0) for e in image_to_rec.flatten()]
        Z.append(input_data)
        dn=0  
        for e in image_to_rec.flatten():
            if e != 0:
                dn=1
                break
        if dn == 0:
            return ["N/B", "0"]
        else: #senão gerou uma imagem toda preta, diz o que reconheceu
            image_id_conf = recognize(Z)
            #Verifica confiança da imagem
            if image_id_conf[1] < 0.20:
                return ["N/A", "0"]
            else:
                return recognize(Z)
    else:
        return ["N/C", "0"]      

def switch_class_name(class_number):
    switcher = {1: "Triângulo",2: "Círculo",3: "Estrela",4: "Quadrado",}    
    return switcher.get(class_number)

def train_wisard (wisard):
    X=[]
    y=[]
    print ("Treinando WiSARD...")
    for i in range(1,4):   # Alterar de acordo com o número de classes
        for j in range(1,11):  # Alterar de acordo com o número de imagens de treino
            print ("Carregado classe " + str(i) +" exemplar " + str(j))
            file = 'quatro_classes_scan/classe_'+str(i) +'/picture_' + str(j)+'.bmp'
            img = cv2.imread(file,0)
            _,img = cv2.threshold(img,125,255,cv2.THRESH_BINARY) #INCLUIR
            img = cv2.resize(img,(110, 110)) #128x128
            input_data = [(1 if e==255 else 0) for e in img.flatten()]
            X.append(input_data)
            y.append(switch_class_name (i))
        wisard.train(X,y)

def recognize (vector):
    out = wsd.classify(vector)
    return [out[0]["class"],out[0]["confidence"]]
        
def process_image(initial_image):
    
    #Transforma a imagem em preto e branco
    image_gray = cv2.cvtColor(initial_image, cv2.COLOR_BGR2GRAY)
    _,image_thresh = cv2.threshold(image_gray,50,255,cv2.THRESH_BINARY)
    image_risized = cv2.resize(image_thresh,(110,110)) #128x128
    
    #escreve a imagem no disco para poder inverter
    cv2.imwrite("image.bmp", image_risized) 
    
    #inverte a imagem
    inverted_image= cv2.imread("image.bmp")
    inverted_image[inverted_image == 255] = 1
    inverted_image[inverted_image == 0] = 255
    inverted_image[inverted_image == 1] = 0
    
    #prepara a imagem para ser usada no findContours
    inverted_image_gray = cv2.cvtColor(inverted_image,cv2.COLOR_BGR2GRAY)
    ret,inverted_image_tresh = cv2.threshold(inverted_image_gray,127,255,0)
    #so controle para ver o resultado da trasnformaçao
    cv2.imwrite("inverted_image.bmp", inverted_image_tresh) 
    
    #encontra as coordenadas da figura geometrica dentro da imagem capturada
    #contours, hierarchy = cv2.findContours(inverted_image_tresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    try:
        im2,contours, hierarchy = cv2.findContours(inverted_image_tresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        x,y,w,h = cv2.boundingRect(cnt)
        #recorda e cria uma nova imagem somente com a figura geometrica
        ret,inverted_image = cv2.threshold(inverted_image,0,255,cv2.THRESH_BINARY_INV)  
        detected_image = inverted_image[y:y+h,x:x+w]
        detected_image = cv2.cvtColor(detected_image,cv2.COLOR_BGR2GRAY) 
        _,detected_image = cv2.threshold(detected_image,50,255,cv2.THRESH_BINARY)        
        #redimensiona a imagem
        detected_image_risized = cv2.resize(detected_image,(110, 110)) #128x128
        result=0
    except:
        detected_image_risized = cv2.resize(inverted_image_tresh,(110, 110)) #128x128
        result=1
        
    #so controle para ver o resultado da trasnformaçao
    cv2.imwrite("detected_image_risized.bmp", detected_image_risized)               
        
    return {"imagem":detected_image_risized,"resultado":result}

#Funções para simplificar comandos --------------------------------------------------------------------

def lerUltrassom (trigger, echo):
    GPIO.output (trigger, 1)
    time.sleep (0.00001)
    GPIO.output (trigger, 0)

    while GPIO.input(echo) == 0:
        pass
    start = time.time()

    while GPIO.input(echo) == 1:
        pass
    stop = time.time()

    return ((stop - start) * 17000)

def irFrente ():
    motor_pwm1.start(75)#75
    motor_pwm2.start(75)
    GPIO.output(17,1)
    GPIO.output(22,0)
    GPIO.output(27,1)
    GPIO.output(23,0)
    
def irTras ():
    motor_pwm1.start(100)#75
    motor_pwm2.start(100)
    GPIO.output(17,0)
    GPIO.output(22,1)
    GPIO.output(27,0)
    GPIO.output(23,1)
    
def irDireita ():
    motor_pwm1.start(100)#75
    motor_pwm2.start(100)
    GPIO.output(17,0)
    GPIO.output(22,0)#0
    GPIO.output(27,1)
    GPIO.output(23,0)
    
def irEsquerda ():
    motor_pwm1.start(100)#75
    motor_pwm2.start(100)
    GPIO.output(17,1)
    GPIO.output(22,0)
    GPIO.output(27,0)
    GPIO.output(23,0)#0
    
def parar ():
    motor_pwm1.start(0)#75
    motor_pwm2.start(0)
    GPIO.output(17,0)
    GPIO.output(22,0)
    GPIO.output(27,0)
    GPIO.output(23,0)

#Inicializações --------------------------------------------------------------------

#Motores DC
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Direita
GPIO.setup(17,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.output(17,0)
GPIO.output(22,0)
#Esquerda
GPIO.setup(27,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.output(27,0)
GPIO.output(23,0)

#Velocidades
GPIO.setup(19,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
motor_pwm1 = GPIO.PWM(19, 100)
motor_pwm2 = GPIO.PWM(16, 100)

#Servo
servoPIN = 25
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM (servoPIN, 50) # GPIO 17 for PWM with 50Hz
#p.start (8.5) # Iniciar servo
time.sleep (1)
p.stop ()

#Sensores de ultrassom
TriggerEsq = 9
EchoEsq = 11
GPIO.setup (TriggerEsq, GPIO.OUT)
GPIO.output (TriggerEsq, 0)
GPIO.setup (EchoEsq, GPIO.IN)

TriggerMeio = 14
EchoMeio = 15
GPIO.setup (TriggerMeio, GPIO.OUT)
GPIO.output (TriggerMeio, 0)
GPIO.setup (EchoMeio, GPIO.IN)

TriggerDir = 18
EchoDir = 24
GPIO.setup (TriggerDir, GPIO.OUT)
GPIO.output (TriggerDir, 0)
GPIO.setup (EchoDir, GPIO.IN)

#Distância para ser usado como comparação (ATEN
maxDistancia = 4

#Camera     
cam_id = 0
cam = connect_cam(cam_id)
print ('Câmera Ligada')

#Wisard
addressSize = 3
ignoreZero  = False
verbose = True
returnConfidence = True
bleachingActivated = True
wsd = wp.Wisard(addressSize, ignoreZero=ignoreZero, verbose=verbose,returnConfidence=returnConfidence,bleachingActivated=bleachingActivated)
#print('verbose:',verbose)
#print('bleaching:',bleachingActivated)
train_wisard(wsd)

while True:
    
    #Medir distância do ultrassom
    if lerUltrassom (TriggerMeio, EchoMeio) < maxDistancia:
        
        parar ()
        
        print("Reconhecendo...")
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((20, 24), 'Reconhecendo...',  font=font, fill=255) #x de 0 a 127 e y de 0 a 63
        disp.image(image)
        disp.display()
        image_id_conf = get_pic_and_rec(cam)
        
        print ("Forma determinada: " + str( image_id_conf[0]) + " - Confiança: %.5s" % (image_id_conf[1] * 100) + "%")
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((8, 12), "Forma: " + str( image_id_conf[0]),  font=font, fill=255) #x de 0 a 127 e y de 0 a 63
        draw.text((8, 36), "Confiança: %.5s" % (image_id_conf[1] * 100) + "%", font=font, fill=255)
        disp.image(image)
        disp.display()
       
        if str( image_id_conf[0]) == "Triângulo":
            time.sleep (2)
            irFrente ()
            time.sleep (2)
            parar ()
        if str( image_id_conf[0]) == "Círculo":
            time.sleep (2)
            irDireita ()
            time.sleep (1)
            parar ()
        if str( image_id_conf[0]) == "Estrela":
            time.sleep (2)
            irEsquerda ()
            time.sleep (1)
            parar ()
        #if str( image_id_conf[0]) == "Estrela":
        #   time.sleep (2)
        #    irTras ()
        #    time.sleep (1)
        #    parar ()
        time.sleep (5.0)
        resultado = 999

cam.release()
cv2.destroyWindow("Imagem")