import cv2
import numpy as np
import pytesseract
import playsound

# Tesseract OCR'yi başlat
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Tesseract'in yolu

def draw_reference_line(image, y_coordinate):
    # Referans çizgisini çiz
    cv2.line(image, (0, y_coordinate), (image.shape[1], y_coordinate), (0, 255, 0), 2)

def preprocess_image(image):
    # Önceden işleme ekleyebilirsiniz (örneğin, bulanıklaştırma, eşikleme, vb.)
    # Bu, OCR'nin daha az hassas çalışmasına yardımcı olabilir
    # Örnek olarak: image = cv2.GaussianBlur(image, (5, 5), 0)
    return image

def detect_text(image):
    # Görüntü üzerinde OCR kullanarak metni tespit et
    text_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config='--psm 6')  # --psm 6: Assume a single uniform block of text.
    return text_data

def calculate_alignment(text_data, reference_line):
    # Metin bloklarının sayısı
    num_blocks = len(text_data['text'])

    # Yazının hizasını temsil eden değer
    alignment_sum = 0

    # Her bir metin bloğunu kontrol et
    for i in range(num_blocks):
        # Sadece metin içeren blokları ele al
        if int(text_data['conf'][i]) > 0:
            # Sol üst köşenin y koordinatını al ve topla
            alignment_sum += int(text_data['top'][i])

    # Yazının hizasını temsil eden ortalama değeri hesapla
    alignment_average = alignment_sum / num_blocks

    # Referans çizgisine göre hizalamayı hesapla
    alignment_offset = alignment_average - reference_line

    return alignment_offset

def main():
    # Örnek bir görüntü yolu
    image_path = "C:/Users/aglam/Documents/python projeleri/SP-image_processing_device/foto/duz.jpg"

    # Görüntüyü oku
    frame = cv2.imread(image_path)

    # Görüntü başarıyla okunmuşsa devam et
    if frame is not None:
        
        
        
        text = pytesseract.image_to_string(frame)
        print(text)

        
        
        # Referans çizgisini yüksekliği
        reference_line_height = 100  # Görüntünün üstünden başlayarak referans çizgisinin yüksekliği

        # Referans çizgisini çiz
        draw_reference_line(frame, reference_line_height)

        # Görüntüyü önceden işle
        preprocessed_frame = preprocess_image(frame)

        # Görüntü üzerinde OCR uygula
        text_data = detect_text(preprocessed_frame)

        # Referans çizgisine göre yazının hizasını hesapla
        alignment_offset = calculate_alignment(text_data, reference_line_height)

        # Eşik değeri
        threshold = 20  # Eğer hizalama bu değeri aşarsa alarm çalacak

        # Eğer hizalama bozulduysa, alarmı çal
        if abs(alignment_offset) > threshold:
            print('Hizalama Bozuldu! Alarm Çalınıyor...')
            # Ses çalma işlemi (örneğin playsound kütüphanesi kullanılarak)

        # Görüntüyü ekranda göster
        cv2.imshow('Image', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('Görüntü okunamadı!')

if __name__ == "__main__":
    main()
