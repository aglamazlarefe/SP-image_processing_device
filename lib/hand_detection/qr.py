"""Fotoğraftaki QR kod(lar)ını okur."""

import cv2
from pyzbar.pyzbar import decode


def qr_oku(foto_yolu):
    """Fotoğraftaki QR kodların içeriğini satır satır döndürür; QR yoksa boş metin.

    Fotoğraf okunamazsa FileNotFoundError fırlatır.
    """
    goruntu = cv2.imread(foto_yolu)
    if goruntu is None:
        raise FileNotFoundError(f"Fotoğraf okunamadı: {foto_yolu}")
    icerikler = [kod.data.decode("utf-8", errors="replace") for kod in decode(goruntu)]
    return "\n".join(icerikler)
