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
        faction_image = Image.open(image_path)
        faction_image = faction_image.convert("RGBA")
        datas = faction_image.getdata()

        new_data = []
        for item in datas:
            if item[0] > 250 and item[1] > 250 and item[2] > 250:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        faction_image.putdata(new_data)
        faction_image = faction_image.resize((400, 400), Image.Resampling.LANCZOS)
        faction_photo = ImageTk.PhotoImage(faction_image)

        self.image_label = tk.Label(self.canvas, image=faction_photo)
        self.image_label.image = faction_photo
        self.image_label.pack(side="top", anchor="n", pady=20)

        self.label = tk.Label(self.canvas, text = WARHAMMER_STRING, font=("Arial", 24))
        self.label.pack(pady=10, padx=10)
        
        self.faction2_button = tk.Button(self.canvas, text="New Faction", command=lambda: self.controller.show_frame("NewFactionPage"))
        self.faction2_button.pack(pady=10,padx=10)
        
        self.bottom_canvas = tk.Canvas(parent, width=parent.winfo_screenwidth(), height=200, bg="darkgrey")

        self.bottom_canvas.create_rectangle(0, 0, parent.winfo_screenwidth(), 200, outline="black", width=5)
        self.bottom_canvas.pack(side="bottom", fill="x")

        #self.update_bottom_canvas()
        

    def on_image_click(self, text):
        self.controller.show_frame(FACTION_PAGE_STRING,text)
        """
        if text == Facciones.STORMCAST.value:
            self.controller.show_frame(FACTION_PAGE_STRING, Facciones.STORMCAST.value)
        elif text == Facciones.SYLVANETH.value:
            self.controller.show_frame(FACTION_PAGE_STRING, Facciones.SYLVANETH.value)
        elif text == Facciones.ORRUK.value:
            self.controller.show_frame(FACTION_PAGE_STRING, Facciones.ORRUK.value)
        elif text == Facciones.NIGHTHAUNT.value: 
            self.controller.show_frame(FACTION_PAGE_STRING, Facciones.NIGHTHAUNT.value)
        elif text == Facciones.GOBLINS.value:
            self.controller.show_frame(FACTION_PAGE_STRING, Facciones.GOBLINS.value)
        elif text == Facciones.SCENOGRAPHY.value:
            self.controller.show_frame(FACTION_PAGE_STRING, Facciones.SCENOGRAPHY.value)
        """
        
    def update_bottom_canvas(self):
        print("MainPage - update_bottom_canvas")
        for widget in self.bottom_canvas.winfo_children():
            widget.destroy()
        # Crear un nuevo diccionario con solo los valores True
        if hasattr(self.controller, 'uso_facciones'):
            facciones_usadas = {key: value for key, value in self.controller.uso_facciones.items() if value}
        else:
            print("ERROR ERROR ERROR")
            facciones_usadas = {
                Facciones.STORMCAST.value : True
            }
            self.label = tk.Label(self.bottom_canvas, text = NO_DATA_ERROR, font=("Arial", 24))
            self.label.pack(pady=10, padx=10)

        #labels_text = [Facciones.STORMCAST.value, Facciones.ORRUK.value, Facciones.NIGHTHAUNT.value, Facciones.SYLVANETH.value, Facciones.GOBLINS.value,Facciones.SCENOGRAPHY.value]
        
        i = 0
        for text, value in facciones_usadas.items():
            #print(i,": ",text," - ",value)
            label = tk.Label(self.bottom_canvas, text=text, bg="darkgrey")
            label.place(relx=(i + 0.5) / len(facciones_usadas), rely=0.3, anchor="center")
            
            label.bind("<Button-1>", lambda e, text=text: self.on_image_click(text))

            label.bind("<Enter>", lambda e: e.widget.config(cursor="hand2"))
            label.bind("<Leave>", lambda e: e.widget.config(cursor=""))

            image_path = self.controller.faction_logo_paths[text][1]
            if image_path == "":
                image_path = OTHER_FACTIONS_LOGO_PATH

            faction_image = Image.open(image_path)
            faction_image = faction_image.convert("RGBA")
            datas = faction_image.getdata()

            new_data = []
            for item in datas:
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)

            faction_image.putdata(new_data)
            faction_image = faction_image.resize((100, 100), Image.Resampling.LANCZOS)
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
            self.canvas.pack(side="top", fill="both", expand=True)
            self.image_label.pack(side="top", anchor="n", pady=20)
            self.label.pack(side="top", anchor="n")
            self.bottom_canvas.pack(side="bottom", fill="x")
            self.controller.title(WARHAMMER_STRING + " - " + MAIN_PAGE_STRING)
            self.update_bottom_canvas()
        else:
            self.canvas.pack_forget()
            self.image_label.pack_forget()
            self.label.pack_forget()
            self.bottom_canvas.pack_forget()
        
        
    
            
