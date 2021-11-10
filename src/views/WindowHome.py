"""
	Bilderk
	@date 08-05-2021
	@author Bilderk
"""

"""Importación de librerías necesarias"""
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk
import os

"""Clase FrameHome"""
class FrameHome(tk.Toplevel):

    """Creación del constructor de la clase"""
    def __init__(self):
        super(FrameHome, self).__init__()
        # Creating mains views
        self.geometry("650x500")
        # self.config(bg="gray25")
        self.title('Bilderk - Home')
        self.resizable(width=True, height=True)
        self.iconbitmap(bitmap="icono.ico")
        # Creating Menu Bar
        self.menubar = tk.Menu(self)
        self.file = tk.Menu(self.menubar, tearoff=0, bg="gray25", fg="white", bd=1)

        self.prueba = tk.Frame(self)
        self.notebookhome = ttk.Notebook(self.prueba)
        self.frame_people = FramePeople(self.notebookhome)
        self.frame_camera = FrameCamera(self.notebookhome)
        self.frame_profile = FrameProfile(self.notebookhome)
        self.frame_register = FrameRegister(self.notebookhome)
        self.frame_log = FrameLog(self.notebookhome)
        self.frame_failed = FrameFailed(self.notebookhome)

        self.notebookhome.add(self.frame_people, text="Usuarios", padding=5)
        self.notebookhome.add(self.frame_register, text="Registrar Usuario", padding=10)
        self.notebookhome.add(self.frame_camera, text="Cámaras", padding=5)
        self.notebookhome.add(self.frame_profile, text="Perfil", padding=5)
        self.notebookhome.add(self.frame_log, text="Auditoría", padding=5)
        self.notebookhome.add(self.frame_failed, text="Ingresos fallidos", padding=5)

        # Putting the views
        self.config(menu=self.menubar)
        self.notebookhome.pack(pady=30, padx=30, fill=tk.BOTH, expand=True)
        self.prueba.config(bg="gray25")
        self.prueba.pack(fill='both', expand=True)

"""Clase FramePeople"""
class FramePeople(tk.Frame):

    """Creación del constructor de la clase"""
    def __init__(self, master=None):
        super(FramePeople, self).__init__(master)
        self.config(bg="gray25")
        self.style_BK = ttk.Style()
        self.style_BK.theme_use("clam")
        self.style_BK.configure("BW.TButton", background="gray25", foreground="white", font=("Helvetica", 10),
                                activebackground="burlywood", highlightcolor="black")
        self.style_BK.configure("TNotebook", background="gray25", foreground="white")
        # Creating mains views
        self.lp = tk.Listbox(self, selectbackground="gray25")
        self.container = tk.Frame(self)
        self.buttonDelete = ttk.Button(self.container, text="Eliminar persona", style="BW.TButton")
        self.buttonEditImg = ttk.Button(self.container, text="Editar imagen", style="BW.TButton")
        self.buttonEditName = ttk.Button(self.container, text="Editar nombre", style="BW.TButton")
        # Putting the views
        self.container.config(bg="gray25")
        self.lp.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.container.pack(padx=10, pady=10, side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.buttonDelete.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X, expand=True)
        self.buttonEditImg.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X, expand=True)
        self.buttonEditName.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X, expand=True)

        self.insertValues()

    """Vaciar la lista para volver a escribir"""
    def voidInBox(self):
        self.lp.delete(0, (self.lp.size() - 1))

    """Inserta los nombres de los usuarios a la lista"""
    def insertValues(self):
        count = 1
        dataPath = 'data/faces'
        peopleList = os.listdir(dataPath)
        for nameDir in peopleList:
            self.lp.insert(count, nameDir)
            count += 1

"""Clase FrameCamera"""
class FrameCamera(tk.Frame):

    """Creación del constructor de la clase"""
    def __init__(self, master=None):
        super(FrameCamera, self).__init__(master)
        self.config(bg="gray25")
        self.style_BK = ttk.Style()
        self.style_BK.theme_use("clam")
        self.style_BK.configure("BW.TButton", background="gray25", foreground="white", font=("Helvetica", 10),
                                activebackground="burlywood", highlightcolor="black")
        self.style_BK.configure("TNotebook", background="gray25", foreground="white")
        # Variables
        self.boolCheck = tk.BooleanVar(self)
        # Creating mains views
        self.container = tk.Frame(self)
        self.buttonEdit = ttk.Button(self.container, text="Editar Cámara", style="BW.TButton")
        self.checkActive = ttk.Checkbutton(self.container, text="Activar Cámara", var=self.boolCheck,
                                           onvalue=True, offvalue=False)
        self.spinboxCamera = tk.Spinbox(self.container, from_=0, to=10)
        # Putting the views
        self.container.config(bg="gray25")
        self.spinboxCamera.pack(padx=10, pady=2, side=tk.TOP, fill=tk.X, expand=True)
        self.checkActive.pack(padx=10, pady=5, side=tk.TOP, fill=tk.X, expand=True)
        self.buttonEdit.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X, expand=True)
        self.container.pack(padx=10, pady=10, side=tk.RIGHT, fill=tk.BOTH, expand=True)

"""Clase FrameRegister"""
class FrameRegister(tk.Frame):

    """Creación del constructor de la clase"""
    def __init__(self, master=None):
        super(FrameRegister, self).__init__(master)
        self.config(bg="gray25")
        self.img_recognition = tk.PhotoImage(file="data/img/face.png")
        self.style_BK = ttk.Style()
        self.style_BK.theme_use("clam")
        self.style_BK.configure("BW.TButton", background="gray25", foreground="white", font=("Helvetica", 10))
        self.style_BK.configure("BW.TLabel", background="gray25", foreground="white", font=("Helvetica", 15))
        self.style_BK.configure("BK.TLabel", background="gray25", foreground="white", font=("Helvetica", 40))
        # Creating mains views
        self.text_login = ttk.Label(self, text="Registrar", style="BK.TLabel")
        self.text_name = ttk.Label(self, text="Nombre:", style="BW.TLabel")
        self.text_list = ttk.Label(self, text="Lista de Personas:", style="BW.TLabel")
        self.entry_name = ttk.Entry(self, width=40)

        self.entry_list = tk.Text(self, width=40, height=10, font=("Helvetica", 15))
        self.botton_long = ttk.Button(self, text="Registrar", style="BW.TButton")
        # Putting the views
        self.text_login.grid(pady=20, padx=5, row=0, column=1, sticky=tk.W + tk.E)
        self.text_name.grid(pady=10, padx=10, row=1, column=0, sticky=tk.W + tk.E)
        self.entry_name.grid(padx=5, pady=5, row=1, column=1, columnspan=5, sticky=tk.W + tk.E)
        self.botton_long.grid(padx=15, pady=10, row=3, column=0, columnspan=6, sticky=tk.W + tk.E)
        self.text_list.grid(pady=10, padx=10, row=4, column=0, sticky=tk.W + tk.E)
        self.entry_list.grid(padx=5, pady=5, row=5, column=0, columnspan=5, rowspan=5, sticky=tk.W + tk.E)

"""Clase FrameLog"""
class FrameLog(tk.Frame):

    """Creación del constructor de la clase"""
    def __init__(self, master=None):
        super(FrameLog, self).__init__(master)
        self.config(bg="gray25")
        self.style_BK = ttk.Style()
        self.style_BK.theme_use("clam")
        self.style_BK.configure("BW.TButton", background="gray25", foreground="white", font=("Helvetica", 10),
                                activebackground="burlywood", highlightcolor="black")
        self.style_BK.configure("TNotebook", background="gray25", foreground='white')
        self.button_update = ttk.Button(self, text="Actualizar información", style="BW.TButton")
        self.button_update.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X, expand=True)
        self.tv = ttk.Treeview(self, columns=('ID', 'Nombre', 'Fecha'), show='headings')
        self.tv.column('ID', minwidth=0, width=30)
        self.tv.column('Nombre', minwidth=0, width=260)
        self.tv.column('Fecha', minwidth=0, width=130)
        self.tv.heading('ID', text='ID')
        self.tv.heading('Nombre', text='Nombre')
        self.tv.heading('Fecha', text='Fecha')
        self.tv.pack(padx=10, pady=10, side=tk.TOP, fill=tk.BOTH, expand=True)

"""Clase FrameProfile"""
class FrameProfile(tk.Frame):

    """Creación del constructor de la clase"""
    def __init__(self, master=None):
        super(FrameProfile, self).__init__(master)
        self.config(bg="gray25")
        self.style_BK = ttk.Style()
        self.style_BK.theme_use("clam")
        self.style_BK.configure("BW.TButton", background="gray25", foreground="white", font=("Helvetica", 10),
                                activebackground="burlywood", highlightcolor="black")
        self.style_BK.configure("TNotebook", background="gray25", foreground="white")
        # Creating mains views
        self.container = tk.Frame(self)
        self.text_edit = ttk.Label(self, text="Editar perfi", style="BK.TLabel")
        self.text_user = ttk.Label(self, text="Nombre de usuario:", style="BW.TLabel")
        self.text_pass = ttk.Label(self, text="Contraseña:", style="BW.TLabel")
        self.text_conf = ttk.Label(self, text="Confirmación:", style="BW.TLabel")

        self.entry_user = ttk.Entry(self, width=40)
        self.entry_pass = ttk.Entry(self, width=40)
        self.entry_conf = ttk.Entry(self, width=40)
        self.buttonAdmin = ttk.Button(self, text="Actualizar información", style="BW.TButton")

        # self.entry_email = tk.Text(self.master,width=40,height=1,font=("Helvetica",15))
        # Putting the views
        self.text_edit.grid(pady=20, padx=5, row=0, column=1, sticky=tk.W + tk.E)
        self.text_user.grid(pady=10, padx=10, row=1, column=0, sticky=tk.W + tk.E)
        self.text_pass.grid(pady=10, padx=10, row=2, column=0, sticky=tk.W + tk.E)
        self.text_conf.grid(pady=10, padx=10, row=3, column=0, sticky=tk.W + tk.E)
        self.entry_user.grid(padx=5, pady=5, row=1, column=1, columnspan=5, sticky=tk.W + tk.E)
        self.entry_pass.grid(padx=5, pady=5, row=2, column=1, columnspan=5, sticky=tk.W + tk.E)
        self.entry_conf.grid(padx=5, pady=5, row=3, column=1, columnspan=5, sticky=tk.W + tk.E)
        self.buttonAdmin.grid(padx=15, pady=10, row=4, column=0, columnspan=6, sticky=tk.W + tk.E)

class FrameFailed(tk.Frame):

    """Creación del constructor de la clase"""
    def __init__(self, master=None):
        super(FrameFailed, self).__init__(master)
        self.config(bg="gray25")
        self.style_BK = ttk.Style()
        self.style_BK.theme_use("clam")
        self.style_BK.configure("BW.TButton", background="gray25", foreground="white", font=("Helvetica", 10),
                                activebackground="burlywood", highlightcolor="black")
        self.style_BK.configure("TNotebook", background="gray25", foreground="white")
        self.button_failed = ttk.Button(self, text="Ver detalle", style="BW.TButton")
        self.button_failed.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X, expand=True)
        # Creating mains views
        self.fl = tk.Listbox(self, selectbackground="gray25")
        self.fl.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

        """
        if len(self.fl.curselection()) > 0:
            self.button_failed['state'] = 'normal'
        else:
            self.button_failed['state'] = 'disabled'
        """

        self.insertFailes()

    def insertFailes(self):
        dat = open("data/logs/RecogLog.txt", "r")
        data_fail = list(dat)
        counter = 1
        for x in reversed(data_fail):
            self.fl.insert(counter, x)
            counter += 1
