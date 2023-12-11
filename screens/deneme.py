import tkinter as tk
from tkinter import ttk
from os import error, getcwd
from pathlib import Path
from numpy import Infinity
import cv2
from PIL import Image, ImageTk


LARGEFONT = ("Verdana", 20)


current_directory = getcwd()

def relative_to_assets(path: str,frame_number: str )-> Path:
    return Path(current_directory + r"\screens\assets" + frame_number) / Path(path)





class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, optik, sesli, yazı):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        
        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")
        canvas.place(x = 0, y = 0)
    
        def asset_path(png:str):
            return relative_to_assets(png, r"\frame3")

        # Keep references to PhotoImage objects
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self,image=self.button_image_1, borderwidth=0, highlightthickness=0, command=lambda: controller.show_frame(yazı) ,relief="flat")
        button_1.place(x=47.0,y=10.0,width=400.0,height=85.0)


        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png"))
        button_2 = tk.Button(self,image=self.button_image_2, borderwidth=0, command=lambda: controller.show_frame(optik),highlightthickness=0, relief="flat")
        button_2.place(x=47.0,y=118.0,width=400.0,height=85.0)


        self.button_image_3 = tk.PhotoImage(file=asset_path("button_3.png"))
        button_3 = tk.Button(self,image=self.button_image_3,command=lambda: controller.show_frame(sesli), borderwidth=0, highlightthickness=0, relief="flat")
        button_3.place(x=47.0,y=226.0,width=400.0,height=85.0)












    


class yazı(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        def asset_path(png:str):
            return relative_to_assets(png, r"\frame0")
        
        
        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")

        canvas.place(x = 0, y = 0)
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png")) # type: ignore # buradaki location yapısı güncellenmesi lazım
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(StartPage),relief="flat")
        button_1.place(x=65.0,y=230.0,width=350.0,height=80.0)

        canvas.create_rectangle(15.0,21.0,465.0,221.0,fill="#F0E2E7",outline="")


class optik(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def asset_path(png:str):
            return relative_to_assets(png, r"\frame2")
        
        canvas = tk.Canvas(self, bg="#47C4B6", height=150, width=425, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png")) 
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(StartPage) ,relief="flat")
        button_1.place(x=69.0,y=240.0,width=349.0,height=60.0)
        
        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png")) 
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=self.take_photo,relief="flat")
        button_2.place(x=36.0,y=160.0,width=200.0,height=60.0)
        
        self.button_image_3 = tk.PhotoImage(file=asset_path("button_3.png")) 
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=lambda: print("button_3 clicked"),relief="flat")
        button_3.place(x=249.0,y=160.0,width=200.0,height=60.0)

        # Canlı kamera görüntüsünü güncellemek için canvas
        self.video_source = 0  # 0: bilgisayarın ana kamerası
        self.vid = cv2.VideoCapture(self.video_source)
        self.canvas = canvas
        self.update()

        # ... (diğer kodlar)

    def take_photo(self):
    # Görüntüyü al
        ret, frame = self.vid.read()

    # OpenCV görüntüyü PIL formatına dönüştür
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)

    # Tkinter PhotoImage oluştur
        photo_tk = ImageTk.PhotoImage(image=img)
    
        # Fotoğrafı göstermek için yeni bir pencere oluştur
        photo_window = tk.Toplevel(self)
        photo_window.title("Çekilen Fotoğraf")
    
        # Tkinter Canvas üzerine görüntüyü yerleştir
        photo_canvas = tk.Canvas(photo_window, width=img.width, height=img.height)
        photo_canvas.pack()
        photo_canvas.create_image(0, 0, image=photo_tk, anchor=tk.NW)
    
        # Bu satır eklendi
        self.photo_tk = photo_tk
    
        # İstenirse fotoğrafı diske kaydedebilirsiniz
        img.save("captured_photo.png")
        
    def update(self):
        # Canlı kamera görüntüsünü güncelle
        ret, frame = self.vid.read()
        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.after(10, self.update)

    def __del__(self):
        # Uygulama kapatıldığında kamera serbest bırak
        if self.vid.isOpened():
            self.vid.release()
        

        """canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")
        canvas.place(x = 0, y = 0)
        
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png")) 
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(StartPage) ,relief="flat")
        button_1.place(x=69.0,y=240.0,width=349.0,height=60.0)
        
        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png")) 
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,ommand=self.take_photo,relief="flat")
        button_2.place(x=36.0,y=160.0,width=200.0,height=60.0)
        
        self.button_image_3 = tk.PhotoImage(file=asset_path("button_3.png")) 
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=lambda: print("button_3 clicked"),relief="flat")
        button_3.place(x=249.0,y=160.0,width=200.0,height=60.0)
        
        canvas.create_rectangle(31.0,19.0,456.0,149.0,fill="#F0E2E7",outline="")
    def take_photo(self):
        # Görüntüyü al
        ret, frame = cv2.VideoCapture(0).read()

        # OpenCV görüntüyü PIL formatına dönüştür
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)

        # Fotoğrafı göstermek için yeni bir pencere oluştur
        photo_window = tk.Toplevel(self)
        photo_window.title("Çekilen Fotoğraf")

        # Tkinter Canvas üzerine görüntüyü yerleştir
        photo_canvas = tk.Canvas(photo_window, width=img.width, height=img.height)
        photo_canvas.pack()
        photo_tk = ImageTk.PhotoImage(image=img)
        photo_canvas.create_image(0, 0, image=photo_tk, anchor=tk.NW)

        # İstenirse fotoğrafı diske kaydedebilirsiniz
        img.save("captured_photo.png")"""





class sesli(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        def asset_path(png:str):
            return relative_to_assets(png, r"\frame1")
        
        
        
        
        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")

        canvas.place(x = 0, y = 0)
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: print("button_1 clicked"),relief="flat")
        button_1.place(x=32.0,y=148.0,width=193.0,height=60.0)

        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png"))
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=lambda: print("button_2 clicked"),relief="flat")
        button_2.place(x=247.0,y=148.0,width=193.0,height=60.0)

        self.button_image_3 = tk.PhotoImage(file=asset_path("button_3.png"))
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(StartPage),relief="flat")
        button_3.place(x=64.0,y=241.0,width=349.0,height=60.0)

        canvas.create_rectangle(14.0,19.0,464.0,139.0,fill="#F0E2E7",outline="")

app = MainApplication()

app.geometry("480x320")
app.resizable(False,False)
app.title("Your Application Title")
app.mainloop()





