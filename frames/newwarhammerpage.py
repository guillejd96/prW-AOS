import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from cfg.Structs import *
from cfg.Configuration import *

class NewWarhammerPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.configure(style='TFrame')  # Establecer el estilo del Frame

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

        self.name_label = ttk.Label(self, text=NAME_FORM_STRING)
        self.name_label.pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)

        self.faction_label = ttk.Label(self, text=FACTION_FORM_STRING)
        self.faction_label.pack(pady=5)
        self.faction_var = tk.StringVar(self)
        self.faction_menu = ttk.OptionMenu(self, self.faction_var, EMPTY_STRING, *[f.value for f in Facciones])
        self.faction_menu.pack(pady=5)
        
        self.type_label = ttk.Label(self, text=TYPE_FORM_STRING)
        self.type_label.pack(pady=5)
        self.type_var = tk.StringVar(self)
        self.type_menu = ttk.OptionMenu(self, self.type_var, EMPTY_STRING, Tipo_WH.MINIATURE.value, Tipo_WH.REGIMENT.value, Tipo_WH.BAND.value)
        self.type_menu.pack(pady=5)

        self.number_label = ttk.Label(self, text=NUMBER_FORM_STRING)
        self.number_label.pack(pady=5)
        self.number_entry = ttk.Entry(self)
        self.number_entry.pack(pady=5)
        
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=5)

        self.clear_button = ttk.Button(self.button_frame, text=CREATE_STRING, command=self.create_entry)
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.create_button = ttk.Button(self.button_frame, text=CLEAN_STRING, command=self.clear_form)
        self.create_button.pack(side=tk.RIGHT, padx=10)

        # Llamar a la función para actualizar el estado del campo de cantidad
        self.update_quantity_entry()
        
        # Usar trace para actualizar el estado del campo de cantidad cuando cambie el tipo
        self.type_var.trace("w", lambda *args: self.update_quantity_entry())

    def update_quantity_entry(self):
        if self.type_var.get() == Tipo_WH.MINIATURE.value:
            self.number_entry.config(state='disabled')
            self.number_entry.delete(0, tk.END)
            self.number_entry.insert(0, "1")
        else:
            self.number_entry.config(state='normal')
            self.number_entry.delete(0, tk.END)

    def create_entry(self):
        name = self.name_entry.get()
        if name == "":
            error_label = ttk.Label(self, text=NO_NAME_ERROR, foreground="red")
            error_label.pack(pady=10)
            self.after(5000, error_label.destroy)
            return
            
        faction = self.faction_var.get()
        if faction == EMPTY_STRING:
            error_label = ttk.Label(self, text=NO_FACTION_ERROR, foreground="red")
            error_label.pack(pady=10)
            self.after(5000, error_label.destroy)
            return
        
        type = self.type_var.get()
        if type == EMPTY_STRING:
            error_label = ttk.Label(self, text=NO_TYPE_ERROR, foreground="red")
            error_label.pack(pady=10)
            self.after(5000, error_label.destroy)
            return
        
        number = self.number_entry.get()
        if type.upper() == Tipo_WH.MINIATURE.value.upper():
            number = "1"
        else:
            if number == "":
                error_label = ttk.Label(self, text=NO_NUMBER_ERROR, foreground="red")
                error_label.pack(pady=10)
                self.after(5000, error_label.destroy)
                print("No number")
                return
            if not number.isdigit():
                error_label = ttk.Label(self, text=INVALID_NUMBER_ERROR, foreground="red")
                error_label.pack(pady=10)
                self.after(5000, error_label.destroy)
                return
        
        # print(f"Nombre: {name}, Facción: {faction}, Número: {number}, Tipo: {type}")
        
        filename = f"saves/{faction}.txt"
        with open(filename, "a") as file:
            file.write(f"{name},{faction},{number},{type}\n")
        
        self.controller.show_frame(FACTION_PAGE_STRING, faction)

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.faction_var.set(EMPTY_STRING)
        self.type_var.set(EMPTY_STRING)
        self.number_entry.delete(0, tk.END)

    def show(self, show, *args, **kwargs):
        if show:
            self.pack(fill="both", expand=True)
            self.clear_form()
            
            if args:
                faction = args[0]
                self.controller.title(WARHAMMER_STRING + " - " + NEW_STRING + " - " + faction)
                self.faction_var.set(faction)
            
        else:
            self.pack_forget()