from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from io import BytesIO




pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

def write_to_pdf(output_path, text):
    # Create a PDF document
    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=A4)

    # Set Turkish font and size
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdf_canvas.setFont('Arial', 12)

    # Encode text to UTF-8
    utf8_text = text.encode('utf-8')

    # Write text to PDF
    pdf_canvas.drawString(100, 700, "tespit edilen şıklar")
    
    y_position = 680  # Initial y position for the text
    
    for line in utf8_text.split(b'\n'):
        pdf_canvas.drawString(100, y_position, line.decode('utf-8'))
        y_position -= 20  # Adjust the y position for the next line

    # Save the PDF document
    pdf_canvas.save()

    # Move the buffer cursor to the beginning
    buffer.seek(0)

    # Write the buffer content to the output file
    with open(output_path, 'wb') as f:
        f.write(buffer.read())
