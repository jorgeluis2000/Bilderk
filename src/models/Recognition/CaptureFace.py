"""
	Bilderk
	@date 08-05-2021
	@author Bilderk
"""

"""Importación de librerías necesarias"""
import cv2
import imutils
import os
import numpy as np
import pickle
from tkinter import messagebox as mb
import tkinter as tk
from threading import *
import time
from datetime import datetime

"""Clase RcogFaces"""


class RecogFaces(object):
    """Creación del contructor de la clase"""

    def __init__(self, nLabel):
        super(RecogFaces, self).__init__()
        self.camera = cv2.VideoCapture()
        self.window = nLabel
        self.cameraRecord = Camera(key=0, cLabel=nLabel)

    """Selección de la cámara para el reconocimiento"""

    def newCamera(self):
        self.cameraRecord = Camera(key=0, cLabel=self.window)

    """Se actualiza el nombre el usuario seleccionado y se cambia el nombre de la carpeta"""

    def updateF(self, cName):
        personName = cName
        dataPath = 'data/faces'  # Cambia a la ruta donde hayas almacenado Data
        personPath = dataPath + '/' + personName
        if not os.path.exists(personPath):
            os.makedirs(personPath)
        return personPath

    """Se lee el formato xml base para el reconocimiento y se guarda el rostro de la persona"""

    def saveFace(self, cName):
        personPath = self.updateF(cName)
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        faceClassif = cv2.CascadeClassifier('recognice/haarcascade_frontalface_default.xml')

        count = 0
        while True:
            ret, frame = cap.read()
            if ret == False: break
            frame = imutils.resize(frame, width=640)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = frame.copy()
            faces = faceClassif.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                rostro = auxFrame[y:y + h, x:x + w]
                rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(personPath + '/rostro_{}.jpg'.format(count), rostro)
                count = count + 1
            cv2.imshow('frame', frame)

            k = cv2.waitKey(1)
            if k == 27 or count >= 20:
                break
        self.listPeople()
        cap.release()
        cv2.destroyAllWindows()

    """Se actualiza la lista de usuarios y se listan los existentes"""

    def listPeople(self):
        dataPath = 'data/faces'  # Cambia a la ruta donde hayas almacenado Data
        peopleList = os.listdir(dataPath)
        # ('Lista de personas: ', peopleList)

        labels = []
        facesData = []
        label = 0

        for nameDir in peopleList:
            personPath = dataPath + '/' + nameDir
            # print('Leyendo las imágenes')

            for fileName in os.listdir(personPath):
                # print('Rostros: ', nameDir + '/' + fileName)
                labels.append(label)
                image = cv2.imread(personPath + '/' + fileName, 0)
                facesData.append(image)
            label += 1

        # Métodos para entrenar el reconocedor
        face_eigen = cv2.face.EigenFaceRecognizer_create()
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Entrenando el reconocedor de rostros
        if len(facesData) > 0:
            face_recognizer.train(facesData, np.array(labels))
            face_eigen.train(facesData, np.array(labels))

        # Almacenando el modelo obtenido
        face_eigen.write('data/document/modeloEigenFace.xml')
        face_recognizer.write('data/document/modeloLBPHFace.xml')

    """Se carga el modelo creado para realizar el reconocimiento facial"""

    def faceRecog(self):
        dataPath = 'data/faces'  # Cambia a la ruta donde hayas almacenado Data
        imagePaths = os.listdir(dataPath)
        # print('imagePaths=', imagePaths)

        # face_recognizer = cv2.face.EigenFaceRecognizer_create()
        # face_recognizer = cv2.face.FisherFaceRecognizer_create()
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Leyendo el modelo
        # face_recognizer.read('modeloEigenFace.xml')
        # face_recognizer.read('modeloFisherFace.xml')
        face_recognizer.read('data/document/modeloLBPHFace.xml')
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        faceClassif = cv2.CascadeClassifier('recognice/haarcascade_frontalface_default.xml')

        while True:
            ret, frame = cap.read()
            if ret == False: break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()

            faces = faceClassif.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                rostro = auxFrame[y:y + h, x:x + w]
                rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                result = face_recognizer.predict(rostro)

                cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
                # LBPHFace
                if result[1] < 70:
                    cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y - 25), 2, 1.1, (0, 255, 0), 1,
                                cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            cv2.imshow('frame', frame)
            k = cv2.waitKey(1)
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()


"""Clase Camera"""


class Camera(Thread):
    """Creación del contructor de la clase"""

    def __init__(self, key=0, cstatus=True, cLabel=None):
        self.entryKey = key
        self.status = cstatus
        self.__realCamera = None
        self.frame = None
        self.before = -2
        self.rgn = 0
        self.wLabel = cLabel
        Thread.__init__(self)

    """Llamado al método de activación de la cámara"""

    def run(self):
        self.activeCamera()

    """Se realiza el reconocimiento de la persona y valida que esta esté registrada. 
    Si lo está aparece el nombre del usuario y de lo contrario, sale como desconocido"""

    def activeCamera(self):
        dataPath = 'data/faces'  # change at away where there are stored data
        imagePaths = os.listdir(dataPath)
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        # reading the model
        face_recognizer.read('data/document/modeloLBPHFace.xml')
        faceClassif = cv2.CascadeClassifier('recognice/haarcascade_frontalface_default.xml')
        self.changeCamera()
        counter = 1
        while self.status:
            ret, self.frame = self.__realCamera.read()

            if not ret: self.status = False
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()
            faces = faceClassif.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                ros = auxFrame[y:y + h, x:x + w]
                recognition = cv2.resize(ros, (150, 150), interpolation=cv2.INTER_CUBIC)
                result = []
                if len(imagePaths) > 0:
                    result = face_recognizer.predict(recognition)
                cv2.putText(self.frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
                timer = datetime.now()
                format = timer.strftime('%d-%m-%Y %H:%M:%S ')
                if len(result) > 0 and result[1] < 70:
                    # print(imagePaths[result[0]])
                    if counter == 0:
                        mb.showinfo('Identificado', '-- Ingreso autorizado --')
                        counter += 1
                    self.rgn = (result[0])
                    if self.rgn != self.before:
                        self.before = (result[0])
                        counter = 0
                    user = '{}'.format(imagePaths[result[0]])
                    cv2.putText(self.frame, user, (x, y - 25), 2, 1.1, (0, 255, 0), 1,
                                cv2.LINE_AA)
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    # print('Desconocido')
                    self.rgn = -1
                    if self.rgn != self.before:
                        # print('diferente')
                        with open("data/logs/RecogLog.txt", "a") as data:
                            data.write(str(format) + 'Ingreso fallido: Usuario no identificado' + '\n')
                        number = open("data/logs/RecogLog.txt", "r")
                        count = list(number)
                        length = str(len(count))
                        cv2.imwrite('data/unidentified/LoginFailed_' + length + '.png', self.frame)
                        self.before = -1
                    cv2.putText(self.frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imwrite("data/img/camera.png", self.frame)
            self.wLabel.img_recognition = tk.PhotoImage(file="data/img/camera.png")
            self.wLabel.extra_full.config(image=self.wLabel.img_recognition, width=540, height=420)
            time.sleep(0.06)
        self.finishCamera()

    """Se cambia la cámara para usar la que se encuentre disponible"""

    def changeCamera(self):
        self.__realCamera = cv2.VideoCapture(self.entryKey, cv2.CAP_DSHOW)

    """Se termina el proceso de ejecución de la cámara"""

    def finishCamera(self):
        self.status = False
        self.__realCamera.release()
        self.saveSettingsCamera()

    """Se reanuda el proceso de ejecución de la cámara"""

    def reActiveCamera(self):
        self.status = True

    """Se guarda la configuración de una cámara agregada"""

    def saveSettingsCamera(self):
        tupla = [self.entryKey, self.status]
        with open("data/document/dataCamera.pickle", "wb") as f:
            pickle.dump(tupla, f)

    """Se carga el archivo base para modelar la estrucutra y lectura de las cámaras"""

    def loadCamera(self):
        tupla = []
        with open("data/document/dataCamera.pickle", "rb") as f:
            tupla = pickle.load(f)
        self.status = True
        self.entryKey = int(tupla[0])
