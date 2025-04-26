from io import BytesIO
from reportlab.pdfgen import canvas

def generate_invoice_pdf(plan_name, amount, date):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setTitle("TweetApp Invoice")
    p.drawString(100, 800, "TweetApp Subscription Invoice")
    p.drawString(100, 770, f"Plan: {plan_name}")
    p.drawString(100, 750, f"Amount Paid: ₹{amount}")
    p.drawString(100, 730, f"Date: {date}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
