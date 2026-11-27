"""1. adım: çekilen fotoğrafta çalışma kâğıdını bulur ve düzleştirir.

Kâğıdın dört köşesi `map.p`'ye kaydedilir (canlı görüntüyü düzleştirmek için
_finger_detect.py kullanır); düzleştirilmiş kâğıt `duzunli_foto.jpg` olur (_rectangles.py okur).
"""

import pickle

import cv2
import numpy as np

CEKILEN_FOTO = "captured_photo.png"          # main.py'deki "fotoğraf çek" düğmesi yazar
HARITA_DOSYASI = "lib/hand_detection/map.p"
DUZ_FOTO = "duzunli_foto.jpg"

# Düzleştirilmiş kâğıdın boyutu (dikey A4 oranına yakın)
width, height = 1080, 1920


def find_largest_rectangle_contour(img):
    """Görüntüdeki en büyük konturu dörtgene yaklaştırır (kâğıdın kenarı olması beklenir)."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10
    )
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_rect = None
    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            largest_rect = cv2.approxPolyDP(contour, epsilon, True)
            max_area = area
    return largest_rect


def warp_image(img, points):
    """Dört köşeyi (width x height) boyutunda dik bir görüntüye taşır."""
    M = cv2.getPerspectiveTransform(
        points.astype(np.float32),
        np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32),
    )
    return cv2.warpPerspective(img, M, (width, height))


def sayfa_haritasini_cikar(foto_yolu=CEKILEN_FOTO, harita_yolu=HARITA_DOSYASI, cikti_yolu=DUZ_FOTO):
    """Kâğıdı bulur, köşeleri ve düzleştirilmiş görüntüyü kaydeder.

    Kâğıt (dört köşeli şekil) bulunamazsa False döner; bu durumda eski `map.p` KULLANILMAZ.
    """
    img = cv2.imread(foto_yolu)
    if img is None:
        raise FileNotFoundError(f"Fotoğraf okunamadı: {foto_yolu}")

    # _finger_detect.py canlı kareleri 180° döndürüp işler. Köşeler aynı koordinat sisteminde
    # olmalı, bu yüzden fotoğraf da aynı şekilde döndürülür. (Eskiden kullanılan sabit örnek
    # foto/foto_qr_2.jpg'de bu dönüş EXIF yönü olarak kayıtlıydı ve cv2.imread uyguluyordu.)
    img = cv2.rotate(img, cv2.ROTATE_180)

    largest_rect = find_largest_rectangle_contour(img)
    if largest_rect is None or len(largest_rect) != 4:
        return False

    # Not: köşeler approxPolyDP'nin verdiği sırayla kaydedilir (orijinal davranış).
    points = largest_rect.reshape(4, 2)
    with open(harita_yolu, "wb") as f:
        pickle.dump(points, f)

    cv2.imwrite(cikti_yolu, warp_image(img, points))
    return True
