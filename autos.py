# imports
import cv2
import numpy as np
from tracker2 import *

# crear un obj de seguimiento
seguimiento = Rastreador()

#lectura de video
cap = cv2.VideoCapture(0)

# deteccion de ob con camara estable
deteccion = cv2.createBackgroundSubtractorMOG2(history=10000, varThreshold=100)

#lista para tiempos

carI = {}
car0 = {}
prueba = {}

while True:
    #lectura de video
    ret, frame = cap.read()

    #Obtener ancho y alto fotogramas
    height = frame.shape[0]
    width = frame.shape[1]

    #crear una mascara
    mask = np.zeros((height,width), dtype="uint8")

    #Elegir zona de interes
    #Seleccion de puntos
    pts = np.array([[[815,402] , [1032,402] ,[1231,848] ,[506,848]]])  # COORDENANDAS [x , y] de cada esquina de la zona de interes, desde la esq sup izquierda en sentido horario

    #Escanear poligono con los puntos
    cv2.fillPoly(mask , pts , 255)

    #Eliminar lo que esta fuera de los puntos
    zona = cv2.bitwise_and(frame , frame, mask=mask)

    #Mostrar lineas en la zona de interes
    areag = [(815,402) , (1032,402) , (1295,1079) , (357,1079)]   # COORDENANDAS [x , y] de cada esquina de la zona de interes, desde la esq sup izquierda en sentido horario
    area3 = [(815,402) , (1032,402) , (1060,470) , (766,470)]
    area1 = [(667,630) , (1120,630) , (1208,848) , (506,848)]
    area2 = [(766,470) , (1060,470) , (1120,630) , (667,630)]

    #DIbujar
    #area general
    cv2.polylines(frame , [np.array(areag,np.int32)] , True , (255,255,0),2)
    #area 3
    cv2.polylines(frame , [np.array(area3,np.int32)] , True , (0,130,255),1)
    #area 2
    cv2.polylines(frame , [np.array(area2,np.int32)] , True , (0,0,255),1)
    #area 1
    cv2.polylines(frame , [np.array(area1,np.int32)] , True , (0,130,255),1)

    # crea,ps ima ,ascara
    mascara = deteccion.apply(zona)

    #aplicamos suavizado
    filtro = cv2.GaussianBlur(mascara , (11 , 11) , 0)

    #Umbral de binarizacion
    _, umbral = cv2.threshold(filtro, 50 ,255, cv2.THRESH_BINARY )

    #Dilatar los pixeles
    dila = cv2.dilate(umbral , np.ones((3,3)))

    #Crear kernel (mascara)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE(3,3))

    #aPLICAMOS EL KERNEL PARA JUNTAR LOS PIXELES DISPERSOS
    cerrar = cv2.morphologyEx(dila, cv2.MORPH_CLOSE , kernel)

    contornos , _ =cv2.findContours(cerrar, cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
    detecciones = [] # lista donde vamos a almacenar la info

    #Dibujamos todos los contronos en fram

    for cont in contornos :
        #Eliminamos los contornos pequeños
        area = cv2.contourArea(cont)
        if area > 1800:
            x,y,ancho,alto = cv2.boundingRect(cont)

            #Almacenamos la informacion de las detecciones
            detecciones.append([x ,y , ancho, alto])

    #Seguimos de los objetos
    info_id = seguimiento.rastreo(detecciones)

    for inf in info_id:
        #extraer coordenadas
        x,y,ancho,alto,id = inf

        #DIbujar rectangulo
        cv2.rectangle(frame , (x,y-10), (x+ancho,y+alto), (0, 0, 255) , 2) #dibujamos el rectangulo


