from textwrap import fill
import tkinter as tk
from tkinter import BOTTOM, ttk
from os import error, getcwd
from pathlib import Path
from numpy import Infinity
import cv2
from PIL import Image, ImageTk



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

        for F in (anasayfa, optik, sesli_1,sesli_2, yazı):
            frame = F(container, self) 
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(anasayfa)
        

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class anasayfa(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        
        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")
        canvas.place(x = 0, y = 0)
    
        def asset_path(png:str):
            return relative_to_assets(png, r"\frame4")

        # Keep references to tk.PhotoImage objects
        
        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")

        canvas.place(x = 0, y = 0)




        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self, image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(yazı),relief="flat")
        button_1.place(x=47.0,y=10.0,width=400.0,height=85.0)

        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png"))
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(optik),relief="flat")
        button_2.place(x=47.0,y=118.0,width=400.0,height=85.0)



        self.button_image_3 = tk.PhotoImage(file=asset_path("button_3.png"))
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(sesli_1),relief="flat")
        button_3.place(x=47.0,y=226.0,width=400.0,height=85.0)











    


class yazı(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        def asset_path(png:str):
            return relative_to_assets(png, r"\frame0")



        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")
        canvas.place(x = 0, y = 0)
        self.button_image_1 =tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(anasayfa),relief="flat")
        button_1.place(x=15.0,y=259.0,width=228.6839599609375,height=53.0)

        canvas.create_rectangle(260.0,259.0,467.0,312.0,fill="#F0E2E7",outline="") #buna ses seviye sistemi eklenecek

        label_frame = tk.LabelFrame(self, background="#F0E2E7")
        
        label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80)) 



















class optik(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def asset_path(png:str):
            return relative_to_assets(png, r"\frame1")
        

        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")

        canvas.place(x = 0, y = 0)
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(anasayfa),relief="flat")
        button_1.place(x=152.0,y=246.0,width=160.0,height=70.0)

        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png"))
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=lambda: print("button_2 clicked"),relief="flat")
        button_2.place(x=9.2552490234375,y=246.0,width=130.0,height=70.0)

        self.button_image_3 = tk.PhotoImage(file=asset_path("button_3.png"))
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=lambda: print("button_3 clicked") ,relief="flat")
        button_3.place(x=325.0,y=246.0,width=150.0,height=70.0)

        label_frame = tk.LabelFrame(self, background="#F0E2E7")
        
        label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80)) 



    
    
    





class sesli_1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        def asset_path(png:str):
            return relative_to_assets(png, r"\frame3")

        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")

        canvas.place(x = 0, y = 0)
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(sesli_2),relief="flat") #ses algılama butonu
        button_1.place(x=313.0,y=247.0,width=165.0,height=70.0)

        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png"))
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=lambda: print("foto çekiliyor"),relief="flat")#foto çekme butonu
        button_2.place(x=7.0,y=247.0,width=135.0,height=70.0)

        self.button_image_3 = tk.PhotoImage(file=asset_path("button_3.png"))
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=lambda: print("button_3 clicked"),relief="flat") #sonraki soru butonu
        button_3.place( x=158.0,y=247.0,width=140.0,height=70.0)

        
        label_frame = tk.LabelFrame(self, background="#F0E2E7")
        
        label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))  # Only add padding at the bottom

        






















class sesli_2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        def asset_path(png:str):
            return relative_to_assets(png, r"\frame2")

        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")

        canvas.place(x = 0, y = 0)
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: print("button_1 clicked"),relief="flat")# ses kaydı 
        button_1.place(x=8.0,y=246.0,width=130.0,height=70.0)

        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png"))
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=lambda: print("button_2 clicked"),relief="flat")# onayla
        button_2.place(x=147.0,y=246.0,width=142.8824462890625,height=70.0)

        self.button_image_3 = tk.PhotoImage(file=asset_path("button_3.png"))
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=lambda:controller.show_frame(anasayfa),relief="flat")# bitir pdf çıktı al bitir pdf çıktı al
        button_3.place( x=299.0,y=246.0,width=170.0,height=70.0)

        
        label_frame = tk.LabelFrame(self, background="#F0E2E7")
        label_frame.pack(expand=1, fill="both", side="bottom", pady=(18, 83),padx=(18)) 
        






app = MainApplication()

app.geometry("480x320")
app.resizable(False,False)
app.title("SP akademik yardımcı")
app.mainloop()