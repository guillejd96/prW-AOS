import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from cfg.Configuration import *
from cfg.Structs import *

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.canvas = tk.Canvas(parent, width=parent.winfo_screenwidth(), height=200)
        self.canvas.pack()

        image_path = MAIN_LOGO_PATH
        faction_image = self.process_image(image_path,400,400)
        faction_photo = ImageTk.PhotoImage(faction_image)

        self.image_label = tk.Label(self.canvas, image=faction_photo)
        self.image_label.image = faction_photo
        self.image_label.pack(side="top", anchor="n", pady=20)

        self.label = tk.Label(self.canvas, text = WARHAMMER_STRING, font=("Arial", 24))
        self.label.pack(pady=10, padx=10)
        
        self.faction2_button = tk.Button(self.canvas, text=NEW_FACTION_STRING, command=lambda: self.controller.show_frame("NewFactionPage"))
        self.faction2_button.pack(pady=10,padx=10)
        
        self.bottom_canvas = tk.Canvas(parent, width=parent.winfo_screenwidth(), height=300, bg="darkgrey")
        #self.bottom_canvas.bind("<Configure>", self.on_resize)

        self.rectangle = None
        """parent.winfo_screenheight() * 0.75"""
        self.bottom_canvas.create_rectangle(0, 0, parent.winfo_screenwidth(), 300, outline="black", width=5)
        self.bottom_canvas.pack(side="bottom", fill="x",pady=10)

    def on_image_click(self, text):
        self.controller.show_frame(FACTION_PAGE_STRING,text)
        
    def on_resize(self, event):
        print("MainPage on resize")
        print("\tEvent ",event.widget)
        print("\tEvent details:", event)
        print("\tEvent attributes:", dir(event)) 
        self.bottom_canvas.delete("all")

        width = event.width
        height = event.height
        if height < 300:
            height = 300
        print(f"\t{width}x{height}")
        self.rectangle = self.bottom_canvas.create_rectangle(
            0, 0, width, height * 0.75, outline="black", width=5
        )
        
    def update_bottom_canvas(self):
        print("MainPage - update_bottom_canvas")
        
        """
        self.bottom_canvas.delete("all")

        width = event.width
        height = event.height
        if height < 300:
            height = 300
        print(f"\t{width}x{height}")
        self.rectangle = self.bottom_canvas.create_rectangle(
            0, 0, width, height * 0.75, outline="black", width=5
        )
        """
        
        for widget in self.bottom_canvas.winfo_children():
            widget.destroy()
        # Crear un nuevo diccionario con solo los valores True
        if hasattr(self.controller, 'uso_facciones'):
            facciones_usadas = {key: value for key, value in self.controller.uso_facciones.items() if value}
            #"""
            if len(facciones_usadas)==0:
                self.nodata_label = tk.Label(self.bottom_canvas, text = NO_DATA_ERROR, font=("Arial", 24))
                self.nodata_label.pack(pady=100, padx=10)
            #    """
        else:
            facciones_usadas = {
                Facciones.STORMCAST.value : True
            }
            self.nodata_label = tk.Label(self.bottom_canvas, text = NO_DATA_ERROR, font=("Arial", 24))
            self.nodata_label.pack(pady=10, padx=10)

        i = 0
        for text, value in facciones_usadas.items():
            #print(i,": ",text," - ",value)
            label = tk.Label(self.bottom_canvas, text=text, bg="darkgrey",pady=10)
            label.place(relx=(i + 0.5) / len(facciones_usadas), rely=0.3, anchor="center")
            
            label.bind("<Button-1>", lambda e, text=text: self.on_image_click(text))

            label.bind("<Enter>", lambda e: e.widget.config(cursor="hand2"))
            label.bind("<Leave>", lambda e: e.widget.config(cursor=""))

            image_path = self.controller.faction_logo_paths[text][1]
            if image_path == "":
                image_path = OTHER_FACTIONS_LOGO_PATH
                
            faction_image = self.process_image(image_path,200,200)
            faction_photo = ImageTk.PhotoImage(faction_image)

            faction_label = tk.Label(self.bottom_canvas, image=faction_photo, bg="darkgrey")
            faction_label.image = faction_photo
            faction_label.place(relx=(i + 0.5) / len(facciones_usadas), rely=0.7, anchor="center")

            faction_label.bind("<Button-1>", lambda e, text=text: self.on_image_click(text))

            faction_label.bind("<Enter>", lambda e: e.widget.config(cursor="hand2"))
            faction_label.bind("<Leave>", lambda e: e.widget.config(cursor=""))
            
            i += 1
            
    def show(self, bool):
        if bool:
            if hasattr(self, 'canvas'):
                self.canvas.pack(side="top", fill="both", expand=True)
            if hasattr(self, 'image_label'):
                self.image_label.pack(side="top", anchor="n", pady=20)
            if hasattr(self, 'label'):
                self.label.pack(side="top", anchor="n")
            if hasattr(self, 'bottom_canvas'):
                self.bottom_canvas.pack(side="bottom", fill="x")
            
                
            self.controller.title(WARHAMMER_STRING + " - " + MAIN_PAGE_STRING)
            self.update_bottom_canvas()
        else:
            if hasattr(self, 'canvas'):
                self.canvas.pack_forget()
            if hasattr(self, 'image_label'):
                self.image_label.pack_forget()
            if hasattr(self, 'label'):
                self.label.pack_forget()
            if hasattr(self, 'bottom_canvas'):
                self.bottom_canvas.pack_forget()
            if hasattr(self, 'nodata_label'):
                self.nodata_label.destroy()
            
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
        
        
    
            
