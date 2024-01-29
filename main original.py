from textwrap import fill
import tkinter as tk
from tkinter import BOTTOM, ttk
import os
from pathlib import Path
from numpy import Infinity
import cv2
from PIL import Image, ImageTk
import pytesseract
import speech_recognition as sr
import vosk

import json




#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

current_directory = os.getcwd() 







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

        self.controller= controller
        # Keep references to tk.PhotoImage objects
        
        canvas = tk.Canvas(self,bg="#47C4B6",height=320,width=480,bd=0,highlightthickness=0,relief="ridge",)

        canvas.place(x = 0, y = 0)
        
        self.button_image_1 = tk.PhotoImage(file="Screens/assets/frame5/button_1.png")
        button_1 = tk.Button(self, image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(yazı),relief="flat")
        button_1.place(x=15.0, y=10.0, width=450.0, height=85.0)


        self.button_image_2 = tk.PhotoImage(file="Screens/assets/frame5/button_2.png")
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(el_tanıma_1),relief="flat")
        button_2.place(x=15.0, y=113.0, width=215.0, height=85.0)



        self.button_image_3 = tk.PhotoImage(file="Screens/assets/frame5/button_3.png")
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(optik),relief="flat")
        button_3.place(x=249.0, y=113.0, width=215.0, height=85.0)

        self.button_image_4 = tk.PhotoImage(file="Screens/assets/frame5/button_4.png")
        button_4 = tk.Button(self,image=self.button_image_4,borderwidth=0,highlightthickness=0,command=self.speech_recognation_screen_controller ,relief="flat")
        button_4.place(x=15.0, y=222.0, width=450.0, height=85.0)
    
        
    def speech_recognation_screen_controller(self):
        self.words = []
        self.controller.show_frame(speech_reco)



        
        







class yazı(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        



        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")
        canvas.place(x = 0, y = 0)
        self.button_image_1 =tk.PhotoImage(file="Screens/assets/frame0/button_1.png")
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,relief="flat") #,command=self.go_ahead
        button_1.place(x=9.0, y=248.0, width=228.6839599609375, height=60.0)

        button_2 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,relief="flat")#,command=self.go_ahead
        button_2.place(x=242.0, y=248.0, width=228.6839599609375, height=60.0)


        label_frame = tk.LabelFrame(self, background="#F0E2E7")
        
        label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80)) 
        self.controller = controller
        

        

        

        self.label_frame = tk.LabelFrame(self, background="#F0E2E7")
        self.label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))
        # self.camera = cv2.VideoCapture(0)
        
        # self.camera.set(4,1080)
        # self.camera.set(3,1920)
        # self.camera_label = tk.Label(self.label_frame)
        # self.camera_label.pack()
        # self.update_camera() 
        
        # Start updating camera stream
    # def go_ahead(self):
    #     self.camera.release()
    #     self.controller.show_frame(el_tanıma_2)
        
        


    # def update_camera(self):
    #     # Function to continuously update the camera stream
    #     ret, frame =self.camera.read()

    #     if ret:
    #         # Display the captured frame on the label
            
    #         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         image = cv2.rotate(image, cv2.ROTATE_180)
    #         image= cv2.resize(image,(500,250))
    #         image = Image.fromarray(image)
            
    #         image = ImageTk.PhotoImage(image=image)
            
    #         self.camera_label.configure(image=image)
    #         self.camera_label.image = image  # type: ignore # Keep a reference to prevent garbage collection

    #     # After 10 milliseconds, call the update_camera function again
    #     self.after(10, self.update_camera)

    




















class optik(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        
        
        
        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")

        canvas.place(x = 0, y = 0)
        self.button_image_1 = tk.PhotoImage(file="Screens/assets/frame1/button_1.png")
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(anasayfa),relief="flat")
        button_1.place(x=152.0, y=246.0, width=160.0, height=70.0)




        self.button_image_2 = tk.PhotoImage(file="Screens/assets/frame1/button_2.png")
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=lambda: print("button_2 clicked"),relief="flat")
        button_2.place(x=9.2552490234375, y=246.0, width=130.0, height=70.0)

        self.button_image_3 = tk.PhotoImage(file="Screens/assets/frame1/button_3.png")
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=lambda: print("button_3 clicked") ,relief="flat")
        button_3.place(x=325.0, y=246.0, width=150.0, height=70.0)


        label_frame = tk.LabelFrame(self, background="#F0E2E7")
        
        label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80)) 


    
class speech_reco(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        

        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        
        self.controller = controller
        self.button_image_1 = tk.PhotoImage(file="Screens/assets/frame4/button_1.png")
        button_1 = tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.transcribe_and_update_label, relief="flat")  # ses kayıt butonu
        button_1.place(x=8.0, y=246.0, width=130.0, height=70.0)

        self.button_image_2 = tk.PhotoImage(file="Screens/assets/frame4/button_2.png")
        button_2 = tk.Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.show_results, relief="flat")  # sonraki soru
        button_2.place(x=147.0, y=246.0, width=142.8824462890625, height=70.0)

        self.button_image_3 = tk.PhotoImage(file="Screens/assets/frame4/button_3.png")
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
        self.transcription_label.config(text= transcription) # type: ignore

    def show_results(self):
        # Bu fonksiyon, "Sonraki Soru" butonuna tıklandığında çalışır.
        current_transcription = self.transcription_label.cget("text")
        self.transcription_label.config(text= "")
        # Append the transcription to the words list only when the "Sonraki Soru" button is clicked
        self.words.append(current_transcription)
        print("Words:", self.words)

    def navigate_and_show_results(self):
    # Bu fonksiyon, "Bitir ve PDF Al" butonuna tıklandığında çalışır.
    # self.words listesini yazdırabilir ve anasayfaya geçebilirsiniz.
        
        # Update the label with the new transcription

        from lib.hand_detection.pdf import write_to_pdf
        metin = ""
        if self.words:
            for kelime in self.words:
                metin = metin + kelime + "\n"
            
            
            output_path = "sesle_yazı.pdf"

            write_to_pdf(output_path, metin)
            print(f"PDF dosyası oluşturuldu: ")
        else:
            print("kelime bulunamadı")

        # Doğru şekilde self.controller kullanın
        self.controller.show_frame(anasayfa)



class el_tanıma_1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        

        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.button_image_1 = tk.PhotoImage(file=   "Screens/assets/frame2/button_1.png")
        button_1 = tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0, relief="flat")#, command=self.take_photo  # şık foto çek
        button_1.place(x=9.2552490234375, y=246.0, width=300.7447509765625, height=70.0)

        self.button_image_2 = tk.PhotoImage(file="Screens/assets/frame2/button_2.png")
        button_2 = tk.Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0, relief="flat")   #, command=self.go_ahead# devam
        button_2.place(x=323.0, y=246.0, width=150.0, height=70.0)

        self.label_frame = tk.LabelFrame(self, background="#F0E2E7")
        self.label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))
        
        
        
        # self.camera = cv2.VideoCapture(0)
        
        # self.camera.set(4,1080)
        # self.camera.set(3,1920)
        # self.camera_label = tk.Label(self.label_frame)
        # self.camera_label.pack()
        # self.update_camera() 
        
        # Start updating camera stream
    # def go_ahead(self):
    #     self.camera.release()
    #     self.controller.show_frame(el_tanıma_2)
    #     from lib.hand_detection import _mapping_offtime
        


    # def update_camera(self):
    #     # Function to continuously update the camera stream
    #     ret, frame =self.camera.read()

    #     if ret:
    #         # Display the captured frame on the label
            
    #         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         image = cv2.rotate(image, cv2.ROTATE_180)
    #         image= cv2.resize(image,(500,250))
    #         image = Image.fromarray(image)
            
    #         image = ImageTk.PhotoImage(image=image)
            
    #         self.camera_label.configure(image=image)
    #         self.camera_label.image = image  # type: ignore # Keep a reference to prevent garbage collection

    #     # After 10 milliseconds, call the update_camera function again
    #     self.after(10, self.update_camera)

    # def capture_image(self):
    # # Capture a single frame from the camera
    #     ret, frame = self.camera.read()

    #     if ret:
    #         # Convert the frame color space from BGR to RGB
    #         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #         # Save the captured frame to a file
    #         image_path = os.path.join(os.getcwd(), "captured_image.jpg")
    #         Image.fromarray(rgb_frame).save(image_path) #grayscale çevirme ve kayıt etme
    #         print("Image captured and saved:", image_path)

    # def take_photo(self):
    #     # Function to capture an image when button_2 is clicked
        
    #     self.capture_image()

    

    # def __del__(self):
    #     # Release the camera when the frame is destroyed
    #     if hasattr(self, 'camera'):
    #         self.camera.release()







class el_tanıma_2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        self.controller = controller
        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")
        
        canvas.place(x = 0, y = 0)
        self.button_image_1 = tk.PhotoImage(file="Screens/assets/frame3/button_1.png")
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(anasayfa),relief="flat")# ses kaydı 
        button_1.place(x=44.0, y=245.0, width=391.035400390625, height=70.0)

        
        
        # label_frame = tk.LabelFrame(self, background="#F0E2E7")
        # label_frame.pack(expand=1, fill="both", side="bottom", pady=(18, 83),padx=(18)) 
        





app = MainApplication()
app.geometry("480x320")
#app.attributes('-fullscreen', True)
app.resizable(False,False)
app.title("SP akademik yardımcı")
app.mainloop()