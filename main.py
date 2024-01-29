from textwrap import fill
import tkinter as tk
from tkinter import BOTTOM, ttk
import os
from pathlib import Path
from numpy import Infinity
import cv2
from PIL import Image, ImageTk
import threading
import pytesseract
import speech_recognition as sr
import vosk
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

current_directory = os.getcwd()

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

        for F in (anasayfa, optik, speech_reco, yazı, el_tanıma_1,el_tanıma_2):
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

        
    
    
        def asset_path(png:str):
            return relative_to_assets(png, r"\frame5")

        # Keep references to tk.PhotoImage objects
        
        canvas = tk.Canvas(self,bg="#47C4B6",height=320,width=480,bd=0,highlightthickness=0,relief="ridge",)

        canvas.place(x = 0, y = 0)
        
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self, image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(yazı),relief="flat")
        button_1.place(x=15.0, y=10.0, width=450.0, height=85.0)


        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png"))
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(el_tanıma_1),relief="flat")
        button_2.place(x=15.0, y=113.0, width=215.0, height=85.0)



        self.button_image_3 = tk.PhotoImage(file=asset_path("button_3.png"))
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(optik),relief="flat")
        button_3.place(x=249.0, y=113.0, width=215.0, height=85.0)

        self.button_image_4 = tk.PhotoImage(file=asset_path("button_4.png"))
        button_4 = tk.Button(self,image=self.button_image_4,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(speech_reco),relief="flat")
        button_4.place(x=15.0, y=222.0, width=450.0, height=85.0)










    


class yazı(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        def asset_path(png:str):
            return relative_to_assets(png, r"\frame0")



        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")
        canvas.place(x = 0, y = 0)
        self.button_image_1 =tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(anasayfa),relief="flat")
        button_1.place(x=9.0, y=248.0, width=228.6839599609375, height=60.0)


        canvas.create_rectangle(242.0, 248.0, 470.6839599609375, 308.0, fill="#FFFFFF", outline="") #buna ses seviye sistemi eklenecek

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
        button_1.place(x=152.0, y=246.0, width=160.0, height=70.0)




        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png"))
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=lambda: print("button_2 clicked"),relief="flat")
        button_2.place(x=9.2552490234375, y=246.0, width=130.0, height=70.0)

        self.button_image_3 = tk.PhotoImage(file=asset_path("button_3.png"))
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=lambda: print("button_3 clicked") ,relief="flat")
        button_3.place(x=325.0, y=246.0, width=150.0, height=70.0)


        label_frame = tk.LabelFrame(self, background="#F0E2E7")
        
        label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80)) 


    
class speech_reco(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        def asset_path(png:str):
            return relative_to_assets(png, r"\frame4")

        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        
        self.controller = controller
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.transcribe_and_update_label, relief="flat")  # ses kayıt butonu
        button_1.place(x=8.0, y=246.0, width=130.0, height=70.0)

        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png"))
        button_2 = tk.Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.show_results, relief="flat")  # sonraki soru
        button_2.place(x=147.0, y=246.0, width=142.8824462890625, height=70.0)

        self.button_image_3 = tk.PhotoImage(file=asset_path("button_3.png"))
        button_3 = tk.Button(self, image=self.button_image_3, borderwidth=0, highlightthickness=0, command= self.navigate_and_show_results, relief="flat")  # bitir ve pdf al butonu
        button_3.place(x=299.0, y=246.0, width=170.0, height=70.0)

        self.label_frame = tk.LabelFrame(self, background="#F0E2E7")
        self.label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))

        # Label for displaying transcription
        self.transcription_label = tk.Label(self.label_frame, text="Transcription will appear here", font=('Helvetica', 12), background="#F0E2E7", wraplength=400)
        self.transcription_label.pack()

        self.words = []  # words listesi sınıfın bir özelliği olacak şekilde taşındı

    def transcribe_audio(self):
        # Initialize the recognizer
        vosk.SetLogLevel(-1)
        recognizer = sr.Recognizer()

        # Initialize the microphone
        with sr.Microphone() as source:
            print("Say something...")
            # Capture audio data in a format compatible with Vosk
            audio_data = recognizer.listen(source)

        try:
            # Use Vosk to transcribe the speech
            model = vosk.Model("voice_recognation/vosk-model-small-tr-0.3")
            recognizer_vosk = vosk.KaldiRecognizer(model, 16000)

            # Get raw audio data from SpeechRecognition and pass it to Vosk
            audio_data_vosk = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
            recognizer_vosk.AcceptWaveform(audio_data_vosk)

            # Get the transcription result from Vosk
            result_json = json.loads(recognizer_vosk.Result())

            # Extract and return the recognized text
            transcription = result_json.get("text", "")
            print("Transcription:", transcription)
            return transcription

        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

    def transcribe_and_update_label(self):
        # Bu fonksiyon, "Ses Kayıt" butonuna tıklandığında çalışır.
        transcription = self.transcribe_audio()

        # Update the label with the new transcription
        self.transcription_label.config(text="Transcription: " + transcription)

    def show_results(self):
        # Bu fonksiyon, "Sonraki Soru" butonuna tıklandığında çalışır.
        current_transcription = self.transcription_label.cget("text")
        
        # Append the transcription to the words list only when the "Sonraki Soru" button is clicked
        self.words.append(current_transcription)
        print("Words:", self.words)

    def navigate_and_show_results(self):
    # Bu fonksiyon, "Bitir ve PDF Al" butonuna tıklandığında çalışır.
    # self.words listesini yazdırabilir ve anasayfaya geçebilirsiniz.

        from pdf import write_to_pdf
        metin = ""
        if self.words:
            for kelime in self.words:
                metin = metin + kelime + "\n"
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')  # usb path eklenecek
            filename = "sesle_yazı.pdf"
            output_path = os.path.join(desktop_path, filename)

            write_to_pdf(output_path, metin)
            print(f"PDF dosyası oluşturuldu: ")
        else:
            print("kelime bulunamadı")

        # Doğru şekilde self.controller kullanın
        self.controller.show_frame(anasayfa)



class el_tanıma_1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def asset_path(png:str):
            return relative_to_assets(png, r"\frame2")

        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.capture_photo, relief="flat")  # şık foto çek
        button_1.place(x=9.2552490234375, y=246.0, width=300.7447509765625, height=70.0)

        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png"))
        button_2 = tk.Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.stop_camera, relief="flat")  # devam
        button_2.place(x=323.0, y=246.0, width=150.0, height=70.0)

        label_frame = tk.LabelFrame(self, background="#F0E2E7")
        label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))

        # Kameradan görüntü almak için bir canvas oluşturun
        self.canvas = tk.Canvas(label_frame, bg="black", width=400, height=300)
        self.canvas.pack()

        # Kamera görüntüsünü güncellemek için bir iş parçacığı başlatın
        self.capture_video = True  # Bu bayrağı kontrol ederek video yakalama durumunu kontrol eder
        self.video_thread = threading.Thread(target=self.update_camera)
        self.video_thread.daemon = True  # Arayüz kapatıldığında iş parçacığını sonlandırın
        self.video_thread.start()

    def update_camera(self):
        cap = cv2.VideoCapture(0)  # 0, yerleşik kamerayı temsil eder
        width=350
        height=300
        cap.set(3, width)
        cap.set(4, height)
        while self.capture_video:
            ret, frame = cap.read()
            
            if ret:
                # OpenCV görüntüyü RGB formatına dönüştürür
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Tkinter PhotoImage nesnesine dönüştür
                img = ImageTk.PhotoImage(Image.fromarray(rgb_frame))
                # Canvas'a görüntüyü yerleştirin
                self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.canvas.image = img  # referansı tutmak için

    def stop_camera(self):
        # Kamera görüntüsü alma işlemine son ver
        self.capture_video = False # referansı tutmak için
    
    def capture_photo(self):
        # Kamera görüntüsünü al
        return None
    





class el_tanıma_2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        def asset_path(png:str):
            return relative_to_assets(png, r"\frame3")

        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")

        canvas.place(x = 0, y = 0)
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(anasayfa),relief="flat")# ses kaydı 
        button_1.place(x=44.0, y=245.0, width=391.035400390625, height=70.0)

        
        
        label_frame = tk.LabelFrame(self, background="#F0E2E7")
        label_frame.pack(expand=1, fill="both", side="bottom", pady=(18, 83),padx=(18)) 
        


        




app = MainApplication()

app.geometry("480x320")
app.resizable(False,False)
app.title("SP akademik yardımcı")
app.mainloop()