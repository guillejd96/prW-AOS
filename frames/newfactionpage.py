import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
from cfg.Configuration import *
from cfg.Structs import *


class NewFactionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        #self.canvas = tk.Canvas(parent, width=parent.winfo_screenwidth(), height=parent.winfo_screenheight())
        #self.canvas.pack()
        
        # Cargar la imagen con transparencia
        self.image = Image.open(WARHAMMER_LOGO_PATH).convert("RGBA")
        datas = self.image.getdata()

        new_data = []
        for item in datas:
            # Change all white (also shades of whites)
            # pixels to transparent
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        self.image.putdata(new_data)
        self.photo = ImageTk.PhotoImage(self.image)

        # Crear un Label para la imagen y empaquetarlo en el centro superior
        self.image_label = ttk.Label(self, image=self.photo)
        self.image_label.pack(pady=10)
        
        self.faction_label = ttk.Label(self, text=FACTION_FORM_STRING)
        self.faction_label.pack(pady=5)
        self.faction_var = tk.StringVar(self)
        self.faction_menu = ttk.OptionMenu(self, self.faction_var, EMPTY_STRING, *[f.value for f in Facciones])
        self.faction_menu.pack(pady=5)
        
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=5)

        self.clear_button = ttk.Button(self.button_frame, text=CREATE_STRING, command=self.create_entry)
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.create_button = ttk.Button(self.button_frame, text=CLEAN_STRING, command=self.clear_form)
        self.create_button.pack(side=tk.RIGHT, padx=10)
        
    def create_entry(self):
        faction = self.faction_var.get()
        if faction == EMPTY_STRING:
            error_label = ttk.Label(self, text=NO_FACTION_ERROR, foreground="red")
            error_label.pack(pady=10)
            self.after(2500, error_label.destroy)
            return
        
        self.controller.uso_facciones[faction] = True
        
        filename = f"saves/{faction}.txt"
        if not os.path.exists(filename):
            with open(filename, "a") as file:
                file.write("")  # Crear el archivo vacío si no existe
        else:
            # Comprobar si el archivo no está vacío
            with open(filename, "r") as file:
                content = file.read()
                if content:  # Si el contenido no está vacío
                    print(f"El archivo {filename} ya tiene contenido.")
                else:  # Si el archivo está vacío
                    with open(filename, "w") as file:
                        file.write("")  # Escribir en el archivo
                
        self.controller.show_frame("MainPage")
        
    def clear_form(self):
        self.faction_var.set(EMPTY_STRING)

        
    def show(self, bool):
        print("")
        self.clear_form()