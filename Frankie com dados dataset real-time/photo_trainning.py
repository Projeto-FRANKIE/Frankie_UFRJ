# import python os module
import os

# importing the python open cv library
import cv2

# interaction
print('Bem-vind@ ao script de fotos de treinamento do robô Frankie!')
num_fotos = int(input('Para iniciar, digite o número de fotos que deseja capturar:'))
num_classes = int(input('Agora, digite o número de classes que deseja classificar:'))
input('Uma janela de captura de fotos irá aparecer agora. Pressione a tecla barra de espaço para capturar a foto. Para sair, pressione a tecla "ESC". Ok?')

# remove previously created frankie training data folders
os.system('rm -rf quatro_classes_scan')

# create frankie training folders
os.system('mkdir quatro_classes_scan')
for i in range(1,num_classes+1): 
    os.system('mkdir quatro_classes_scan/classe_'+str(i))

# intialize the webcam and pass a constant which is 0
cam = cv2.VideoCapture(0)

# title of the app
cv2.namedWindow(' de fotos para o treinamento do Frankie')

# let's assume the number of images gotten is 0
img_counter = 0

# loop until we have the required number of images in each classes folder
for i in range(num_classes):
    while img_counter < num_fotos:
        # get the image from the webcam
        ret, frame = cam.read()
        # show the image
        cv2.imshow(' de fotos para o treinamento do Frankie', frame)
        # if the user presses the spacebar, then the image is captured
        if cv2.waitKey(1) & 0xFF == 32:
            # save the image
            cv2.imwrite('quatro_classes_scan/classe_'+str(i+1)+'/picture_'+str(img_counter+1)+'.bmp', frame)
            print('Foto ' + str(img_counter+1) + ' salva!')
            img_counter += 1
            
        # if the user presses the escape key, then the program is terminated
        elif cv2.waitKey(1) & 0xFF == 27:
            break
    img_counter = 0

# release the camera
cam.release()

# stops the camera window
cv2.destroyAllWindows()