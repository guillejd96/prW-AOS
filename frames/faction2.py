import tkinter as tk
from PIL import Image, ImageTk
from cfg.Structs import *
from cfg.Configuration import *
from tkinter import ttk, filedialog
import os
import csv
import webbrowser

class Faction2Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.canvas = tk.Canvas(self, width=800, height=400)

    def show(self, show, *args,**kwargs):
        if show:
            self.canvas.pack(fill="both", expand=True)
            if len(args)>0 and len(args)==1:
                self.faction_str, self.faction_logo, self.faction_save_path = self.get_faction_info(args[0])
                if self.faction_str != NO_DATA_ERROR:
                    self.show_faction()
                else:
                    self.label = tk.Label(self.canvas, text=NO_DATA_ERROR, font=("Arial", 24))
                    self.label.pack(pady=10, padx=10) 
        else:
            self.canvas.pack_forget()
            for children in self.canvas.winfo_children():
                children.pack_forget()
            if hasattr(self, 'image_label'):
                self.image_label.pack_forget()
            if hasattr(self, 'label'):
                self.label.pack_forget()
            if hasattr(self, 'button_frame'):
                self.button_frame.pack_forget()
            if hasattr(self, 'table'):
                self.table.pack_forget()
    
    def show_faction(self):
        image_path = self.faction_logo
        if image_path == '':
            image_path = OTHER_FACTIONS_LOGO_PATH
        faction_image = Image.open(image_path)
        faction_image = self.process_image(image_path,int(faction_image.width * 0.4),int(faction_image.height * 0.4))
        faction_image = faction_image.resize((int(faction_image.width * 0.4), int(faction_image.height * 0.4)), Image.Resampling.LANCZOS)
        faction_photo = ImageTk.PhotoImage(faction_image)

        self.image_label = tk.Label(self.canvas, image=faction_photo)
        self.image_label.image = faction_photo
        self.image_label.pack(side="top", anchor="n", pady=20)

        self.label = tk.Label(self.canvas, text=self.faction_str, font=("Arial", 24))
        self.label.pack(pady=10, padx=10)

        self.button_frame = tk.Frame(self.canvas)
        self.button_frame.pack(pady=10)

        self.new_button = tk.Button(self.button_frame, text=NEW_STRING, command=self.on_new_button_click)
        self.new_button.pack(side="left", padx=5)

        self.clear_button = tk.Button(self.button_frame, text=CLEAR_STRING, command=self.on_clear_button_click)
        self.clear_button.pack(side="left", padx=5)
        
        self.table = tk.Frame(self.canvas)
        self.table.pack(pady=10)
        
        self.canvas.pack()
        self.image_label.pack(side="top", anchor="n", pady=20)
        self.label.pack(side="top", anchor="n")
        self.button_frame.pack(pady=10)
        self.table.pack(side="top", anchor="n", pady=10)
        self.controller.title(WARHAMMER_STRING + " - " + self.faction_str)
        self.updateData()
        
    def updateData(self):
        file_path = self.faction_save_path
        for widget in self.table.winfo_children():
            widget.destroy()
            
        # Inicializar listas para almacenar la información de cada fila
        lstNames = []
        lstFactions = []
        lstQuantities = []
        lstTypes = []

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                nombre, faccion, cantidad, tipo = row
                lstNames.append(nombre)
                lstFactions.append(faccion)
                lstQuantities.append(cantidad)
                lstTypes.append(tipo)
                
        if len(lstNames) == 0:
            return
            
        # Llamar a update_idletasks para que el canvas actualice sus dimensiones
        self.canvas.update_idletasks()
        
        # Crear el bottom_frame con borde y fondo gris
        self.bottom_frame = tk.LabelFrame(self.canvas, bg="grey", borderwidth=5, relief="solid")
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)

        for tipo_wh in list(Tipo_WH):
            col_frame = tk.Frame(self.bottom_frame, bg="white", borderwidth=1, relief="solid")
            col_frame.pack(side="left", fill="both", expand=True)
            
            tipo_label = tk.Label(col_frame, text=tipo_wh.value.upper(), bg="grey", font=("Arial", 12))
            tipo_label.pack(side="top", fill="x")
            
            for i, tipo in enumerate(lstTypes):
                if tipo_wh.value == tipo:
                    row_frame = tk.Frame(col_frame, bg="white", borderwidth=1, relief="solid")
                    row_frame.pack(side="top", fill="x")
                    
                    if tipo_wh.value != Tipo_WH.MINIATURE.value: 
                        name_label = tk.Label(row_frame, text=f"{lstNames[i]} (x{lstQuantities[i]})", bg="white", font=("Arial", 12))
                        name_label.pack(side="left", fill="x")
                    else:
                        name_label = tk.Label(row_frame, text=f"{lstNames[i]}", bg="white", font=("Arial", 12))
                        name_label.pack(side="left", fill="x")
                        
                    action_image = Image.open(ADD_IMAGE_ICON_PATH).convert("RGBA")
                    data = action_image.getdata()
                    new_data = []
                    for item in data:
                        if item[:3] == (0, 0, 0):  # Change black to white
                            new_data.append((255, 255, 255, item[3]))
                        else:
                            new_data.append(item)
                    action_image.putdata(new_data)
                    action_image = action_image.resize((30, 30), Image.Resampling.LANCZOS)
                    action_photo = ImageTk.PhotoImage(action_image)
                    action_button = tk.Button(row_frame, image=action_photo, command=lambda name=lstNames[i]: self.on_add_image_click(name))
                    action_button.image = action_photo
                    action_button["bg"] = self.cget("bg")
                    action_button.pack(side="right", padx=2, pady=2, ipadx=2, ipady=2, expand=True)
                    
                    
                    search_icon = Image.open(WEB_SEARCH_ICON_PATH).convert("RGBA")
                    data = search_icon.getdata()
                    new_data = []
                    for item in data:
                        if item[:3] == (0, 0, 0):  # Change black to white
                            new_data.append((255, 255, 255, item[3]))
                        else:
                            new_data.append(item)
                    search_icon.putdata(new_data)
                    search_icon = search_icon.resize((30, 30), Image.Resampling.LANCZOS)
                    search_icon = ImageTk.PhotoImage(search_icon)
                    self.search_button = tk.Button(row_frame, image=search_icon, command=lambda name=lstNames[i]: self.search_name_online(name))
                    self.search_button.image = search_icon  # Keep a reference to avoid garbage collection
                    self.search_button["bg"] = self.cget("bg")
                    self.search_button.pack(side="right", padx=2, pady=2, ipadx=2, ipady=2, expand=True)
                    
                    sub_dir = os.path.join("pics", self.faction_str)
                    sub_dir = os.path.join(sub_dir, lstNames[i])
                    if os.path.exists(sub_dir):
                        action_image = Image.open(VIEW_IMAGES_ICON_PATH).convert("RGBA")
                        data = action_image.getdata()
                        new_data = []
                        for item in data:
                            if item[:3] == (0, 0, 0):  # Change black to white
                                new_data.append((255, 255, 255, item[3]))
                            else:
                                new_data.append(item)
                        action_image.putdata(new_data)
                        action_image = action_image.resize((30, 30), Image.Resampling.LANCZOS)
                        action_photo = ImageTk.PhotoImage(action_image)
                        action_button = tk.Button(row_frame, image=action_photo, command=lambda name=lstNames[i]: self.on_view_pics_click(self.faction_str,name))
                        action_button.image = action_photo
                        action_button["bg"] = self.cget("bg")
                        action_button.pack(side="right", padx=2, pady=2, ipadx=2, ipady=2, expand=True)

            # Crear bordes separadores excepto después de la última columna
            if tipo_wh != list(Tipo_WH)[-1]:
                border = tk.Label(self.bottom_frame, bg="grey", width=1)  # width in pixels
                border.pack(side="left", fill="y")

        
    def on_add_image_click(self, name):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            dir = os.path.join("pics", self.faction_str)
            if not os.path.exists(dir):
                os.makedirs(dir)

            sub_dir = os.path.join(dir, name)
            if not os.path.exists(sub_dir):
                os.makedirs(sub_dir)
                
            image_name = os.path.basename(file_path)
            destination_path = os.path.join(sub_dir, image_name)
            with open(file_path, "rb") as src_file:
                with open(destination_path, "wb") as dest_file:
                    dest_file.write(src_file.read())
                    
            tk.messagebox.showinfo("Info", "Imagen guardada correctamente")
            self.updateData()
              
            
    def on_view_pics_click(self, dir, name):
        self.controller.show_frame(PICS_PAGE_STRING, dir,name)

    def on_new_button_click(self):
        self.controller.show_frame(NEW_WARHAMMER_PAGE_STRING, self.faction_str)
        
    def on_clear_button_click(self):
        response = tk.messagebox.askyesno(CONFIRM_STRING, CONFIRM_QUESTION_STRING)
        if not response:
            return
        
        file_path = self.faction_save_path
        with open(file_path, "w") as file:
            file.write("")
            
        dir = os.path.join("pics", self.faction_str)
        if os.path.exists(dir):
            for root, dirs, files in os.walk(dir, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            if os.path.exists(dir):
                os.rmdir(dir)
        self.updateData()
        self.controller.updateInfo()
            
    def get_faction_info(self, faction):
        return self.controller.faction_logo_paths[faction]
        
    def search_name_online(self,name):
        if not name.strip():
            return
        query = "Warhammer "
        query = query + name.replace('_', ' ').replace('-', ' ')
        url = f"https://www.google.com/search?tbm=isch&q={query}"
        webbrowser.open(url)
        
    def process_image(self,image_path,width,height):
        image = Image.open(image_path).convert("RGBA")
        
        def is_near_white(pixel):
            r, g, b = pixel[:3]
            return r > 240 and g > 240 and b > 240

        datas = image.getdata()
        new_data = [
            (255, 255, 255, 0) if is_near_white(item) else item
            for item in datas
        ]
        image.putdata(new_data)
        
        original_width, original_height = image.size
    
        aspect_ratio = original_width / original_height

        if width / height != aspect_ratio:
            if width / height > aspect_ratio:
                width = int(height * aspect_ratio)
            else:
                height = int(width / aspect_ratio)    
            
        print(f"{image_path} resized from {original_height}x{original_width} to {height}x{width}")
            
        return image.resize((width, height), Image.Resampling.LANCZOS)