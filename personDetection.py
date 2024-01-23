# importar librerias

import torch
import cv2
import numpy as np
import pandas

# Para poder manejar directorio en windows
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# model_path = Path('C:/Users/DavidC/Desktop/IA proyects/Human detection/humanDetectionIA/model/best.pt')

# leer modelo
model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path = 'C:/Users/DavidC/Desktop/IA proyects/Human detection/humanDetectionIA/model/best2.pt')

# Realizar videocaptura
# para analizar video tiempo real desde camara =>
cap = cv2.VideoCapture(0) #que camara queremos usar
# cap = cv2.VideoCapture('Test video/output.avi')

# para grabar video => out = cv2.VideoWriter('output.avi', cv2.VideoWriter.fourcc(*'XVID'), 20.0, (640, 480))

#
while True:
    # Realizar lectura video
    ret, frame = cap.read()

    # Correccion de color

    # Realizar deteccion
    detect = model(frame)
    info = detect.pandas().xyxy[0]
    print(info)

    # Mostrar fps y  cuadrito
    cv2.imshow('Detector de humanos' , np.squeeze(detect.render()))

    #Ir guardando video
    # para grabar video => out.write(frame)

    # Condicion de salida

    t = cv2.waitKey(5) # 5ms de retraso
    if t == 27: # 27 es tecla 'ESC'
        break

cap.release()  # Si salimos del loop, borramos captura
# para grabar video => out.release() # cerrar grabacion
cv2.destroyAllWindows() # Si salimos del loop, destruimos todas las ventanas
