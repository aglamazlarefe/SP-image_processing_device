import cv2
from pyzbar.pyzbar import decode

# QR kodunun bulunduğu fotoğrafın yolunu belirtin
image_path = 'captured_photo.png'

# Görüntüyü yükleyin
image = cv2.imread(image_path)

# QR kodunu tarayın ve çözün
qr_codes = decode(image)
qr_content=""
# Bulunan QR kodlarını ve içeriklerini yazdırın
for qr_code in qr_codes:
    # QR kodunun dörtgen koordinatlarını alın
    rect = qr_code.rect
    points = qr_code.polygon

    # QR kodunun içeriğini alın
    qr_content = qr_code.data.decode('utf-8')
    

# Sonuç görüntüsünü gösterin
try:
    print(f"QR Kod İçeriği: {qr_content}")
except:
    print("hata")
cv2.waitKey(0)
cv2.destroyAllWindows()
