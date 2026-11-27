# SP-image_processing_device — ajan rehberi

"SP akademik yardımcı": 480x320 dokunmatik ekranlı bir Linux cihazı (Raspberry Pi hedefli) için Tkinter uygulaması. Okul/yarışma prototipi. Özellikler ve kurulum `README.md`'de.

**En önemli sınır:** Bu makinede kamera, dokunmatik ekran, Raspberry Pi ve Tesseract **yok**. Kameraya, ekrana veya OCR'a dokunan bir değişikliği burada uçtan uca doğrulayamazsın. Neyi test ettiğini ve neyin cihazda denenmesi gerektiğini her seferinde açıkça yaz.

## Çalıştırma ve test

Her şey **proje kökünden** çalıştırılır; tüm dosya yolları köke göredir (`lib/...`, `Screens/...`).

```powershell
.venv\Scripts\python -m unittest test_sp -v    # 7 test; kamera/mikrofon/Tesseract gerekmez
.venv\Scripts\python main.py                   # uygulama (tam ekran açılır; Alt+F4 ile kapat)
```

- `.venv` Python **3.10** ile kurulmalı (cihazla aynı sürüm): `py -3.10 -m venv .venv`, ardından `.venv\Scripts\python -m pip install -r requirements.txt`.
- Örnek kâğıt testleri `foto/foto_qr_2.jpg` dosyasını ister. Bu dosya yalnızca yerelde durur; yoksa testler atlanır, bu normaldir.

## Mimari

`main.py` içinde `MainApplication(tk.Tk)` beş ekranı (`tk.Frame`) üst üste tutar ve `show_frame` ile birini öne getirir. Kamera kullanan ekranlar (`el_tanıma_1`, `optik`) `KameraEkrani` sınıfından türer ve her girişte `yeni_ekran()` ile sıfırdan kurulur.

| Ekran sınıfı | Görsel klasörü | Görev |
|---|---|---|
| `anasayfa` | `Screens/assets/frame4` | ana menü |
| `optik` | `frame0` | **yarım**: fotoğraf çeker, analiz etmez |
| `el_tanıma_1` | `frame1` | kâğıdın fotoğrafını çeker → "devam" düğmesi işlem hattını başlatır |
| `el_tanıma_2` | `frame2` | "bitti, ana sayfaya dön" ekranı |
| `speech_reco` | `frame3` | sesle yazma → PDF |

**El tanıma işlem hattı** (`el_tanıma_1.next_page`). Adımlar sırayla çağrılır ve birbirine **dosya** yoluyla veri aktarır:

```
captured_photo.png
  └─ _mapping_offtime.sayfa_haritasini_cikar()  -> lib/hand_detection/map.p (4 köşe) + duzunli_foto.jpg (1080x1920)
       └─ _rectangles.kutulari_bul()            -> lib/hand_detection/rectangles.p ([kontur, OCR yazısı] listesi)
qr.qr_oku(captured_photo.png)                   -> QR metni
_finger_detect.parmakla_sec(qr)                 -> OpenCV tam ekran penceresi; Exit'e basınca selected_countries.pdf
```

Ses tanıma: düğme bir iş parçacığı başlatır (`sr.Microphone` → Vosk). Sonuç `queue.Queue` üzerinden gelir ve `_sonucu_bekle` (Tk `after` ile) ekrana yazar.

PDF yazımı: `lib/hand_detection/pdf.py` içindeki `write_to_pdf(dosya_adı, metin)`. Dosyayı USB bellek varsa oraya, yoksa `cikti/` klasörüne kaydeder ve tam yolu döndürür.

## Değişmezler — bunları bozma

1. **Canlı kareler 180° döndürülür** (`_finger_detect.py`, `cv2.rotate(img, cv2.ROTATE_180)`) **ve çekilen fotoğraf da aynı şekilde döndürülür** (`_mapping_offtime.sayfa_haritasini_cikar`). `map.p`'deki köşeler canlı karelerin koordinat sisteminde olmalı. Birini değiştirirsen ötekini de değiştir ve `test_sp` testini çalıştır; beklenen köşeler testte sabit yazılıdır.
2. **`lib/` modülleri import edildiğinde iş yapmamalı.** Eskiden her adım bir betikti ve import anında çalışıyordu; bu yüzden düğme oturumda yalnızca bir kez çalışıyordu ve `pdf.py` her import'ta çöküyordu. Yeni kod fonksiyon olarak yazılır ve `main.py`'den çağrılır.
3. **Tk widget'larına iş parçacığından dokunma.** Ses tanımadaki `Queue` + `after` deseninin aynısını kullan. Tk iş parçacığında `thread.join()` çağırma; arayüz donar.
4. **Kamera ekranından çıkarken `stop_camera()` çağır.** Bu fonksiyon hem kamerayı serbest bırakır hem de `after` ile kurulan yenileme döngüsünü iptal eder. Yeni bir kamera ekranı açmak için `controller.yeni_ekran(Sinif)` kullan.
5. **Bütün ekran görselleri `Screens/assets/...` altında, büyük S ile durur.** Git bir ara hem `screens/` hem `Screens/` izliyordu. Windows bu farkı gizler, ama Linux cihazda uygulama açılmaz. Yeni görsel eklerken yolun harf büyüklüğüne dikkat et.
6. **cvzone 2.x kullanılmalı.** cvzone 1.x, MediaPipe'ın eski `mp.solutions` API'sini kullanır ve yeni mediapipe sürümlerinde bu API yok. cvzone 2.x ilk çalıştırmada `hand_landmarker.task` dosyasını köke indirir.
7. **Şunları depoya ekleme:** Vosk modelleri (yaklaşık 57 MB), çalışma zamanı fotoğrafları, `*.p` dosyaları, `cikti/`, `foto/` (GPS EXIF bilgisi içerebilir). Depo geçmişi bu dosyalardan temizlendi; `.gitignore` artık engelliyor.
8. **Kutu filtresi alana dayanır** (`_rectangles.MIN_KUTU_ORANI = 0.005`). Eskiden `findContours` çıktısında 9-11. sıradaki öğeler siliniyordu; bu sıra OpenCV sürümüne göre değişiyor. Sıra numarasına göre silme mantığını geri getirme.

## Cihazda doğrulanması gerekenler

Kullanıcıya liste olarak ver:
- El tanıma: yeni bir kâğıt fotoğrafı çek → "devam". Kutular doğru yerde görünmeli; parmak 3 sn bekleyince kutu seçilmeli; Exit'e basınca PDF USB'ye yazılmalı. Düğme aynı oturumda **ikinci kez** de çalışmalı.
- Sesle yazma: konuş → "ekle" → "bitir". PDF'te Türkçe harfler doğru çıkmalı (DejaVu fontu gerekir).
- Ekranlar arasında birkaç kez gidip gelince uygulama yavaşlamamalı (eski kamera döngüleri kapanıyor mu?).

## Açık görevler

- **Canlı görüntü boyutu** (`_finger_detect.warp_image`). Düzleştirme hedefi dikey 1080x1920, ama çıktı (1920, 1080) boyutunda üretiliyor. Bu yüzden ekranda kâğıdın alt yaklaşık %44'ü görünmüyor; seçim yine de çalışıyor. Sonra görüntü 480x320'ye sıkıştırılıyor. Doğru düzen cihazda görülerek seçilmeli. **Kabul ölçütü:** kâğıdın tamamı ekranda, en-boy oranı bozulmadan görünür.
- **Optik okuma** (`lib/detect_chics/detect_rectangles.py`). Hiçbir düğmeye bağlı değil ve çalışmıyor:
  - `captured_image.jpg` okuyor, oysa ekran `captured_photo_optic.png` yazıyor;
  - `reshape(4,2)` dört köşesi olmayan şekillerde çöküyor (97. satır);
  - OCR, `roi` yerine bütün görüntü üzerinde çalışıyor (121. satır);
  - 15-43 ve 46-74. satırlardaki fonksiyonlar birbirinin kopyası.

  Bu bir özellik geliştirme işi; ne yapması gerektiğini önce sahibine sor.
- **Köşe sırası** (`_mapping_offtime.py`). `approxPolyDP`'nin verdiği köşe sırası olduğu gibi kullanılıyor. Kâğıt farklı açıyla çekilirse düzleştirme ters veya aynalı çıkabilir. Köşeleri sol üst → sağ üst → sağ alt → sol alt sırasına koymak daha sağlam olur. Ancak bu değişiklik `_finger_detect.py`'deki `cv2.flip` ve `_rectangles.py`'deki OCR aynalamasını da etkiler; üçü birlikte ele alınmalı ve cihazda denenmeli.
- **Kutu adları anahtar olarak kullanılıyor** (`_finger_detect.create_overlay_image`). OCR iki kutuya aynı yazıyı verirse ikisi tek kutu gibi davranır.
- **Mikrofon gürültüsü.** `speech_reco.transcribe_audio` içinde `adjust_for_ambient_noise` yok; gürültülü ortamda dinleme hemen bitebilir.
