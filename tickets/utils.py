import qrcode
from io import BytesIO
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

def generate_ticket_pdf(ticket):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.drawString(100, 750, f"Vizit Africa Ticket")
    p.drawString(100, 720, f"Booking ID: {ticket.booking.id}")
    p.drawString(100, 690, f"Payment ID: {ticket.payment.id}")
    p.drawString(100, 660, f"Total: {ticket.booking.total_amount} {ticket.booking.currency}")
    p.drawString(100, 630, f"Issued: {ticket.issued_at.strftime('%Y-%m-%d %H:%M')}")
    
    p.showPage()
    p.save()
    
    pdf_file = ContentFile(buffer.getvalue())
    filename = f"ticket_{ticket.booking.id}_{ticket.payment.id}.pdf"
    
    return default_storage.save(f"tickets/{filename}", pdf_file)
