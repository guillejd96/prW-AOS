import tkinter as tk
from PIL import Image, ImageTk
from cfg.Structs import *
from cfg.Configuration import *
import os
import webbrowser
from PIL.ExifTags import TAGS, GPSTAGS


class PicsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.MAX_HEIGHT_PIC_CANVAS = int(self.winfo_screenwidth() * 0.75)
        self.MAX_WIDTH_PIC_CANVAS = int(self.winfo_screenheight() * 0.75)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.config(width=int(self.winfo_screenwidth() * 0.75), height=int(self.winfo_screenheight() * 0.75))
        self.canvas.pack()

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        prev_icon_path = [os.path.join("icos", file) for file in os.listdir("icos") if file.startswith("previous") and file.endswith(".ico")][0]
        prev_icon = ImageTk.PhotoImage(Image.open(prev_icon_path))
        self.prev_button = tk.Button(self.button_frame, image=prev_icon, command=self.show_prev_image)
        self.prev_button.image = prev_icon  # Keep a reference to avoid garbage collection
        self.prev_button.pack(side="left", padx=10)

        next_icon_path = [os.path.join("icos", file) for file in os.listdir("icos") if file.startswith("play") and file.endswith(".ico")][0]
        next_icon = ImageTk.PhotoImage(Image.open(next_icon_path))
        self.next_button = tk.Button(self.button_frame, image=next_icon, command=self.show_next_image)
        self.next_button.image = next_icon  # Keep a reference to avoid garbage collection
        self.next_button.pack(side="left", padx=10)

    def show_image(self, index):
        if len(self.images) > 0:
            self.canvas.delete("all")
            image = self.images[index]
            
            # Resize image if it exceeds max dimensions
            if image.width() > self.MAX_WIDTH_PIC_CANVAS or image.height() > self.MAX_HEIGHT_PIC_CANVAS:
                image = Image.open(self.image_paths[index])
                image.thumbnail((self.MAX_WIDTH_PIC_CANVAS, self.MAX_HEIGHT_PIC_CANVAS), Image.Resampling.LANCZOS)
                image = ImageTk.PhotoImage(image)
                self.images[index] = image  # Update the image in the list with the resized one

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image_width = image.width()
            image_height = image.height()
            
            x = (canvas_width - image_width) // 2
            y = (canvas_height - image_height) // 2
            
            self.canvas.create_image(x, y, anchor="nw", image=image)
        else:
            self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, text="No images to show", font=("Arial", 24))
            
        # Print image metadata
        image_path = self.image_paths[index]
        try:
            img = Image.open(image_path)
            exif_data = img._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == "DateTime":
                        print(f"Creation Date: {value}")
                    elif tag_name == "GPSInfo":
                        gps_data = {}
                        for t in value:
                            sub_tag = GPSTAGS.get(t, t)
                            gps_data[sub_tag] = value[t]
                        print(f"GPS Data: {gps_data}")
            else:
                print("No EXIF metadata found")
        except Exception as e:
            print(f"Error reading metadata: {e}")

    def show_prev_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.images)
        self.show_image(self.current_image_index)

    def show_next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.show_image(self.current_image_index)

    def show(self, show,*args, **kwargs):
        if show:
            if args:
                self.faction = args[0]
                self.name = args[1]
                dir = "pics/" + args[0] + "/" + args[1]
                if os.path.exists(dir):
                    self.image_folder = dir
                    self.image_paths = [os.path.join(self.image_folder, file) for file in os.listdir(self.image_folder) if file.endswith(('.png','.PNG', '.jpg', '.jpeg', '.gif', '.webp'))]
                    self.images = [ImageTk.PhotoImage(Image.open(path)) for path in self.image_paths]
                    self.current_image_index = 0
                    self.show_image(self.current_image_index)
            self.canvas.pack()
            self.button_frame.pack(pady=10)
            self.controller.title(WARHAMMER_STRING + " - " + self.faction + " - " + self.name)
        else:
            #self.label.pack_forget()
            self.canvas.pack_forget()
            self.button_frame.pack_forget()