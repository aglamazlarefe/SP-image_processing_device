import cv2
from pyzbar.pyzbar import decode

# QR kodunun bulunduğu fotoğrafın yolunu belirtin
image_path = 'foto/qr.jpg'

# Görüntüyü yükleyin
image = cv2.imread(image_path)

# QR kodunu tarayın ve çözün
qr_codes = decode(image)

# Bulunan QR kodlarını ve içeriklerini yazdırın
for qr_code in qr_codes:
    # QR kodunun dörtgen koordinatlarını alın
    rect = qr_code.rect
    points = qr_code.polygon

    # QR kodunun içeriğini alın
    qr_content = qr_code.data.decode('utf-8')
    print(f"QR Kod İçeriği: {qr_content}")

    # QR kodunun etrafına dikdörtgen çizin
    cv2.rectangle(image, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height), (0, 255, 0), 3)

# Sonuç görüntüsünü gösterin
cv2.imshow('QR Kod Algılandı', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
