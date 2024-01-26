# imports
import time

import cv2
import numpy as np
from tracker2 import *
from person import personDetector
from person import Person

# crear un obj de seguimiento
seguimiento = Rastreador()

#lectura de video
cap = cv2.VideoCapture("Test video/2 corto.mp4.mp4")

# deteccion de ob con camara estable
# Aumentando el historial podemos mejorar resultados en camara estatica
# modificando el umbral aumenta la detecion, pero posibles falsos positivos
deteccion = cv2.createBackgroundSubtractorMOG2(history=10000, varThreshold=100) # Sirve para extrar los objetos en movimiento de una camara estable, devuelve fondo negro y los objetos en movimiento de color blanco y grices

#lista para tiempos

carI = {}
car0 = {}
prueba = {}

personDetector = personDetector()

while True:
    #lectura de video
    ret, frame = cap.read()

    #Obtener ancho y alto fotogramas
    height = frame.shape[0] # 720
    width = frame.shape[1] #1280

    #crear una mascara
    mask = np.zeros((height,width), dtype="uint8")

    #Elegir zona de interes
    #Seleccion de puntos punto Izquierdo / derecho, superior / inferior , x / y
    pISx = 0
    pISy = 280
    pDSx = 600
    pDSy = 125
    pIIx = 230
    pIIy = 600
    pDIx = 1000
    pDIy = 260


    pts = np.array([[[pISx , pISy] , [pDSx , pDSy] ,[pDIx,pDIy] ,[pIIx,pIIy]]])  # COORDENANDAS [x , y] de cada esquina de la zona de interes, desde la esq sup izquierda en sentido horario

    #Escanear poligono con los puntos
    cv2.fillPoly(mask , pts , 255)

    #Eliminar lo que esta fuera de los puntos
    zona = cv2.bitwise_and(frame , frame, mask=mask)

    #Mostrar lineas en la zona de interes
    areaPileta = [(pISx , pISy) , (pDSx , pDSy) , (pDIx,pDIy) , (pIIx,pIIy)]   # COORDENANDAS [x , y] de cada esquina de la zona de interes, desde la esq sup izquierda en sentido horario
    areaAgua =  [(60,290) , (560,160) , (840,240) , (200,450)]
    # area3 = [(427,196) , (pDSx , pDSy) , (pDIx,pDIy) , (619,306)]
    # area2 = [(221,251) , (427,196) , (619,306) , (382,395)]
    # area1 = [(pISx , pISy) , (221,251) , (382,395) , (pIIx,pIIy)]

    #DIbujar
    #area general
    cv2.polylines(frame , [np.array(areaPileta,np.int32)] , True , (255,255,0),5)
    #area agua
    cv2.polylines(frame , [np.array(areaAgua,np.int32)] , True , (0,0,255),3)
    #area 3
    # cv2.polylines(frame , [np.array(area3,np.int32)] , True , (0,130,255),3)
    #area 2
    # cv2.polylines(frame , [np.array(area2,np.int32)] , True , (0,0,255),3)
    #area 1
    # cv2.polylines(frame , [np.array(area1,np.int32)] , True , (0,130,255),3)

    # crear mascara para que los obj sean blancos y el fondo negro
    mascara = deteccion.apply(zona) # la deteccion creada en cv2.createBackgroundSubtractorMOG2(history=10000, varThreshold=100), la aplicamos solo a zona de interes

    # INICIO => Esto es para eliminar ruidos que generan sobras de algunos objetos como arboles
    #aplicamos suavizado
    filtro = cv2.GaussianBlur(mascara , (31 , 31) , 0)
    #Umbral de binarizacion, eliminamos los pixeles grises, y solo quedan blancos y negros, seteamos el limite donde un pixel gris se pasa a blanco o negro
    # _, umbral = cv2.threshold(filtro, 254 ,255, cv2.THRESH_BINARY ) Ejemplo, un objeto lo entrega en 255 blanco puro, pero la sombra puede que le entregue en 253 250, por lo que ponemos blanco puro (255) como el limite
    _, umbral = cv2.threshold(filtro, 50 ,255, cv2.THRESH_BINARY )
    #Dilatar los pixeles, CUANDO HAY OBJETOS "GRANDES", SE USA PARA EVITAR POSIBLES "HUECOS" DENTRO DE LOS OBJETOS, QUE PRODUCAN QUE UN OBJETO SEA ENTENDIDO COMO SI FUERAN DOS O MAS OBJETOS
    dila = cv2.dilate(umbral , np.ones((3,3)))
    #Crear kernel (mascara), ESTO ES PARA CUANDO HAY UNOS PIXELES CERCANOS, SEAN UNIDOS COMO PARTE DE UNA MISMA REGION
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    #aPLICAMOS EL KERNEL PARA JUNTAR LOS PIXELES DISPERSOS
    cerrar = cv2.morphologyEx(dila, cv2.MORPH_CLOSE , kernel)
    # FIN => Esto es para eliminar ruidos que generan sobras de algunos objetos como arboles



    contornos , _ =cv2.findContours(cerrar, cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)  # deteccion de contornos y lo guardamos en lista "contornos"
    detecciones = [] # lista donde vamos a almacenar la info

    #Estas lineas son para obtener los contornos y discernir si el contorno es lo suficientemente grande como para tenerlo en cuenta, ayuda a limpiar el ingreso de info que luego sera rastreada
    #Dibujamos todos los contronos en fram
    for cont in contornos :
        #Eliminamos los contornos pequeños
        area = cv2.contourArea(cont) # Extraemos el valor de superficie dentro de los contornos, y los que sean mayores a un valor los aceptamos o no.. EJ 1800 pixeles



        # TODO ACA DEBERIA METER LA VALIDACION DE PERSONA, ES PERSONA? ES ADULTO? ES NIÑO?
        # TODO ACA DEBERIA METER LA VALIDACION DE PERSONA, ES PERSONA? ES ADULTO? ES NIÑO?
        # TODO ACA DEBERIA METER LA VALIDACION DE PERSONA, ES PERSONA? ES ADULTO? ES NIÑO?

        personDetected = personDetector.detectPerson(frame)

        # TODO ACA DEBERIA METER LA VALIDACION DE PERSONA, ES PERSONA? ES ADULTO? ES NIÑO?
        # TODO ACA DEBERIA METER LA VALIDACION DE PERSONA, ES PERSONA? ES ADULTO? ES NIÑO?
        # TODO ACA DEBERIA METER LA VALIDACION DE PERSONA, ES PERSONA? ES ADULTO? ES NIÑO?


        if personDetected is not None:# TODO ACA DEBERIA METER LA VALIDACION DE PERSONA, ES PERSONA? ES ADULTO? ES NIÑO?
            x,y,ancho,alto = cv2.boundingRect(cont) #Obtenemos alto ancho y posicion x inicial e y inicial, de los objetos suficientemente grandes
            #Almacenamos la informacion de las detecciones en la lista,
            detecciones.append([x ,y , ancho, alto])

    #Seguimiento de los objetos almacenados en la lista de detecciones
    info_id = seguimiento.rastreo(detecciones)

    for inf in info_id:
        #extraer coordenadas
        x,y,ancho,alto,id = inf #x e y son las cordenadas del pixel inicial del objeto

        #Extraer centro del objeto
        cx = int(x + ancho / 2)
        cy = int(y + alto / 2)


        zonaAgua = cv2.pointPolygonTest(np.array(areaAgua, np.int32), (cx, cy), False)
        zonaPileta = cv2.pointPolygonTest(np.array(areaPileta, np.int32), (cx, cy), False)

        # ACA DEBO DEFINIR UNA MANERA PARA SUTRAER UNA AREA DENTRO DE OTRA AREA...


        #DIbujar rectangulo color condicional
        if zonaAgua >= 0:
            cv2.rectangle(frame , (x,y-15), (x+ancho,y+alto), (0, 0,255 ) , 3) #dibujamos el rectangulo
        elif zonaPileta == 1:
            cv2.rectangle(frame , (x-10,y-10), (x+ancho,y+alto), (0, 255 ,0 ) , 2) #dibujamos el rectangulo



        """
        #Areas de influencia
        a2= cv2.pointPolygonTest(np.array(area2 , np.int32) , (cx , cy), False) # NOS DICE SI UN PUNTO ESTA EN UN AREA=>  esta fuera (-1), adentro (1) o cruzando (0),. RECIBE UNA MATRIZ, para eso es numpy

        #Si esta en el area de la mitad
        if a2 >= 0:
            #tomar el tiempo en el que el carro entra y lo almacenamos en el diccionario
            carI[id] = time.process_time()

        if id in carI:
            cv2.circle(frame , (cx , cy) ,3 ,(0,0,255), -1) #mostrar el centro del objeto mientras esta en el area

            #Preguntar si entra al area 3
            a3 = cv2.pointPolygonTest(np.array(area3 , np.int32) , (cx, cy) , False)

            #Si esta en el area
            if a3>= 0:
                #Tomar el tiempo
                tiempo = time.process_time() - carI[id]

                #Corregir error de tiempo
                if tiempo % 1 == 0:
                    tiempo = tiempo + 0.323
                if tiempo % 1 != 0:
                    tiempo = tiempo + 1.016

                if id not in car0:
                    #Almacenar info
                    car0[id] = tiempo
                if id in car0:
                    tiempo = car0[id]

                    vel = 14.3 / car0[id] # 14.3 es la distancia del area, que luego al dividir en tiempo dara la velocidad en Mts/Seg
                    vel = vel * 3.6 # EL valor 3.6 es para convertir Mts/Seg a Km/h

                #Mostrar el numero
                cv2.rectangle(frame , ( x , y-10 ) , ( x+100 , y-50 ) , (0,0,255) , -1 )
                cv2.putText(frame , str(int(vel)) + " km/h", (x,y -35), cv2.FONT_HERSHEY_PLAIN , 1 , (255,255,255) , 2)

        #Mostramos el numero
        cv2.putText(frame, str(id) , (x , y-15) , cv2.FONT_HERSHEY_PLAIN, 1 , (0,0,0) , 2)
        """
    # Secciones
    cv2.imshow('Video completo' , frame)
    # cv2.imshow("Zona de interes" , zona)
    # cv2.imshow("mascara" , mascara)
    # cv2.imshow("filtro" , filtro)
    # cv2.imshow("umbral" , umbral)
    # cv2.imshow("dila" , dila)
    # cv2.moveWindow("dila",200,200)


    key = cv2.waitKey(5)
    if key == 27:
        # cap.release()
        # cv2.destroyAllWindows()
        break

cap.release()
cv2.destroyAllWindows()






