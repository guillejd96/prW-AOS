import os
import sys
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from frames.mainpage import MainPage
from frames.newwarhammerpage import NewWarhammerPage
from frames.pics import PicsPage
from frames.faction import FactionPage
from frames.faction2 import Faction2Page
from frames.newfactionpage import NewFactionPage
from cfg.Configuration import *
from cfg.Structs import *
from PIL import Image, ImageEnhance
from PIL import Image, ImageDraw

class App(ttkb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title(WARHAMMER_STRING)
        self.state('zoomed')
        #self.iconbitmap(MAIN_ICON_PATH) #FIXME
        self.configure(bg="darkgrey")
        menu = ttkb.Menu(self)
        self.config(menu=menu)
        
        self.top_frame = ttkb.Frame(self)
        self.top_frame.pack(side="top", anchor="nw", padx=1, pady=1,)
        
        style = ttkb.Style()
        style.configure("TButton", background="black", foreground="white")
        
        main_button = ttkb.Button(self.top_frame, text=MAIN_STRING, command=lambda: self.show_frame(MAIN_PAGE_STRING), style="TButton")
        main_button.pack(side="left", padx=1, pady=1)
        
        back_button = ttkb.Button(self.top_frame, text="Quit", command=self.quit, style="TButton")
        back_button.pack(side="left", padx=1, pady=1)

        self.container = ttkb.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.uso_facciones = {faccion.value: False for faccion in Facciones}
        
        # Diccionario para mapear las facciones con sus datos
        self.faction_logo_paths = {
            # Orden
            Facciones.CITIES.value: (Facciones.CITIES.value, "", f"saves/{Facciones.CITIES.value}.txt"),
            Facciones.DAUGHTERS.value: (Facciones.DAUGHTERS.value, "", f"saves/{Facciones.DAUGHTERS.value}.txt"),
            Facciones.FYRESLAYERS.value: (Facciones.FYRESLAYERS.value, "", f"saves/{Facciones.FYRESLAYERS.value}.txt"),
            Facciones.IDONETH.value: (Facciones.IDONETH.value, "", f"saves/{Facciones.IDONETH.value}.txt"),
            Facciones.KHARADRON.value: (Facciones.KHARADRON.value, KHARADRON_LOGO_PATH, f"saves/{Facciones.KHARADRON.value}.txt"),
            Facciones.LUMINETH.value: (Facciones.LUMINETH.value, "", f"saves/{Facciones.LUMINETH.value}.txt"),
            Facciones.SERAPHON.value: (Facciones.SERAPHON.value, "", f"saves/{Facciones.SERAPHON.value}.txt"),
            Facciones.STORMCAST.value: (Facciones.STORMCAST.value, STORMCAST_LOGO_PATH, f"saves/{Facciones.STORMCAST.value}.txt"),
            Facciones.SYLVANETH.value: (Facciones.SYLVANETH.value, SYLVANETH_LOGO_PATH, f"saves/{Facciones.SYLVANETH.value}.txt"),
            
            # Muerte
            Facciones.FLESH.value: (Facciones.FLESH.value, "", f"saves/{Facciones.FLESH.value}.txt"),
            Facciones.NIGHTHAUNT.value: (Facciones.NIGHTHAUNT.value, NIGHTHAUNT_LOGO_PATH, f"saves/{Facciones.NIGHTHAUNT.value}.txt"),
            Facciones.OSSIARCH.value: (Facciones.OSSIARCH.value, "", f"saves/{Facciones.OSSIARCH.value}.txt"),
            Facciones.SOULBLIGHT.value: (Facciones.SOULBLIGHT.value, "", f"saves/{Facciones.SOULBLIGHT.value}.txt"),
            
            # Caos
            Facciones.KHORNE.value: (Facciones.KHORNE.value, "", f"saves/{Facciones.KHORNE.value}.txt"),
            Facciones.TZEENTCH.value: (Facciones.TZEENTCH.value, "", f"saves/{Facciones.TZEENTCH.value}.txt"),
            Facciones.SLAANESH.value: (Facciones.SLAANESH.value, "", f"saves/{Facciones.SLAANESH.value}.txt"),
            Facciones.NURGLE.value: (Facciones.NURGLE.value, "", f"saves/{Facciones.NURGLE.value}.txt"),
            Facciones.SKAVEN.value: (Facciones.SKAVEN.value, "", f"saves/{Facciones.SKAVEN.value}.txt"),
            Facciones.SLAVES.value: (Facciones.SLAVES.value, "", f"saves/{Facciones.SLAVES.value}.txt"),
            Facciones.BEASTS.value: (Facciones.BEASTS.value, "", f"saves/{Facciones.BEASTS.value}.txt"),
            
            # Destrucción
            Facciones.GOBLINS.value: (Facciones.GOBLINS.value, GLOOMSPITE_LOGO_PATH, f"saves/{Facciones.GOBLINS.value}.txt"),
            Facciones.OGOR.value: (Facciones.OGOR.value, "", f"saves/{Facciones.OGOR.value}.txt"),
            Facciones.ORRUK.value: (Facciones.ORRUK.value, ORRUK_LOGO_PATH, f"saves/{Facciones.ORRUK.value}.txt"),
            Facciones.SONS.value: (Facciones.SONS.value, "", f"saves/{Facciones.SONS.value}.txt"),
            
            # Escenografía
            Facciones.SCENOGRAPHY.value: (Facciones.SCENOGRAPHY.value, SCEN_LOGO_PATH, f"saves/{Facciones.SCENOGRAPHY.value}.txt")
        }
        
        self.updateInfo()
        
        self.frames = {}
        
        for F in (
                   MainPage
                  ,NewWarhammerPage
                  ,PicsPage
                  ,FactionPage
                  ,Faction2Page
                  ,NewFactionPage
                  ):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
        
        self.show_frame(MAIN_PAGE_STRING)
        self.last_frame = None
            
    def show_frame(self, page_name,*args, **kwargs):
        for frame in self.frames.values():
            frame.pack_forget()
            frame.show(False)
        frame = self.frames[page_name]
        frame.pack(fill="both", expand=True)
        frame.show(True, *args, **kwargs)
        frame.tkraise()
        self.updateInfo()
    
    def updateInfo(self):
        print("Update Info")
        self.faction_data = {}
        
        if hasattr(self, 'faction_labels'):
            for label in self.faction_labels:
                label.pack_forget()
                label.destroy()
        
        self.faction_labels = []
        
        if hasattr(self, 'top_label'):
            self.top_label.pack_forget()
        
        saves_path = os.path.join(os.path.dirname(__file__), 'saves')
        for i in os.listdir(saves_path):
            if i.endswith('.txt'):
                file_path = os.path.join(saves_path, i)
                if os.path.getsize(file_path) > 0:
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            parts = line.strip().split(',')
                            if len(parts) >= 3:
                                faction = parts[1]
                                if hasattr(self, 'uso_facciones'):
                                    self.uso_facciones[faction] = True
                                try:
                                    value = int(parts[2])
                                    if faction in self.faction_data:
                                        self.faction_data[faction] += value
                                    else:
                                        self.faction_data[faction] = value
                                except ValueError:
                                    pass
            
        if hasattr(self, 'faction_data') and self.faction_data:
            for faction, value in self.faction_data.items():
                faction_label = ttkb.Label(self.top_frame, text=f"{faction}: {value}")
                faction_label.pack(side="left", padx=1, pady=1)
                self.faction_labels.append(faction_label)
        
        """
        if hasattr(self, 'uso_facciones'):
            for key,value in self.uso_facciones.items():
                if value:
                    print(f"{key} -> {value}")
        """
            

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
            
    if not os.path.isdir("saves"):
        print(f"saves/ folder not found in path {os.getcwd()}. Creating it now...")
        os.makedirs("saves")
    if not os.path.isdir("pics"):
        print(f"pics/ folder not found in path {os.getcwd()}. Creating it now...")
        os.makedirs("pics")
    
    app = App()
    app.mainloop()

