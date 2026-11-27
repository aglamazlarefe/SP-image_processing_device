"""2. adım: düzleştirilmiş kâğıttaki kutuları bulur ve içlerindeki yazıyı OCR ile okur.

Sonuç `rectangles.p`'ye [kontur, yazı] listesi olarak kaydedilir; _finger_detect.py okur.
"""

import pickle

import cv2
import pytesseract

DUZ_FOTO = "duzunli_foto.jpg"
KUTU_DOSYASI = "lib/hand_detection/rectangles.p"
MIN_KUTU_ORANI = 0.005  # kutu, düzleştirilmiş kâğıt alanının en az %0,5'i olmalı


def is_within_bounds(rectangle, image_shape, padding=5):
    x, y, w, h = cv2.boundingRect(rectangle)
    return y > padding and x > padding and y + h < image_shape[0] - padding and x + w < image_shape[1] - padding


def kutulari_bul(duz_foto_yolu=DUZ_FOTO, cikti_yolu=KUTU_DOSYASI):
    """Kutuları bulur, OCR yapar, sonucu kaydeder ve bulunan kutu sayısını döndürür."""
    image = cv2.imread(duz_foto_yolu)
    if image is None:
        raise FileNotFoundError(f"Düzleştirilmiş fotoğraf okunamadı: {duz_foto_yolu}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 20)
    edges = cv2.Canny(thresh, 50, 280)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Küçük dörtgenler (QR kodun köşe işaretleri, gürültü) kutu sayılmaz. Örnek kâğıtta
    # (foto/foto_qr_2.jpg) gerçek kutular görüntünün >= %1,05'i, artıklar <= %0,27'si.
    # Eskiden findContours sırasındaki 9-11. öğeler siliniyordu; sıra OpenCV sürümüne göre
    # değiştiği için bu yanlış öğeyi siliyordu.
    en_kucuk_alan = MIN_KUTU_ORANI * image.shape[0] * image.shape[1]

    rectangles = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4 and is_within_bounds(approx, image.shape) \
                and cv2.contourArea(approx) >= en_kucuk_alan:
            rectangles.append(approx)

    rectangle_name = []
    for rectangle in rectangles:
        x, y, w, h = cv2.boundingRect(rectangle)
        roi_gray = cv2.cvtColor(image[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)
        _, roi_thresh = cv2.threshold(roi_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        roi_thresh = cv2.flip(roi_thresh, 1)  # görüntü aynalı; yazıyı düz okumak için çevrilir
        text = pytesseract.image_to_string(roi_thresh, lang="tur", config="--psm 9").strip()
        rectangle_name.append([rectangle, text])

    with open(cikti_yolu, "wb") as f:
        pickle.dump(rectangle_name, f)
    return len(rectangle_name)
