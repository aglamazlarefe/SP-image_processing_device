import cv2
import numpy as np

def separate_white_and_color(image_path, color_threshold=100):
    # Resmi oku
    image = cv2.imread(image_path)

    # Görüntüyü BGR renk uzayından HSV renk uzayına dönüştür
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Daraltılmış beyaz renk aralığını belirle
    lower_white = np.array([0, 0, 200], dtype=np.uint8)
    upper_white = np.array([255, 20, 255], dtype=np.uint8)

    # Belirlenen beyaz aralığındaki pikselleri beyaz olarak işaretle
    white_mask = cv2.inRange(hsv_image, lower_white, upper_white)

    # Diğer renkler için ters maske oluştur
    color_mask = cv2.bitwise_not(white_mask)

    # Orijinal görüntü üzerine maskeleme yap
    white_result = cv2.bitwise_and(image, image, mask=white_mask)
    color_result = cv2.bitwise_and(image, image, mask=color_mask)

    # Sonuçları göster
    cv2.imshow('Original Image', image)
    cv2.imshow('White Areas', white_result)
    cv2.imshow('Colored Areas', color_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# Görüntü dosya yolu
image_path = "foto/alignment2.jpg"

# Beyaz renk için eşik değeri
color_threshold = 100

# Fonksiyonu çağır
separate_white_and_color(image_path, color_threshold)
