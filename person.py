import torch
import cv2
import numpy as np
import pandas

# Para poder manejar directorio en windows
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# model_path = Path('C:/Users/DavidC/Desktop/IA proyects/Human detection/humanDetectionIA/model/best.pt')


class Person():
    def __init__(self):
        self.type = "adulto"
        self.position = ""
        self.id = ""


class personDetector():
    MINIMAL_CONFIDENCE = 0.25
    # leer modelo
    model = torch.hub.load('ultralytics/yolov5', 'custom',
                                path="C:/Users/DavidC/Desktop/IA proyects/Human detection/humanDetectionIA/model/best2.pt")  # C:/Users/DavidC/Desktop/IA proyects/Human detection/humanDetectionIA/model/best2.pt
    def detectPerson(self, frame):
        detect = self.model(frame)
        info = detect.pandas().xyxy[0]
        # Mostrar fps y  cuadrito
        cv2.imshow('Detector de humanos' , np.squeeze(detect.render()))

        if len(info) > 0 :
            if detect.pandas().xyxy[0]["confidence"][0] > self.MINIMAL_CONFIDENCE:
                ancho = int(info["xmax"][0] - info["xmin"][0])
                alto = int(info["ymax"][0] - info["ymin"][0])
                person = {int(info["xmin"][0]), int(info["ymin"][0]), ancho, alto}
                return person
            else:
                print("BAJA CONFIDENCE ================== >>>>> " + str(detect.pandas().xyxy[0]["confidence"][0]))

        return None

