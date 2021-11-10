"""
	Bilderk
	@date 08-05-2021
	@author Bilderk
"""

"""Importación de librerías necesarias"""
import tkinter as tk
from tkinter import ttk

"""Clase FrameMain"""

class FrameMain(tk.Frame):
    """Creación del contructor de la clase"""

    def __init__(self, master=None):
        super(FrameMain, self).__init__(master)
        self.__master = master
        self.__master.config(bg="gray24")
        self.img_recognition = tk.PhotoImage(file="data/img/face.png")
        self.style_BK = ttk.Style()
        self.style_BK.theme_use("clam")
        self.style_BK.configure("IG.TLabel", width=80, height=50, background="gray25")
        self.style_BK.configure("TNotebook", background="gray25", foreground="white")
        self.style_BK.configure("TNotebook.tap", background="gray25", foreground="white")
        # Creating mains views
        self.extra_full = tk.Label(self.__master, text="", image=self.img_recognition, width=540, height=420)
        self.separator_panel = ttk.Separator(self.__master, orient=tk.VERTICAL)
        self.notebook = ttk.Notebook(self.__master)
        self.frame_login = FrameLogin(self.notebook)
        self.notebook.add(self.frame_login, text="Login", padding=10)
        # Putting the views
        self.separator_panel.grid(padx=30, pady=5, row=0, column=6, rowspan=10, sticky=tk.N + tk.S)
        self.extra_full.grid(padx=10, pady=10, row=0, column=7, rowspan=6)
        self.notebook.grid(padx=10, pady=5, row=0, column=0, rowspan=10, sticky=tk.N + tk.S + tk.W + tk.E)

    """Cierre de la ventana principal"""

    def close_window(self):
        self.__master.destroy()

    """Llamada al master de la clase"""

    def getMaster(self):
        return self.__master

    """Creación del frame de la ventana"""

    def frameCamera(self, nCamera):
        self.__cameraF = nCamera


class FrameLogin(tk.Frame):
    """Creación del contructor de la clase"""

    def __init__(self, master=None):
        super(FrameLogin, self).__init__(master)
        self.config(bg="gray25")
        self.img_recognition = tk.PhotoImage(file="data/img/face.png")
        self.style_BK = ttk.Style()
        self.style_BK.theme_use("clam")
        self.style_BK.configure("BW.TButton", background="gray25", foreground="white", font=("Helvetica", 10),
                                activeforeground="#F50743")
        self.style_BK.configure("BW.TLabel", background="gray25", foreground="white", font=("Helvetica", 15))
        self.style_BK.configure("BK.TLabel", background="gray25", foreground="white", font=("Helvetica", 40))
        # Creating mains views
        self.text_login = ttk.Label(self, text="Inicio de sesión", style="BK.TLabel")
        self.text_email = ttk.Label(self, text="Usuario:", style="BW.TLabel")
        self.text_pass = ttk.Label(self, text="Contraseña:", style="BW.TLabel")
        self.entry_email = ttk.Entry(self, width=40)
        self.entry_pass = ttk.Entry(self, width=40, show="*")
        self.botton_long = ttk.Button(self, text="Ingresar", style="BW.TButton")

        # self.entry_email = tk.Text(self.master,width=40,height=1,font=("Helvetica",15))
        # Putting the views
        self.text_login.grid(pady=20, padx=5, row=0, column=1, sticky=tk.W + tk.E)
        self.text_email.grid(pady=10, padx=10, row=1, column=0, sticky=tk.W + tk.E)
        self.text_pass.grid(pady=10, padx=10, row=2, column=0, sticky=tk.W + tk.E)
        self.entry_email.grid(padx=5, pady=5, row=1, column=1, columnspan=5, sticky=tk.W + tk.E)
        self.entry_pass.grid(padx=5, pady=5, row=2, column=1, columnspan=5, sticky=tk.W + tk.E)
        self.botton_long.grid(padx=15, pady=10, row=4, column=0, columnspan=6, sticky=tk.W + tk.E)
