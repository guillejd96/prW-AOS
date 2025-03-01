import tkinter as tk
from PIL import Image, ImageTk
from cfg.Structs import *
from cfg.Configuration import *
from tkinter import ttk, filedialog
import os

class FactionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.canvas = tk.Canvas(self, width=800, height=400)

    def show(self, show, *args,**kwargs):
        if show:
            self.canvas.pack()
            if len(args)>0 and len(args)==1:
                self.faction_str, self.faction_logo, self.faction_save_path = self.get_faction_info(args[0])
                if self.faction_str != NO_DATA_ERROR:
                    self.show_faction()
                else:
                    self.label = tk.Label(self.canvas, text=NO_DATA_ERROR, font=("Arial", 24))
                    self.label.pack(pady=10, padx=10) 
        else:
            self.canvas.pack_forget()
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
        faction_image = Image.open(image_path)
        faction_image = faction_image.resize((int(faction_image.width * 0.75), int(faction_image.height * 0.75)), Image.Resampling.LANCZOS)
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
        self.updateTable()
        self.controller.title(WARHAMMER_STRING + " - " + self.faction_str)
        
        
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
            self.updateTable()  
              
            
    def on_view_pics_click(self, dir, name):
        self.controller.show_frame(PICS_PAGE_STRING, dir,name)

    def on_new_button_click(self):
        self.controller.show_frame(NEW_WARHAMMER_PAGE_STRING)
        
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
        self.updateTable()
        self.controller.updateInfo()
            
    def get_faction_info(self, faction):
        print(faction)
        """
        if faction == STORMCAST_STRING:
            return STORMCAST_STRING, STORMCAST_LOGO_PATH, STORMCAST_SAVE_PATH
        elif faction == ORRUK_STRING:
            return ORRUK_STRING, ORRUK_LOGO_PATH, ORRUK_SAVE_PATH
        elif faction == NIGHTHAUNT_STRING:
            return NIGHTHAUNT_STRING, NIGHTHAUNT_LOGO_PATH, NIGHTHAUNT_SAVE_PATH
        elif faction == SYLVANETH_STRING:
            return SYLVANETH_STRING, SYLVANETH_LOGO_PATH, SYLVANETH_SAVE_PATH
        elif faction == GLOOMSPITE_STRING:
            return GLOOMSPITE_STRING, GLOOMSPITE_LOGO_PATH, GLOOMSPITE_SAVE_PATH
        elif faction == OTHER_FACTIONS_STRING:
            return OTHER_FACTIONS_STRING, OTHER_FACTIONS_LOGO_PATH, OTHER_FACTIONS_SAVE_PATH
        elif faction == SCEN_STRING:
            return SCEN_STRING, SCEN_LOGO_PATH, SCEN_SAVE_PATH
        else:
            return NO_DATA_ERROR, NO_DATA_ERROR, NO_DATA_ERROR
        """
        
    def updateTable(self):
        for widget in self.table.winfo_children():
            widget.destroy()
        file_path = self.faction_save_path
        try:
            with open(file_path, "r") as file:
                content = file.read()
                if content == "":
                    error_label = tk.Label(self.table, text=NO_DATA_ERROR, borderwidth=1, relief="solid", padx=10, pady=10)
                    error_label.pack(side="top", fill="x")
                else:
                    rows = content.split("\n")
                    for row in rows:
                        if row == "":
                            continue
                        values = row.split(",")
                        name = values[0]
                        row_frame = tk.Frame(self.table)
                        row_frame.pack(side="top", fill="x", pady=5)
                        row_text = f"Nombre: {values[0]}\nTipo: {values[3]}\nCantidad: {values[2]}"
                        row_label = tk.Label(row_frame, text=row_text, borderwidth=1, relief="solid", padx=10, pady=5)
                        row_label.pack(side="top", fill="both", expand=True)
                        
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
                        action_button = tk.Button(row_frame, image=action_photo, command=lambda name=name: self.on_add_image_click(name))
                        action_button.image = action_photo
                        action_button["bg"] = self.cget("bg")
                        action_button.pack(side="left", padx=5, pady=5, ipadx=2, ipady=2, expand=True)

                        sub_dir = os.path.join("pics", self.faction_str)
                        sub_dir = os.path.join(sub_dir, name)
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
                            action_button = tk.Button(row_frame, image=action_photo, command=lambda name=name: self.on_view_pics_click(self.faction_str,name))
                            action_button.image = action_photo
                            action_button["bg"] = self.cget("bg")
                            action_button.pack(side="left", padx=5, pady=5, ipadx=2, ipady=2, expand=True)
        except FileNotFoundError:
            error_label = tk.Label(self.table, text=FILE_NOT_FOUND_ERROR, borderwidth=1, relief="solid", padx=10, pady=10)
            error_label.pack(side="top", fill="x")