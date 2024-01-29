import cv2
import pytesseract

# Tesseract OCR'nin yüklenmesi
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Tesseract OCR'nin yolunu güncelleyin

# Video akışı başlatma (örneğin, bir dosyadan veya kameradan)
video_capture = cv2.VideoCapture('video.mp4')  # Video dosyasının adını veya kamera numarasını güncelleyin

while True:
    # Çerçeveyi yakalama
    ret, frame = video_capture.read()

    # Okuma işlemi başarılı olduysa devam et
    if not ret:
        print("Video sona erdi veya okuma hatası!")
        break

    # Görüntüyü uygun formata dönüştürme (BGR'den RGB'ye)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Tesseract OCR ile metni çerçeveleme
    boxes = pytesseract.image_to_boxes(rgb_frame)

    # Çerçeve üzerine dikdörtgen kutuları çizme
    for b in boxes.splitlines():
        b = b.split()
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        frame = cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)

    # Sonuçları gösterme
    cv2.imshow('Text Detection', frame)

    # Çıkış için 'q' tuşuna basma kontrolü
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Video akışını serbest bırakma ve pencereyi kapatma
video_capture.release()
cv2.destroyAllWindows()
