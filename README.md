# SP-image_processing_device — SP akademik yardımcı

480x320 dokunmatik ekranlı küçük bir Linux cihazı (Raspberry Pi hedefli) için Tkinter uygulaması. Üç özelliği var:

| Özellik | Durum | Ne yapar |
|---|---|---|
| **El tanıma** | çalışıyor | Kâğıdın fotoğrafını çeker. Kâğıdı ve kutuları bulup kutulardaki yazıları OCR ile okur. Ardından kamera önünde işaret parmağı izlenir; parmak bir kutuda 3 sn kalınca o kutu seçilir. Kâğıttaki QR içeriği ve seçilen kutular PDF'e yazılır. |
| **Sesle yazma** | çalışıyor | Vosk ile çevrimdışı Türkçe konuşma tanıma. Cümleler listeye eklenir, "bitir" düğmesi PDF yazar. |
| **Optik** | yarım | Fotoğraf çekiyor, henüz analiz etmiyor (`lib/detect_chics/`). |

PDF'ler USB bellek takılıysa (`/media/...` veya `/mnt/...`) oraya, değilse proje kökündeki `cikti/` klasörüne kaydedilir.

## Donanım

- Kamera (indeks 0, 1920x1080 istenir)
- Mikrofon
- 480x320 dokunmatik ekran (uygulama tam ekran açılır)
- İsteğe bağlı USB bellek

## Kurulum

1. Python 3.10 ile sanal ortam kurup bağımlılıkları yükleyin:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```
2. Sistem paketlerini kurun:
   - **Tesseract ve Türkçe dil verisi:** `sudo apt install tesseract-ocr tesseract-ocr-tur`
   - **zbar** (QR okuma için): `sudo apt install libzbar0`
   - **PortAudio** (PyAudio için): `sudo apt install portaudio19-dev`
   - **Türkçe karakterli font:** Raspberry Pi OS'ta Arial yoktur; `fonts-dejavu-core` kurulu olmalıdır.
3. Vosk Türkçe modelini indirin. Model ~57 MB ve depoda yok:
   ```bash
   cd lib/voice_recognation
   wget https://alphacephei.com/vosk/models/vosk-model-small-tr-0.3.zip
   unzip vosk-model-small-tr-0.3.zip && rm vosk-model-small-tr-0.3.zip
   ```
4. El modeli: cvzone ilk el tanımada `hand_landmarker.task` dosyasını proje köküne indirir. Cihazın o anda internete bağlı olması gerekir; ya da dosyayı başka bir makineden kopyalayın.

## Çalıştırma

Proje kökünden çalıştırın; tüm yollar köke göredir:

```bash
.venv/bin/python main.py
```

## Test

Kamera, mikrofon ve Tesseract gerektirmeyen testler:

```bash
.venv/bin/python -m unittest test_sp -v
```

Örnek kâğıt testleri `foto/foto_qr_2.jpg` dosyası yoksa atlanır. Bu fotoğraf GPS bilgisi içerdiği için depoda tutulmuyor.

## El tanıma akışı

```
main.py "fotoğraf çek"  -> captured_photo.png
_mapping_offtime.py     -> kâğıdın köşeleri: lib/hand_detection/map.p, düz kâğıt: duzunli_foto.jpg
_rectangles.py (OCR)    -> kutular ve yazıları: lib/hand_detection/rectangles.p
qr.py                   -> QR içeriği
_finger_detect.py       -> canlı kamera + parmak takibi -> selected_countries.pdf
```

Bu ara dosyalar her çalıştırmada yeniden üretilir ve `.gitignore`'dadır.
