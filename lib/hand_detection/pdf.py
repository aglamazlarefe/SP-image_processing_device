from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os

pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))


def find_usb_mount_point():
    mounts = os.popen('lsblk -o NAME,MOUNTPOINT').read().splitlines()
    for mount in mounts:
        if '/media/' in mount or '/mnt/' in mount:
            parts = mount.split()
            if len(parts) == 2:
                return parts[1]
    return None


def write_to_pdf(output_path, text):
    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=A4)
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdf_canvas.setFont('Arial', 12)

    utf8_text = text.encode('utf-8')
    #pdf_canvas.drawString(100, 700, "tespit edilen sonuçlar\n")
    
    y_position = 680
    
    for line in utf8_text.split(b'\n'):
        pdf_canvas.drawString(100, y_position, line.decode('utf-8'))
        y_position -= 20

    pdf_canvas.save()
    buffer.seek(0)

    # usb dosya yolu bulma 
    
    usb_mount_point = find_usb_mount_point()
    if usb_mount_point:
        file_path = os.path.join(usb_mount_point, output_path)

    # PDF dosyasını masaüstüne kaydet
    USB_output_path = os.path.join(file_path, output_path)
    with open(USB_output_path, 'wb') as f:
        f.write(buffer.read())
    
    print(f'PDF başarıyla  kaydedildi: {USB_output_path}')



write_to_pdf("deneme1.pdf","""

bu bir deneme pdf'sidir 
             ich liebe AFL
             """ )