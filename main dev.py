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
import pickle  #
import cvzone
import numpy as np  
from cvzone.HandTrackingModule import HandDetector
import time
import sys
sys.path.append("..")



pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

current_directory = os.getcwd()

def relative_to_assets(path: str,frame_number: str )-> Path:
    return Path(current_directory + r"\screens\assets" + frame_number) / Path(path)





class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = ttk.Notebook(self)
        container.pack(side="top", fill="both", expand=True)

        frames = (anasayfa, optik, speech_reco, yazı, el_tanıma_1, el_tanıma_2)

        for F in frames:
            frame = F(container, self)
            container.add(frame, text=F.__name__)

        # Bind the event when the user switches between tabs
        container.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.frames = {F.__name__: F for F in frames}
        self.show_frame("anasayfa")

    def on_tab_change(self, event):
        # Get the current tab name
        current_tab_name = event.widget.tab(event.widget.select(), "text")

        # If the current tab is el_tanıma_2, start updating the display
        if current_tab_name == "el_tanıma_2":
            self.frames["el_tanıma_2"].start_display_update()
        else:
            # Stop updating the display for other frames
            self.frames["el_tanıma_2"].stop_display_update()

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
        self.transcription_label.config(text= transcription)  # type: ignore

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
        self.controller = controller
        def asset_path(png: str):
            return relative_to_assets(png, r"\frame2")

        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.take_photo, relief="flat")  # şık foto çek
        button_1.place(x=9.2552490234375, y=246.0, width=300.7447509765625, height=70.0)

        self.button_image_2 = tk.PhotoImage(file=asset_path("button_2.png"))
        button_2 = tk.Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.go_ahead, relief="flat")  # devam
        button_2.place(x=323.0, y=246.0, width=150.0, height=70.0)

        self.label_frame = tk.LabelFrame(self, background="#F0E2E7")
        self.label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))
        self.camera = cv2.VideoCapture(0)
        self.camera.set(4,1080)
        self.camera.set(3,1920)
        self.camera_label = tk.Label(self.label_frame)
        self.camera_label.pack()
        self.update_camera() 
        
        # Start updating camera stream
    def go_ahead(self):
        self.camera.release()
        self.controller.show_frame(el_tanıma_2)
        


    def update_camera(self):
        # Function to continuously update the camera stream
        ret, frame =self.camera.read()

        if ret:
            # Display the captured frame on the label
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image= cv2.resize(image,(500,250))
            image = Image.fromarray(image)
            
            image = ImageTk.PhotoImage(image=image)
            
            self.camera_label.configure(image=image)
            self.camera_label.image = image  # type: ignore # Keep a reference to prevent garbage collection

        # After 10 milliseconds, call the update_camera function again
        self.after(10, self.update_camera)

    def capture_image(self):
    # Capture a single frame from the camera
        ret, frame = self.camera.read()

        if ret:
            # Convert the frame color space from BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Save the captured frame to a file
            image_path = os.path.join(os.getcwd(), "captured_image.jpg")
            Image.fromarray(rgb_frame).save(image_path) #grayscale çevirme ve kayıt etme
            print("Image captured and saved:", image_path)

    def take_photo(self):
        # Function to capture an image when button_2 is clicked
        
        self.capture_image()

    

    def __del__(self):
        # Release the camera when the frame is destroyed
        if hasattr(self, 'camera'):
            self.camera.release()







class el_tanıma_2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.display_update_running = False
        
        
        
        def asset_path(png: str):
            return relative_to_assets(png, r"\frame3")

        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        self.button_image_1 = tk.PhotoImage(file=asset_path("button_1.png"))
        button_1 = tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0,command=lambda: controller.show_frame(anasayfa), relief="flat")
        button_1.place(x=44.0, y=245.0, width=391.035400390625, height=70.0)
        # Create a label to display the image
        
        
        
        self.label_frame = tk.LabelFrame(self, background="#F0E2E7")
        self.label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))
        self.camera_label = tk.Label(self.label_frame)
        self.camera_label.pack()

        # Initialize variables
        cam_id = 0
        width, height = 1080, 1920
        map_file_path = "lib/hand_detection/map.p"
        countries_file_path = "lib/hand_detection/rectangles.p"
        self.polygons = []
        self.country_entry_times = {}
        self.selected_countries = []

        file_obj = open(map_file_path, 'rb')
        self.map_points = pickle.load(file_obj)
        file_obj.close()
        print(f"Loaded map coordinates.")

        file_obj = open(countries_file_path, 'rb')
        self.polygons = pickle.load(file_obj)
        file_obj.close()
        print(f"Loaded {len(self.polygons)} rectangles.")

        # Open a connection to the webcam
        self.cap = cv2.VideoCapture(cam_id)
        self.cap.set(4, width)
        self.cap.set(3, height)

        self.update_display()

    def start_display_update(self):
        # Start updating the display only if it's not already running
        if not self.display_update_running:
            self.display_update_running = True
            self.update_display()

    def stop_display_update(self):
        # Stop updating the display
        self.display_update_running = False

    @staticmethod
    def warp_image(img, points, size=[1920, 1080]):
        """
        Warp the input image based on the provided points to create a top-down view.

        Parameters:
        - img: Input image.
        - points: List of four points representing the region to be warped.
        - size: Size of the output image.

        Returns:
        - imgOutput: Warped image.
        - matrix: Transformation matrix.
        """
        # Convert points to NumPy array
    
        # Get the points
        width, height = 1080,1920

    
        # Explicitly convert the points to type numpy.float32
        points = points.astype(np.float32)

        # Compute the perspective transform matrix
        matrix = cv2.getPerspectiveTransform(points, np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32))

        # Apply the perspective transform
        imgOutput = cv2.warpPerspective(img, matrix, (height,width))
    

        # Rotate the result to the right
        #result = cv2.rotate(result, cv2.ROTATE_90_CLOCKWISE)
        #mirrored_result = cv2.flip(result, 1)

        # Display the result


        return imgOutput, matrix
    
    
    
    @staticmethod
    def warp_single_point(point, matrix):
        """
        Warp a single point using the provided perspective transformation matrix.
    
        Parameters:
        - point: Coordinates of the point to be warped.
        - matrix: Perspective transformation matrix.
    
        Returns:
        - point_warped: Warped coordinates of the point.
        """
        # Convert the point to homogeneous coordinates

        point_homogeneous = np.array([[point[0], point[1], 1]], dtype=np.float32)

        # Apply the perspective transformation to the point
        point_homogeneous_transformed = np.dot(matrix, point_homogeneous.T).T

        # Convert back to non-homogeneous coordinates
        point_warped = point_homogeneous_transformed[0, :2] / point_homogeneous_transformed[0, 2]

        return point_warped
    
    @staticmethod
    def get_finger_location(img, imgWarped, matrix):
        """
        Get the location of the index finger tip in the warped image.

        Parameters:
        - img: Original image.

        Returns:
        - warped_point: Coordinates of the index finger tip in the warped image.
        """
        # Find hands in the current frame
        detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

        hands, img = detector.findHands(img, draw=False, flipType=True)
        # Check if any hands are detected
        if hands:
            # Information for the first hand detected
            hand1 = hands[0]  # Get the first hand detected
            indexFinger = hand1["lmList"][8][0:2]  # List of 21 landmarks for the first hand
            # cv2.circle(img,indexFinger,5,(255,0,255),cv2.FILLED)
            warped_point = el_tanıma_2.warp_single_point(indexFinger, matrix)
            warped_point = int(warped_point[0]), int(warped_point[1])
            cv2.circle(imgWarped, warped_point, 5, (255, 0, 0), cv2.FILLED)
        else:
            warped_point = None

        return warped_point

 
    @staticmethod
    def create_overlay_image(polygons, warped_point, imgOverlay, country_entry_times, selected_countries):
        """
        Create an overlay image with marked polygons based on the warped finger location.

        Parameters:
        - polygons: List of polygons representing countries.
        - warped_point: Coordinates of the index finger tip in the warped image.
        - imgOverlay: Overlay image to be marked.
        - country_entry_times: Dictionary to store entry times for countries.
        - selected_countries: List to store selected countries.

        Returns:
        - imgOverlay: Overlay image with marked polygons.
        - country_selected: Name of the selected country.
        """

        country_selected = None
        green_duration_threshold = 3

        for polygon, name in polygons:
            polygon_np = np.array(polygon, np.int32).reshape((-1, 1, 2))
            result = cv2.pointPolygonTest(polygon_np, warped_point, False)

            if result >= 0:
                if name not in country_entry_times:
                    country_entry_times[name] = time.time()

                time_in_country = time.time() - country_entry_times[name]

                if time_in_country >= green_duration_threshold:
                    color = (255, 0, 0)  # blue color
                    country_selected = name

                    if name not in selected_countries:
                        selected_countries.append(name)
                else:
                    color = (255, 0, 255)  # pink color
                    angle = int((time_in_country / green_duration_threshold) * 360)
                    cv2.ellipse(imgOverlay, (warped_point[0], warped_point[1] - 100), (50, 50), 0, 0, angle, color, thickness=-1)

                cv2.polylines(imgOverlay, [np.array(polygon)], isClosed=True, color=color, thickness=2)
                cv2.fillPoly(imgOverlay, [np.array(polygon)], color)
                cvzone.putTextRect(imgOverlay, name, tuple(polygon[0][0]), scale=1, thickness=1)

        return imgOverlay, country_selected
    
    def update_display(self):
        # Read a frame from the webcam
        if self.cap.isOpened():
            success, img = self.cap.read()
            if not success:
                return

            imgWarped, matrix = el_tanıma_2.warp_image(img, self.map_points)

            warped_point = el_tanıma_2.get_finger_location(img, imgWarped, matrix)

            h, w, _ = imgWarped.shape
            imgOverlay = np.zeros((h, w, 3), dtype=np.uint8)
            imgOverlay = cv2.flip(imgOverlay, 1)

            for polygon, name in self.polygons:
                cv2.polylines(imgOverlay, [np.array(polygon)], isClosed=True, color=(0, 255, 0), thickness=2)
                cv2.fillPoly(imgOverlay, [np.array(polygon)], (0, 255, 0))

            selected_country = None

            imgOverlay, selected_country = el_tanıma_2.create_overlay_image(
                self.polygons, warped_point, imgOverlay, self.country_entry_times, self.selected_countries
            )

            imgOutput = cv2.addWeighted(imgWarped, 1, imgOverlay, 0.7, 0)
            imgOutput = cv2.flip(imgOutput, 1)
            imgOutput = cv2.resize(imgOutput, (500, 250))


            
            
            
            
            
            

            # Convert the OpenCV image to a format that Tkinter can handle
            img = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            self.camera_label.configure(image=img)
            self.camera_label.image = img # type: ignore
        
        if self.display_update_running:
            self.after(100, self.update_display)



            

    





app = MainApplication()

app.geometry("480x320")
app.resizable(False,False)
app.title("SP akademik yardımcı")
app.mainloop()