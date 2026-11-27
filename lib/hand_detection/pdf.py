"""Metni PDF'e yazar; USB bellek takılıysa oraya, değilse yerel `cikti/` klasörüne kaydeder."""

import os
import shutil
import subprocess

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

YEREL_CIKTI_KLASORU = "cikti"

# Türkçe karakterler (ğ, ş, ı, İ) için TrueType font gerekir. İlk bulunan kullanılır.
# Raspberry Pi OS'ta Arial yoktur; DejaVuSans genellikle kuruludur (fonts-dejavu-core).
FONT_ADAYLARI = [
    "Arial.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
]
FONT_ADI = "SPFont"
FONT_BOYUTU = 12
SATIR_ARALIGI = 20
KENAR_BOSLUGU = 72  # 1 inç

_font_adi = None


def _font():
    """Fontu bir kez kaydeder; hiçbiri bulunamazsa Helvetica (Türkçe harfler eksik çıkar)."""
    global _font_adi
    if _font_adi is None:
        for yol in FONT_ADAYLARI:
            try:
                pdfmetrics.registerFont(TTFont(FONT_ADI, yol))
                _font_adi = FONT_ADI
                break
            except Exception:  # reportlab bulamazsa çeşitli hata türleri fırlatır
                continue
        else:
            print("Uyarı: TrueType font bulunamadı, Helvetica kullanılıyor (Türkçe harfler bozuk çıkabilir)")
            _font_adi = "Helvetica"
    return _font_adi


def find_usb_mount_point():
    """Linux'ta /media veya /mnt altına bağlı ilk diski döndürür; yoksa None."""
    if not shutil.which("lsblk"):
        return None  # Windows veya lsblk olmayan sistem
    try:
        cikti = subprocess.run(["lsblk", "-nro", "MOUNTPOINT"], capture_output=True,
                               text=True, timeout=5, check=False).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    for satir in cikti.splitlines():
        # -r (raw) çıktısında boşluklar \x20 olarak kaçışlanır
        yol = satir.strip().replace("\\x20", " ")
        if yol.startswith(("/media/", "/mnt/")) and os.path.isdir(yol):
            return yol
    return None


def kayit_klasoru():
    return find_usb_mount_point() or YEREL_CIKTI_KLASORU


def write_to_pdf(dosya_adi, text):
    """`text`'i A4 PDF'e yazar ve kaydedilen dosyanın yolunu döndürür.

    `dosya_adi` yalnızca dosya adıdır (ör. "sesle_yazı.pdf"); klasörü bu fonksiyon seçer.
    Uzun satırlar kaydırılır, sayfa dolunca yeni sayfaya geçilir.
    """
    klasor = kayit_klasoru()
    os.makedirs(klasor, exist_ok=True)
    yol = os.path.join(klasor, os.path.basename(dosya_adi))

    font = _font()
    genislik, yukseklik = A4
    pdf = canvas.Canvas(yol, pagesize=A4)
    pdf.setFont(font, FONT_BOYUTU)
    y = yukseklik - KENAR_BOSLUGU

    for paragraf in text.split("\n"):
        satirlar = simpleSplit(paragraf, font, FONT_BOYUTU, genislik - 2 * KENAR_BOSLUGU) or [""]
        for satir in satirlar:
            if y < KENAR_BOSLUGU:
                pdf.showPage()
                pdf.setFont(font, FONT_BOYUTU)
                y = yukseklik - KENAR_BOSLUGU
            pdf.drawString(KENAR_BOSLUGU, y, satir)
            y -= SATIR_ARALIGI

    pdf.save()
    print(f"PDF kaydedildi: {yol}")
    return yol
