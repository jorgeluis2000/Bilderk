"""
	Bilderk
	@date 08-05-2021
	@author Bilderk
"""

"""Importación de librerías necesarias"""
from src.models.Recognition.CaptureFace import RecogFaces
from src.views.WindowMain import FrameMain
from src.views.WindowHome import FrameHome
from tkinter import Tk
import tkinter as tk
import os
from shutil import rmtree
from shutil import copytree
from tkinter import messagebox as mb
from tkinter import simpledialog as smd
import base64
from datetime import datetime
from PIL import Image

"""Clase Controller"""


class Controller:
    """Creación del contructor de la clase"""

    def __init__(self):
        super(Controller, self).__init__()
        self.window = FrameMain(master=self.start())
        self.recog = RecogFaces(nLabel=self.window)
        self.home = None
        self.clickedMain()
        self.startRecogCamera()
        self.window.master.protocol("WM_DELETE_WINDOW", self.beforeCloseWindow)
        self.window.mainloop()

    """"""

    def startRecogCamera(self):
        self.recog.cameraRecord.loadCamera()
        self.recog.cameraRecord.start()

    """"""

    def clickedMain(self):
        self.window.frame_login.botton_long['command'] = self.getIn

    """"""

    def clickedHome(self):
        self.home.frame_people.buttonEditImg['command'] = self.editImgPerson
        self.home.frame_people.buttonEditName['command'] = self.editPerson
        self.home.frame_people.buttonDelete['command'] = self.deletePeople
        self.home.frame_camera.buttonEdit['command'] = self.editCamera
        self.home.frame_profile.buttonAdmin['command'] = self.editAdmin
        self.home.frame_register.botton_long['command'] = self.submitData
        self.home.frame_log.button_update['command'] = self.updateLog
        self.home.frame_failed.button_failed['command'] = self.listFailed
        self.setListPeople()

    """"""

    def editCamera(self):
        if self.recog.cameraRecord.status:
            self.recog.cameraRecord.finishCamera()
        self.recog.newCamera()
        self.recog.cameraRecord.status = self.home.frame_camera.boolCheck.get()
        self.recog.cameraRecord.entryKey = int(self.home.frame_camera.spinboxCamera.get())
        self.recog.listPeople()
        self.recog.cameraRecord.start()

    """"""

    def deletePeople(self):
        area = self.home.frame_people.lp.curselection()[0]
        user = str(self.home.frame_people.lp.get(area, last=None))
        rmtree("data/faces/" + user)
        self.home.frame_people.lp.delete(tk.ANCHOR)
        self.editCamera()
        self.setListPeople()
        self.writeLog('Usuario eliminado: ' + user)

    def listFailed(self):
        dat = open("data/logs/RecogLog.txt", "r")
        tam = len(list(dat))
        attempt = self.home.frame_failed.fl.curselection()[0]
        selected = attempt + 1
        total = tam - selected + 1
        src = "data/unidentified/LoginFailed_" + str(total) + ".png"
        im = Image.open(src)
        im.show()

    """"""

    def editPerson(self):
        fullname = self.home.frame_people.lp.curselection()[0]
        new_name = smd.askstring(title="Nombre por el que desea cambiar", prompt="Nombre")
        if new_name != None or new_name != "":
            self.createDir(des=new_name, act=str(self.home.frame_people.lp.get(fullname, last=None)))
            self.editCamera()
        else:
            mb.showerror("Campos vacíos", "Por favor, escriba el nombre")
        self.home.frame_people.voidInBox()
        self.home.frame_people.insertValues()
        self.setListPeople()
        self.writeLog('Usuario editado: ' + new_name)

    """"""

    def editImgPerson(self):
        fullname = self.home.frame_people.lp.curselection()[0]
        user = str(self.home.frame_people.lp.get(fullname, last=None))
        rmtree("data/faces/" + user)
        mb.showinfo("Reconocimiento Facial", "Prepárese para el reconocimiento facial")
        if self.recog.cameraRecord.status:
            self.recog.cameraRecord.finishCamera()
        self.recog.newCamera()
        self.recog.saveFace(cName=user)
        self.recog.cameraRecord.status = self.home.frame_camera.boolCheck.get()
        self.recog.cameraRecord.entryKey = int(self.home.frame_camera.spinboxCamera.get())
        self.recog.cameraRecord.start()
        mb.showinfo("Edición Exitosa", "Ha sido editada exitosamente")
        self.setListPeople()
        self.writeLog('Imagen del usuario ' + user + ' editada')

    """"""

    def submitData(self):
        name = str(self.home.frame_register.entry_name.get())
        if (name != ""):
            if self.verifyPeople(cFullName=name) != True:
                if self.recog.cameraRecord.status:
                    self.recog.cameraRecord.finishCamera()
                self.recog.newCamera()
                mb.showinfo("Reconocimiento Facial", "Prepárese para el reconocimiento facial")
                self.recog.saveFace(cName=name)
                mb.showinfo("Registro Exitoso", "Su registro ha sido exitoso")
                self.setListPeople()
                self.home.frame_people.voidInBox()
                self.home.frame_people.insertValues()
                self.recog.cameraRecord.status = self.home.frame_camera.boolCheck.get()
                self.recog.cameraRecord.entryKey = int(self.home.frame_camera.spinboxCamera.get())
                self.recog.cameraRecord.start()
                self.writeLog('Nuevo usuario agregado: ' + name)
            else:
                mb.showinfo("Reconocimiento Facial", "Este usuario ya se encuentra registrado")
        else:
            mb.showerror("Características inválidas", "Complete todos los campos")

    """Verifíca que un nuevo usuario no esté creado en el sistema"""

    def verifyPeople(self, cFullName):
        dataPath = 'data/faces'
        peopleList = os.listdir(dataPath)
        for nameDir in peopleList:
            if nameDir == cFullName:
                return True
        return False

    """Lista la lista de usuarios y cambia su estado a Normal o Deshabilitado"""

    def setListPeople(self):
        dataPath = 'data/faces'
        peopleList = os.listdir(dataPath)
        self.home.frame_register.entry_list['state'] = tk.NORMAL
        self.home.frame_register.entry_list.delete(index1=0.0, index2=tk.END)
        for nameDir in peopleList:
            self.home.frame_register.entry_list.insert(tk.END, " - " + nameDir + "\n")
        self.home.frame_register.entry_list['state'] = tk.DISABLED

    """Inicialización de la ventana principal del software"""

    def start(self):
        root = Tk()
        root.title('Bilderk')
        root.resizable(width=False, height=False)
        root.geometry('1200x460')
        root.iconbitmap(bitmap="icono.ico")
        root.config(bg="gray25")
        self.writeLog('Ingreso al sistema')
        return root

    """Advertencia y cierre de la ventana principal"""

    def beforeCloseWindow(self):
        self.recog.cameraRecord.status = True
        self.recog.cameraRecord.saveSettingsCamera()
        self.recog.cameraRecord.finishCamera()
        mb.showinfo("Cerrar Ventana", "Se encuentra cerrando la ventana")
        self.window.close_window()
        self.writeLog('Cierre del sistema')

    """Inicialización de la ventana Home del software"""

    def startHome(self):
        root = tk.Toplevel()
        root.title('Bilderk - Home')
        root.resizable(width=True, height=True)
        root.iconbitmap(bitmap="icono.ico")
        root.config(bg="gray25")
        return root

    """Edición del admistrador. Se actualiza nombre de usuario y contraseña ingresada"""

    def editAdmin(self):
        admUser = self.home.frame_profile.entry_user.get()
        admPass = self.home.frame_profile.entry_pass.get()
        admConf = self.home.frame_profile.entry_conf.get()
        if admUser != None or admUser != "":
            if admPass != None or admPass != "":
                if admConf != None or admConf != "":
                    if admPass != admConf:
                        mb.showerror("No hay coincidencia", "Ambas contraseñas deben ser iguales.")
                    else:
                        f = open("data/logs/LgAdm.txt", "w")
                        f.write(self.crypting(admUser) + "\n" + self.crypting(admConf))
                        f.close()
                        mb.showinfo("Perfil actualizado", "Los datos han sido actualizados")
                        self.writeLog('Perfil del administrador editado')
                else:
                    mb.showerror("Campo vacío", "Debe ingresar la verificación de la contraseña.")
            else:
                mb.showerror("Campo vacío", "Debe ingresar una contraseña.")
        else:
            mb.showerror("Campo vacío", "Debe ingresar un nombre de usuario.")

    """Encriptación de la contraseña del administrador"""

    def crypting(self, inputText):
        return base64.b64encode(inputText.encode()).decode()

    """Desencriptación de la contraseña del administrador"""

    def decrypting(self, inputText):
        return base64.b64decode(inputText).decode()

    """Se escribe el log con las acciones que el usuario realice en el sistema"""

    def writeLog(self, info):
        time = datetime.now()
        format = time.strftime('%d-%m-%Y %H:%M:%S ')
        with open("data/logs/Log.txt", "a") as txt_file:
            txt_file.write(str(format) + '/ ' + str(info) + '\n')

    """Actualización de log que contiene la navegación de los usuarios en el sistema"""

    def updateLog(self):
        log = open("data/logs/Log.txt", "r")
        lines = list(log)
        it = len(lines)
        tree = self.home.frame_log.tv
        for i in tree.get_children():
            tree.delete(i)
        for x in reversed(lines):
            spl = x.split('/')
            tree.insert(parent='', index='end', iid=it, text='', values=(it - 1, spl[1], spl[0]))
            it = it - 1
        log.close()

    """Autenticación de datos del admin para ingresar al sistema"""

    def getIn(self):
        f = open("data/logs/LgAdm.txt", "r")
        lines = list(f)
        f.close()
        inpMail = self.window.frame_login.entry_email
        inpPass = self.window.frame_login.entry_pass
        us = self.crypting(inpMail.get())
        ps = self.crypting(inpPass.get())
        if us == lines[0][:-1]:
            if ps == lines[1]:
                mb.showinfo(title="Ingresar", message="Ingreso exitoso - BIENVENIDO ADMIN")
                self.home = FrameHome()
                self.clickedHome()
                userAd = self.decrypting(us)
                pswdAd = self.decrypting(ps)
                self.home.frame_profile.entry_user.insert(0, userAd)
                self.home.frame_profile.entry_pass.insert(0, pswdAd)
                self.updateLog()
                self.home.frame_camera.boolCheck.set(self.recog.cameraRecord.status)
                self.home.frame_camera.spinboxCamera.delete(0, tk.END)
                self.home.frame_camera.spinboxCamera.insert(0, self.recog.cameraRecord.entryKey)
                self.writeLog('Nuevo inicio de sesión - ADMIN')
            else:
                mb.showinfo(title="Error de ingreso", message="Contraseña incorrecta, revise los datos")
                self.writeLog('Inicio de sesión fallido')
        else:
            mb.showinfo(title="Error de ingreso", message="El usuario es incorrecto, revise los datos")
            self.writeLog('Inicio de sesión fallido')

    """Se crea un directorio nuevo con el nuevo usuario que se registre"""

    def createDir(self, des, act):
        personName = des
        dataPath = 'data/faces'  # Cambia a la ruta donde hayas almacenado Data
        personPath = dataPath + '/' + personName
        if not os.path.exists(personPath):
            # print(f'Carpeta creada: {personPath}')
            copytree(dataPath + "/" + act, personPath)
            rmtree(dataPath + "/" + act)
            self.writeLog('Nuevo directorio de usuario creado: ' + des)
            return True
        else:
            mb.showwarning("Hay un directorio llamado así", "Por favor, use otro nombre para ese directorio")
        return False


if __name__ == '__main__':
    c = Controller()
