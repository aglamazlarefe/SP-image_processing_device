"""SP akademik yardımcı: 480x320 dokunmatik ekranlı cihaz için Tkinter uygulaması.

Ekranlar: anasayfa, optik (yarım), el_tanıma_1 (kâğıt fotoğrafı) -> el ile seçim,
el_tanıma_2 (bitti ekranı), speech_reco (sesle yazma -> PDF).
Proje kökünden çalıştırılmalı: `python main.py` (tüm yollar köke göredir).
"""

import json
import queue
import threading
import tkinter as tk
from tkinter import messagebox

import cv2
import speech_recognition as sr
import vosk
from PIL import Image, ImageTk

# Windows'ta Tesseract PATH'te değilse:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

VOSK_MODEL_YOLU = "lib/voice_recognation/vosk-model-small-tr-0.3"
CEKILEN_FOTO = "captured_photo.png"
OPTIK_FOTO = "captured_photo_optic.png"
KAMERA_ARALIGI_MS = 30
DIKTE_YER_TUTUCU = "Konuşmanız Burada Görünecek"


def varlik(cerceve, dosya):
    return f"Screens/assets/{cerceve}/{dosya}"


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (anasayfa, optik, speech_reco, el_tanıma_1, el_tanıma_2):
            self._ekle(F)
        self.show_frame(anasayfa)

    def _ekle(self, F):
        frame = F(self.container, self)
        self.frames[F] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        return frame

    def show_frame(self, cont):
        self.frames[cont].tkraise()

    def yeni_ekran(self, F):
        """Kamera ekranlarını her girişte sıfırdan kurar; eskisinin kamerasını kapatıp yok eder."""
        eski = self.frames.get(F)
        if eski is not None:
            if hasattr(eski, "stop_camera"):
                eski.stop_camera()
            eski.destroy()
        frame = self._ekle(F)
        frame.tkraise()
        return frame


class anasayfa(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.button_image_1 = tk.PhotoImage(file=varlik("frame4", "button_1.png"))
        tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0,
                  command=self.optik_contoller, relief="flat").place(x=15.0, y=10.0, width=450.0, height=85.0)

        self.button_image_2 = tk.PhotoImage(file=varlik("frame4", "button_2.png"))
        tk.Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0,
                  command=self.el_tanıma_1_contoller, relief="flat").place(x=15.0, y=116.0, width=450.0, height=85.0)

        self.button_image_3 = tk.PhotoImage(file=varlik("frame4", "button_3.png"))
        tk.Button(self, image=self.button_image_3, borderwidth=0, highlightthickness=0,
                  command=self.speech_recognation_screen_controller, relief="flat").place(
            x=15.0, y=222.0, width=285.0, height=85.0)

        self.button_image_4 = tk.PhotoImage(file=varlik("frame4", "button_4.png"))
        tk.Button(self, image=self.button_image_4, borderwidth=0, highlightthickness=0,
                  command=self.controller.destroy, relief="flat").place(x=310.0, y=222.0, width=155.0, height=85.0)

    def speech_recognation_screen_controller(self):
        self.controller.frames[speech_reco].yeni_dikte()
        self.controller.show_frame(speech_reco)

    def el_tanıma_1_contoller(self):
        self.controller.yeni_ekran(el_tanıma_1).start_camera()

    def optik_contoller(self):
        self.controller.yeni_ekran(optik).start_camera()


class KameraEkrani(tk.Frame):
    """Canlı kamera önizlemesi ve fotoğraf çekme (el_tanıma_1 ve optik ortak kullanır)."""

    def kamera_alanini_kur(self):
        self.label_frame = tk.LabelFrame(self, background="#F0E2E7")
        self.label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))
        self.captured_image_label = tk.Label(self.label_frame)
        self.captured_image_label.pack()
        self.camera_label = tk.Label(self.label_frame)
        self.camera_label.pack()
        self.cap = None
        self._after_id = None

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.cap = None
            messagebox.showerror("Kamera", "Kamera açılamadı.")
            return
        self.cap.set(4, 1080)
        self.cap.set(3, 1920)
        self.update_camera()

    def update_camera(self):
        if self.cap is None:
            return
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (480, 270))
            img = ImageTk.PhotoImage(image=Image.fromarray(rgb_frame))
            self.camera_label.img = img  # referans tutulmazsa görüntü silinir
            self.camera_label.config(image=img)
        self._after_id = self.after(KAMERA_ARALIGI_MS, self.update_camera)

    def stop_camera(self):
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def fotograf_cek(self, dosya_yolu):
        """Kareyi kaydeder ve küçük önizlemesini gösterir. Başarılıysa True."""
        if self.cap is None:
            return False
        ret, frame = self.cap.read()
        if not ret:
            return False
        cv2.imwrite(dosya_yolu, frame)
        onizleme = ImageTk.PhotoImage(Image.open(dosya_yolu).resize((480, 270)))
        self.captured_image_label.img = onizleme
        self.captured_image_label.config(image=onizleme)
        return True


class el_tanıma_1(KameraEkrani):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.foto_cekildi = False

        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.button_image_1 = tk.PhotoImage(file=varlik("frame1", "button_1.png"))
        tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0,
                  command=self.take_photo, relief="flat").place(x=9.2552490234375, y=246.0,
                                                                 width=300.7447509765625, height=70.0)

        self.button_image_2 = tk.PhotoImage(file=varlik("frame1", "button_2.png"))
        tk.Button(self, image=self.button_image_2, borderwidth=0, command=self.next_page,  # devam
                  highlightthickness=0, relief="flat").place(x=323.0, y=246.0, width=150.0, height=70.0)

        self.kamera_alanini_kur()

    def take_photo(self):
        if self.fotograf_cek(CEKILEN_FOTO):
            self.foto_cekildi = True

    def next_page(self):
        """Kâğıdı işler ve parmakla seçim ekranını açar.

        Seçim ekranı OpenCV penceresidir ve kapanana kadar Tk'yi bekletir (bilerek: tam ekran
        tek etkileşim o pencerededir). Modüller her basışta yeniden çağrılabilir.
        """
        if not self.foto_cekildi:
            messagebox.showinfo("El tanıma", "Önce kâğıdın fotoğrafını çekin.")
            return
        self.stop_camera()
        self.controller.show_frame(el_tanıma_2)
        self.update_idletasks()

        try:
            from lib.hand_detection._finger_detect import parmakla_sec
            from lib.hand_detection._mapping_offtime import sayfa_haritasini_cikar
            from lib.hand_detection._rectangles import kutulari_bul
            from lib.hand_detection.qr import qr_oku

            if not sayfa_haritasini_cikar(CEKILEN_FOTO):
                messagebox.showwarning("El tanıma", "Fotoğrafta kâğıt bulunamadı. Tekrar çekin.")
                self.controller.show_frame(anasayfa)
                return
            if kutulari_bul() == 0:
                messagebox.showwarning("El tanıma", "Kâğıtta kutu bulunamadı. Tekrar çekin.")
                self.controller.show_frame(anasayfa)
                return
            parmakla_sec(qr_content=qr_oku(CEKILEN_FOTO))
        except Exception as e:  # cihazda konsol görünmeyebilir; hatayı ekranda göster
            messagebox.showerror("El tanıma", f"Hata: {e}")
            self.controller.show_frame(anasayfa)


class el_tanıma_2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        self.button_image_1 = tk.PhotoImage(file=varlik("frame2", "button_1.png"))
        tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0,
                  command=lambda: controller.show_frame(anasayfa), relief="flat").place(
            x=44.0, y=245.0, width=391.035400390625, height=70.0)


_vosk_model = None
_vosk_kilidi = threading.Lock()


def vosk_modeli():
    """57 MB'lık modeli bir kez yükler (eskiden her cümlede yeniden yükleniyordu)."""
    global _vosk_model
    with _vosk_kilidi:
        if _vosk_model is None:
            vosk.SetLogLevel(-1)
            _vosk_model = vosk.Model(VOSK_MODEL_YOLU)
        return _vosk_model


class speech_reco(tk.Frame):
    """Sesle yazma: "konuş" bir cümle dinler, "ekle" listeye ekler, "bitir" PDF yazar."""

    DINLEME_ZAMAN_ASIMI_SN = 8
    EN_UZUN_CUMLE_SN = 15

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recognizer = sr.Recognizer()
        self.thread = None
        self.sonuclar = queue.Queue()  # iş parçacığı -> arayüz (Tk iş parçacığı güvenli değil)
        self.words = []

        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.button_image_1 = tk.PhotoImage(file=varlik("frame3", "button_1.png"))
        tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0,
                  command=self.transcribe_and_update_label, relief="flat").place(x=8.0, y=246.0, width=130.0, height=70.0)

        self.button_image_2 = tk.PhotoImage(file=varlik("frame3", "button_2.png"))
        tk.Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0,
                  command=self.show_results, relief="flat").place(x=147.0, y=246.0, width=142.8824462890625, height=70.0)

        self.button_image_3 = tk.PhotoImage(file=varlik("frame3", "button_3.png"))
        tk.Button(self, image=self.button_image_3, borderwidth=0, highlightthickness=0,
                  command=self.navigate_and_show_results, relief="flat").place(x=299.0, y=246.0, width=170.0, height=70.0)

        self.label_frame = tk.LabelFrame(self, background="#F0E2E7")
        self.label_frame.pack(expand=1, fill="both", side="bottom", pady=(0, 80))
        self.transcription_label = tk.Label(self.label_frame, text=DIKTE_YER_TUTUCU, font=("Helvetica", 12),
                                            background="#F0E2E7", wraplength=400)
        self.transcription_label.pack()
        self._son_metin = ""

    def yeni_dikte(self):
        """Ekrana her girişte önceki dikteyi temizler."""
        self.words = []
        self._etiket(DIKTE_YER_TUTUCU)

    def _etiket(self, metin, sonuc=""):
        self._son_metin = sonuc
        self.transcription_label.config(text=metin)

    # --- arka plan: dinle + tanı -------------------------------------------------------------

    def transcribe_audio(self):
        """Bir cümle dinler ve metne çevirir; iş parçacığında çalışır."""
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=self.DINLEME_ZAMAN_ASIMI_SN,
                                               phrase_time_limit=self.EN_UZUN_CUMLE_SN)
        except sr.WaitTimeoutError:
            return "", "Ses algılanmadı."
        except OSError as e:  # mikrofon yok / PyAudio sorunu
            return "", f"Mikrofon hatası: {e}"

        try:
            tanici = vosk.KaldiRecognizer(vosk_modeli(), 16000)
            tanici.AcceptWaveform(audio.get_raw_data(convert_rate=16000, convert_width=2))
            return json.loads(tanici.Result()).get("text", ""), ""
        except Exception as e:  # model eksik vb.
            return "", f"Tanıma hatası: {e}"

    def process_speech(self):
        self.sonuclar.put(self.transcribe_audio())

    # --- düğmeler -----------------------------------------------------------------------------

    def transcribe_and_update_label(self):
        if self.thread and self.thread.is_alive():
            return  # zaten dinleniyor
        self._etiket("Dinleniyor...")
        self.thread = threading.Thread(target=self.process_speech, daemon=True)
        self.thread.start()
        self.after(100, self._sonucu_bekle)

    def _sonucu_bekle(self):
        try:
            metin, hata = self.sonuclar.get_nowait()
        except queue.Empty:
            self.after(100, self._sonucu_bekle)
            return
        if metin:
            self._etiket(metin, sonuc=metin)
        else:
            self._etiket(hata or "Anlaşılamadı, tekrar deneyin.")

    def show_results(self):
        """Son tanınan cümleyi listeye ekler."""
        if self._son_metin:
            self.words.append(self._son_metin)
            print("Words:", self.words)
        self._etiket("")

    def navigate_and_show_results(self):
        """Bitir ve PDF al."""
        from lib.hand_detection.pdf import write_to_pdf

        if self.words:
            try:
                yol = write_to_pdf("sesle_yazı.pdf", "\n".join(self.words))
                messagebox.showinfo("PDF", f"Kaydedildi:\n{yol}")
            except Exception as e:
                messagebox.showerror("PDF", f"PDF yazılamadı: {e}")
                return
        else:
            print("kelime bulunamadı")
        self.yeni_dikte()
        self.controller.show_frame(anasayfa)


class optik(KameraEkrani):
    """Optik okuma ekranı. YARIM: fotoğraf çekiliyor ama henüz analiz edilmiyor
    (bkz. lib/detect_chics/detect_rectangles.py ve AGENTS.md)."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        canvas = tk.Canvas(self, bg="#47C4B6", height=320, width=480, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        self.button_image_1 = tk.PhotoImage(file=varlik("frame0", "button_1.png"))
        tk.Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0,
                  command=self.bitir, relief="flat").place(x=248.0, y=246.0, width=224.0, height=70.0)

        self.button_image_2 = tk.PhotoImage(file=varlik("frame0", "button_2.png"))
        tk.Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0,
                  command=self.take_photo, relief="flat").place(x=11.0, y=246.0, width=224.0, height=70.0)

        self.kamera_alanini_kur()

    def take_photo(self):
        self.fotograf_cek(OPTIK_FOTO)  # kamera açık kalır; yeniden çekilebilir

    def bitir(self):
        self.stop_camera()
        self.controller.show_frame(anasayfa)


if __name__ == "__main__":
    app = MainApplication()
    app.geometry("480x320")
    app.attributes("-fullscreen", True)
    app.resizable(False, False)
    app.title("SP akademik yardımcı")
    app.mainloop()
