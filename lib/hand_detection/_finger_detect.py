"""3. adım: canlı kamerada işaret parmağını izler; parmak bir kutuda 3 sn kalınca kutu seçilir.

Seçilen kutuların yazıları (ve kâğıttaki QR içeriği) PDF'e yazılır.
Akıştaki önceki adımlar: _mapping_offtime.py (map.p) ve _rectangles.py (rectangles.p).
"""

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import pickle
import time

import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector

from lib.hand_detection.pdf import write_to_pdf

button_x, button_y, button_width, button_height = 11, 11, 75, 35
button_text = "Exit"

cam_id = 0
# Düzleştirilmiş kâğıt koordinatları (_mapping_offtime.py ile aynı olmalı)
width, height = 1080, 1920
map_file_path = "lib/hand_detection/map.p"
countries_file_path = "lib/hand_detection/rectangles.p"
PENCERE = "Output Image"
SECIM_SURESI_SN = 3
TOLERANS_SN = 0.5  # parmak bu kadar süre görünmezse kutunun sayacı sıfırlanır
EN_FAZLA_BOS_KARE = 30  # art arda bu kadar kare okunamazsa kamera kopmuş sayılır


def warp_image(img, points):
    """Canlı kareyi kâğıdın köşelerine göre düzleştirir; görüntüyü ve dönüşüm matrisini döndürür.

    Not (cihazda doğrulanmalı): hedef köşeler 1080x1920 (dikey), çıktı boyutu ise
    (1920 genişlik, 1080 yükseklik). Bu yüzden ekranda kâğıdın alt kısmı görünmez; seçim
    yine de tüm kâğıtta çalışır çünkü parmak konumu matrisle ayrıca dönüştürülür.
    """
    points = points.astype(np.float32)
    matrix = cv2.getPerspectiveTransform(
        points, np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32))
    imgOutput = cv2.warpPerspective(img, matrix, (height, width))
    return imgOutput, matrix


def warp_single_point(point, matrix):
    """Tek bir noktayı perspektif matrisiyle dönüştürür."""
    point_homogeneous = np.array([[point[0], point[1], 1]], dtype=np.float32)
    transformed = np.dot(matrix, point_homogeneous.T).T
    return transformed[0, :2] / transformed[0, 2]


def get_finger_location(detector, img, imgWarped, matrix):
    """İşaret parmağı ucunun düzleştirilmiş görüntüdeki konumu; el yoksa None."""
    hands, img = detector.findHands(img, draw=False, flipType=True)
    if not hands:
        return None
    indexFinger = hands[0]["lmList"][8][0:2]
    warped_point = warp_single_point(indexFinger, matrix)
    warped_point = int(warped_point[0]), int(warped_point[1])
    cv2.circle(imgWarped, warped_point, 5, (255, 0, 0), cv2.FILLED)
    return warped_point


def create_overlay_image(polygons, warped_point, imgOverlay, entry_times, selected):
    """Parmağın bulunduğu kutuyu boyar; 3 sn dolunca kutuyu `selected` listesine ekler.

    `entry_times`: kutu adı -> [parmağın kutuya girdiği an, kutuda son görüldüğü an].
    Parmak kutudan çıkınca sayaç sıfırlanır (bkz. eski_girisleri_temizle).
    """
    simdi = time.time()
    for polygon, name in polygons:
        polygon_np = np.array(polygon, np.int32).reshape((-1, 1, 2))
        if cv2.pointPolygonTest(polygon_np, warped_point, False) < 0:
            continue
        if name not in entry_times:
            entry_times[name] = [simdi, simdi]
        entry_times[name][1] = simdi
        time_in_box = simdi - entry_times[name][0]

        if time_in_box >= SECIM_SURESI_SN:
            color = (255, 0, 0)  # mavi (BGR): seçildi
            if name not in selected:
                selected.append(name)
        else:
            color = (255, 0, 255)  # pembe: bekleniyor; parmağın üstünde dolan daire
            angle = int((time_in_box / SECIM_SURESI_SN) * 360)
            cv2.ellipse(imgOverlay, (warped_point[0], warped_point[1] - 100), (50, 50), 0, 0, angle,
                        color, thickness=-1)

        cv2.polylines(imgOverlay, [np.array(polygon)], isClosed=True, color=color, thickness=2)
        cv2.fillPoly(imgOverlay, [np.array(polygon)], color)
        cvzone.putTextRect(imgOverlay, name, tuple(polygon[0][0]), scale=1, thickness=1)

    return imgOverlay


def eski_girisleri_temizle(entry_times, simdi=None):
    """Parmağın TOLERANS_SN'den uzun süredir görülmediği kutuların sayacını sıfırlar.

    Eskiden sayaç hiç sıfırlanmıyordu: daha önce dokunulan bir kutuya dönmek onu anında
    seçiyordu. Tolerans, el algılamanın tek tük kaçırdığı karelerde sayacın sıfırlanmasını önler.
    """
    simdi = time.time() if simdi is None else simdi
    for name in [n for n, (_giris, son) in entry_times.items() if simdi - son > TOLERANS_SN]:
        del entry_times[name]


def draw_exit_button(img):
    cv2.rectangle(img, (button_x, button_y), (button_x + button_width, button_y + button_height),
                  (255, 0, 0), cv2.FILLED)
    cv2.putText(img, button_text, (button_x + 10, button_y + 17), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)


def _yukle(yol):
    with open(yol, "rb") as f:
        return pickle.load(f)


def parmakla_sec(qr_content="", pdf_adi="selected_countries.pdf"):
    """Parmakla seçim ekranını açar; Exit'e basılınca kapanır.

    Seçilen kutu yazılarının listesini döndürür; en az bir seçim varsa PDF de yazar.
    """
    map_points = _yukle(map_file_path)
    polygons = _yukle(countries_file_path)
    print(f"{len(polygons)} kutu yüklendi.")

    cap = cv2.VideoCapture(cam_id)
    if not cap.isOpened():
        raise RuntimeError("Kamera açılamadı")
    # Not: değişken adları ters ama sonuç 1920x1080 istemektir (3 = genişlik, 4 = yükseklik)
    cap.set(4, width)
    cap.set(3, height)

    detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5,
                            minTrackCon=0.5)
    entry_times = {}
    selected = []
    durum = {"cikis": False}

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and button_x < x < button_x + button_width \
                and button_y < y < button_y + button_height:
            durum["cikis"] = True

    cv2.namedWindow(PENCERE, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(PENCERE, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(PENCERE, mouse_callback)

    bos_kare = 0
    try:
        while not durum["cikis"]:
            success, img = cap.read()
            if not success:
                bos_kare += 1
                if bos_kare >= EN_FAZLA_BOS_KARE:
                    print("Kameradan görüntü alınamıyor, çıkılıyor.")
                    break
                cv2.waitKey(10)
                continue
            bos_kare = 0

            img = cv2.rotate(img, cv2.ROTATE_180)
            imgWarped, matrix = warp_image(img, map_points)
            imgOutput = imgWarped.copy()
            warped_point = get_finger_location(detector, img, imgWarped, matrix)

            h, w, _ = imgWarped.shape
            imgOverlay = np.zeros((h, w, 3), dtype=np.uint8)
            for polygon, _name in polygons:
                cv2.polylines(imgOverlay, [np.array(polygon)], isClosed=True, color=(0, 255, 0), thickness=2)
                cv2.fillPoly(imgOverlay, [np.array(polygon)], (0, 255, 0))
            if warped_point:
                imgOverlay = create_overlay_image(polygons, warped_point, imgOverlay, entry_times, selected)
                imgOutput = cv2.addWeighted(imgWarped, 1, imgOverlay, 0.7, 0)
            eski_girisleri_temizle(entry_times)

            imgOutput = cv2.flip(imgOutput, 1)
            imgOutput = cv2.resize(imgOutput, (480, 320))
            draw_exit_button(imgOutput)
            cv2.imshow(PENCERE, imgOutput)
            cv2.waitKey(1)
    finally:
        cap.release()
        cv2.destroyWindow(PENCERE)

    if selected:
        metin = f"{qr_content}\n\n" + "\n".join(selected)
        write_to_pdf(pdf_adi, metin)
    return selected
