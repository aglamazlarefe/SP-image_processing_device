from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os

pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

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

    # Kullanıcının masaüstü dizini
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

    # PDF dosyasını masaüstüne kaydet
    desktop_output_path = os.path.join(desktop_path, output_path)
    with open(desktop_output_path, 'wb') as f:
        f.write(buffer.read())
    
    print(f'PDF başarıyla  kaydedildi: {desktop_output_path}')


write_to_pdf("el_isaret_sonuc.pdf","""

AFL26 - numara 287    
                      
tespit edilen sonuçlar:

Aşıkkı
C şıkkı         
""")