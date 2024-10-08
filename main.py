import tkinter as tk
import os
import cv2
from PIL import Image, ImageTk
import speech_recognition as sr
import vosk
import json


#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

current_directory = os.getcwd() 




class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (anasayfa, optik, speech_reco, el_tanıma_1, el_tanıma_2):
            frame = F(self.container, self) 
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

        #frame ***4****        

        def relative_to_assets(file: str):
            file= "Screens/assets/frame4/"+ file
            return file
        
        

        canvas = tk.Canvas(self,bg="#47C4B6",height=320,width=480,bd=0,highlightthickness=0,relief="ridge",)

        canvas.place(x = 0, y = 0)
        
        self.button_image_1 = tk.PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=self.optik_contoller,relief="flat")        
        button_1.place(x=15.0,y=10.0,width=450.0,height=85.0)


        self.button_image_2 = tk.PhotoImage(file=relative_to_assets("button_2.png"))       
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=self.el_tanıma_1_contoller,relief="flat",)
        button_2.place(x=15.0, y=116.0, width=450.0, height=85.0)



        self.button_image_3 = tk.PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = tk.Button(self,image=self.button_image_3,borderwidth=0,highlightthickness=0,command=self.speech_recognation_screen_controller,relief="flat")
        button_3.place(x=15.0,y=222.0,width=285.0,height=85.0)

        self.button_image_4 = tk.PhotoImage(file=relative_to_assets("button_4.png"))
        button_4 = tk.Button(self,image=self.button_image_4,borderwidth=0,highlightthickness=0,command=self.controller.destroy,relief="flat")
        button_4.place(x=310.0,y=222.0,width=155.0,height=85.0)


    def speech_recognation_screen_controller(self):
        self.words = []
        self.controller.show_frame(speech_reco)
    
    def el_tanıma_1_contoller(self):
        el_tanima_frame = el_tanıma_1(self.controller.container, self.controller)
        self.controller.frames[el_tanıma_1] = el_tanima_frame
        el_tanima_frame.grid(row=0, column=0, sticky="nsew")  # Use grid instead of pack
        el_tanima_frame.start_camera()
    
    def optik_contoller(self):
        optik_frame = optik(self.controller.container, self.controller)
        self.controller.frames[optik] = optik_frame
        optik_frame.grid(row=0, column=0, sticky="nsew")  # Use grid instead of pack
        optik_frame.start_camera()



class el_tanıma_1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        

        #frame 1
        def relative_to_assets(file: str):
            file= "Screens/assets/frame1/"+ file
            return file
        
        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        
        self.button_image_1 = tk.PhotoImage(file= relative_to_assets("button_1.png"))
        button_1 = tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.take_photo, relief="flat")
        button_1.place(x=9.2552490234375, y=246.0, width=300.7447509765625, height=70.0)
        
        self.button_image_2 = tk.PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = tk.Button(self, image=self.button_image_2, borderwidth=0, command=self.next_page, highlightthickness=0, relief="flat")  # devam etme butonu
        button_2.place(x=323.0, y=246.0, width=150.0, height=70.0)

        self.label_frame = tk.LabelFrame(self, background="#F0E2E7")
        self.label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))
        
        self.captured_image_label = tk.Label(self.label_frame)
        self.captured_image_label.pack()
        
        self.camera_label = tk.Label(self.label_frame)
        self.camera_label.pack()

        self.cap = None  # Camera is set to None before it's started
    
    
    
    def next_page(self):
        self.stop_camera()
        self.controller.show_frame(el_tanıma_2)
        import lib.hand_detection._mapping_offtime
        import lib.hand_detection._rectangles
        import lib.hand_detection._finger_detect
        
        



    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(4, 1080)
        self.cap.set(3, 1920)
        self.update_camera()

    def update_camera(self):
        if self.cap is not None:
            ret, frame = self.cap.read()   

            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_frame = cv2.resize(rgb_frame, (480, 270))
                img = Image.fromarray(rgb_frame)
                img = ImageTk.PhotoImage(image=img)
                self.camera_label.img = img  # type: ignore
                self.camera_label.config(image=img)

        self.after(10, self.update_camera)

    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        

    def take_photo(self):
        if self.cap is not None:
            ret, frame = self.cap.read() 

            if ret:
                cv2.imwrite("captured_photo.png", frame)
                captured_img = Image.open("captured_photo.png")
                resized_img = captured_img.resize((480, 270))
                resized_img = ImageTk.PhotoImage(resized_img)
                self.captured_image_label.img = resized_img  # type: ignore
                self.captured_image_label.config(image=resized_img)
        #self.stop_camera()
        

    def __del__(self):
        self.stop_camera()










class el_tanıma_2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #frame 2 
        def relative_to_assets(file: str):
            file= "Screens/assets/frame2/"+ file
            return file
        
        
        self.controller = controller
        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")
        
        canvas.place(x = 0, y = 0)
        self.button_image_1 = tk.PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(anasayfa),relief="flat")
        button_1.place(x=44.0, y=245.0, width=391.035400390625, height=70.0)

        


    
    

class speech_reco(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.recognizer = sr.Recognizer()

        self.thread = None  # Add a thread attribute
        self.terminate_thread = False  # Flag to signal thread termination
        
        # frame 3
        def relative_to_assets(file: str):
            file= "Screens/assets/frame3/"+ file
            return file


        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        
        self.controller = controller


        self.button_image_1 = tk.PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.transcribe_and_update_label, relief="flat")  
        button_1.place(x=8.0, y=246.0, width=130.0, height=70.0)



        self.button_image_2 = tk.PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = tk.Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.show_results, relief="flat")  
        button_2.place(x=147.0, y=246.0, width=142.8824462890625, height=70.0)



        self.button_image_3 = tk.PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = tk.Button(self, image=self.button_image_3, borderwidth=0, highlightthickness=0, command=self.navigate_and_show_results, relief="flat")  
        button_3.place(x=299.0, y=246.0, width=170.0, height=70.0)




        self.label_frame = tk.LabelFrame(self, background="#F0E2E7")
        self.label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))

        # Label for displaying transcription
        self.transcription_label = tk.Label(self.label_frame, text="Konuşmanız Burada Görünecek", font=('Helvetica', 12), background="#F0E2E7", wraplength=400)
        self.transcription_label.pack()

        self.words = []  # words listesi sınıfın bir özelliği olacak şekilde taşındı


    def transcribe_audio(self):
        vosk.SetLogLevel(-1)

        # Initialize the microphone
        with sr.Microphone() as source:
            print("bir şey söyleyin...")
            # Capture audio data in a format compatible with Vosk
            audio_data = self.recognizer.listen(source)


        try:
            # Use Vosk to transcribe the speech
            model = vosk.Model("lib/voice_recognation/vosk-model-small-tr-0.3")
            recognizer_vosk = vosk.KaldiRecognizer(model, 16000)

            # Get raw audio data from SpeechRecognition and pass it to Vosk
            audio_data_vosk = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
            recognizer_vosk.AcceptWaveform(audio_data_vosk)

            # Get the transcription result from Vosk
            result_json = json.loads(recognizer_vosk.Result())

            # Extract and return the recognized text
            transcription = result_json.get("text", "")
            print("konuşmanız: ", transcription)
            return transcription

        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""
        



    def transcribe_and_update_label(self):
        import threading
        # Check if a thread is already running and wait for it to complete
        if self.thread and self.thread.is_alive():
            self.terminate_thread = True  # Set the flag to terminate the thread
            self.thread.join()

        # Create a new thread for speech recognition
        self.terminate_thread = False  # Reset the flag
        self.thread = threading.Thread(target=self.process_speech)
        self.thread.start()
        

    def show_results(self):
        current_transcription = self.transcription_label.cget("text")
        self.transcription_label.config(text="")
        self.words.append(current_transcription)
        print("Words:", self.words)

    def navigate_and_show_results(self):
        # Create a new thread for speech recognition
        # # Bu fonksiyon, "Bitir ve PDF Al" butonuna tıklandığında çalışır.
    # self.words listesini yazdırabilir ve anasayfaya geçebilirsiniz.
        
        # Update the label with the new transcription
        if self.thread is not None: 
            self.terminate_thread = True  # Set the flag to terminate the thread
            self.thread.join()# Wait for the thread to complete
            


        from lib.hand_detection.pdf import write_to_pdf
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

    def process_speech(self):
        transcription = self.transcribe_audio()
        if transcription is not None and transcription != "":
        # Update the label with the new transcription
            self.transcription_label.config(text=transcription)
        if self.terminate_thread:
            print("Thread terminated.")
            return
        # Additional processing if needed
        # ...

        # Show results in GUI
        

        # If you need to perform GUI operations, use the after method to schedule them
        # self.after(0, self.show_results)


    
    


class optik(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller= controller
        #Frame 0
        def relative_to_assets(file: str):
            file= "Screens/assets/frame0/"+ file
            return file
        
        
        canvas = tk.Canvas(self,bg = "#47C4B6",height = 320,width = 480,bd = 0,highlightthickness = 0,relief = "ridge")

        canvas.place(x = 0, y = 0)
        self.button_image_1 = tk.PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = tk.Button(self,image=self.button_image_1,borderwidth=0,highlightthickness=0,command=lambda: controller.show_frame(anasayfa),relief="flat")#bitir 
        button_1.place(x=248.0, y=246.0, width=224.0, height=70.0)





        self.button_image_2 = tk.PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = tk.Button(self,image=self.button_image_2,borderwidth=0,highlightthickness=0,command=self.take_photo,relief="flat")#foto çek
        button_2.place(x=11.0, y=246.0, width=224.0, height=70.0)



        self.label_frame = tk.LabelFrame(self, background="#F0E2E7")
        self.label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))
        
        self.captured_image_label = tk.Label(self.label_frame)
        self.captured_image_label.pack()
        
        self.camera_label = tk.Label(self.label_frame)
        self.camera_label.pack()

        self.cap = None  # Camera is set to None before it's started
    
    
    
    def next_page(self):
        self.controller.show_frame(anasayfa)
        import lib.detect_chics.detect_rectangles
        
        
        



    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(4, 1080)
        self.cap.set(3, 1920)
        self.update_camera()

    def update_camera(self):
        if self.cap is not None:
            ret, frame = self.cap.read()   

            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_frame = cv2.resize(rgb_frame, (480, 270))
                img = Image.fromarray(rgb_frame)
                img = ImageTk.PhotoImage(image=img)
                self.camera_label.img = img  # type: ignore
                self.camera_label.config(image=img)

        self.after(10, self.update_camera)

    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        

    def take_photo(self):
        if self.cap is not None:
            ret, frame = self.cap.read() 

            if ret:
                cv2.imwrite("captured_photo_optic.png", frame)
                captured_img = Image.open("captured_photo_optic.png")
                resized_img = captured_img.resize((480, 270))
                resized_img = ImageTk.PhotoImage(resized_img)
                self.captured_image_label.img = resized_img  # type: ignore
                self.captured_image_label.config(image=resized_img)
        self.stop_camera()
        

    def __del__(self):
        self.stop_camera()




app = MainApplication()
app.geometry("480x320")
app.attributes('-fullscreen', True)
app.resizable(False,False)
app.title("SP akademik yardımcı")
app.mainloop()