"""Kamera, mikrofon ve Tesseract gerektirmeyen testler.

Çalıştırma (proje kökünden):  python -m unittest test_sp -v
Örnek kâğıt testleri `foto/foto_qr_2.jpg` yoksa atlanır (fotoğraf GPS bilgisi içerdiği için
depoda değil; yerel kopyadan çalıştırın).
"""

import os
import pathlib
import pickle
import shutil
import tempfile
import time
import unittest
from unittest import mock

import cv2
import numpy as np

from lib.hand_detection import _finger_detect as parmak
from lib.hand_detection import _mapping_offtime as harita
from lib.hand_detection import _rectangles as kutu
from lib.hand_detection import pdf
from lib.hand_detection.qr import qr_oku

ORNEK_KAGIT = "foto/foto_qr_2.jpg"
# Eski kodun (2024) bu kâğıttan ürettiği map.p ve rectangles.p ile karşılaştırılarak bulundu
BEKLENEN_KOSELER = [[1311, 31], [639, 36], [641, 1045], [1314, 1041]]
BEKLENEN_KUTU_SAYISI = 9
BEKLENEN_QR = "AFL26 - numara 287"


class GeciciKlasor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sp_test_")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def yol(self, ad):
        return os.path.join(self.tmp, ad)


class PdfTesti(GeciciKlasor):
    def test_turkce_ve_cok_sayfa(self):
        with mock.patch.object(pdf, "find_usb_mount_point", return_value=None), \
                mock.patch.object(pdf, "YEREL_CIKTI_KLASORU", self.tmp):
            yol = pdf.write_to_pdf("deneme.pdf", "çğıöşü ÇĞİÖŞÜ\n" + "\n".join(map(str, range(80))))
        veri = pathlib.Path(yol).read_bytes()
        self.assertTrue(veri.startswith(b"%PDF"))
        self.assertTrue(b"/Count 2" in veri or b"/Count 3" in veri, "sayfa sonu yok")
        self.assertEqual(os.path.dirname(yol), self.tmp)


@unittest.skipUnless(os.path.exists(ORNEK_KAGIT), f"{ORNEK_KAGIT} yok")
class OrnekKagitTesti(GeciciKlasor):
    def ham_kare(self):
        """Örneği, kameranın vereceği gibi (EXIF dönüşü uygulanmamış) kaydeder."""
        ham = cv2.imread(ORNEK_KAGIT, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION)
        cv2.imwrite(self.yol("ham.png"), ham)
        return self.yol("ham.png")

    def test_harita_kutular_qr(self):
        self.assertTrue(harita.sayfa_haritasini_cikar(self.ham_kare(), self.yol("map.p"), self.yol("duz.jpg")))
        self.assertEqual(pickle.loads(pathlib.Path(self.yol("map.p")).read_bytes()).tolist(), BEKLENEN_KOSELER)
        self.assertEqual(cv2.imread(self.yol("duz.jpg")).shape[:2], (1920, 1080))

        with mock.patch.object(kutu.pytesseract, "image_to_string", return_value=" KUTU\n\x0c"):
            n = kutu.kutulari_bul(self.yol("duz.jpg"), self.yol("rect.p"))
        self.assertEqual(n, BEKLENEN_KUTU_SAYISI)
        self.assertTrue(all(t == "KUTU" for _, t in pickle.loads(pathlib.Path(self.yol("rect.p")).read_bytes())))

        self.assertEqual(qr_oku(ORNEK_KAGIT), BEKLENEN_QR)

    def test_kagit_yoksa_false(self):
        cv2.imwrite(self.yol("bos.png"), np.zeros((1080, 1920, 3), np.uint8))
        self.assertFalse(harita.sayfa_haritasini_cikar(self.yol("bos.png"), self.yol("m.p"), self.yol("d.jpg")))
        self.assertFalse(os.path.exists(self.yol("m.p")))

    def test_eksik_foto(self):
        with self.assertRaises(FileNotFoundError):
            harita.sayfa_haritasini_cikar(self.yol("yok.png"))


class SecimSayaciTesti(unittest.TestCase):
    KARE = [(np.array([[[100, 100]], [[300, 100]], [[300, 300]], [[100, 300]]], np.int32), "A")]

    def adim(self, an, giris, secilen, nokta=(200, 200)):
        katman = np.zeros((400, 400, 3), np.uint8)
        with mock.patch.object(parmak.time, "time", return_value=an):
            parmak.create_overlay_image(self.KARE, nokta, katman, giris, secilen)

    def test_uc_saniyede_secilir(self):
        giris, secilen = {}, []
        self.adim(1000.0, giris, secilen)
        self.adim(1002.0, giris, secilen)
        self.assertEqual(secilen, [])
        self.adim(1003.1, giris, secilen)
        self.assertEqual(secilen, ["A"])

    def test_cikinca_sayac_sifirlanir(self):
        giris, secilen = {}, []
        self.adim(1000.0, giris, secilen)
        parmak.eski_girisleri_temizle(giris, simdi=1001.0)
        self.adim(1003.5, giris, secilen)
        self.assertEqual(secilen, [], "eski giriş zamanıyla anında seçildi")

    def test_kisa_kayip_tolere_edilir(self):
        giris = {"A": [1000.0, 1000.0]}
        parmak.eski_girisleri_temizle(giris, simdi=1000.0 + parmak.TOLERANS_SN / 2)
        self.assertIn("A", giris)


if __name__ == "__main__":
    unittest.main()
