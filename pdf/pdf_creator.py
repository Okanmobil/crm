from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader


class PDFCreator:
    def __init__(self, output_path, logo_path=None):
        self.output_path = output_path
        self.logo_path = logo_path
        self.width, self.height = A4

        pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))

    def create_proposal(self, proposal_data):
        pdf = canvas.Canvas(self.output_path, pagesize=A4)

        # Başlık
        pdf.setFont("Arial", 16)
        pdf.drawString(50, self.height - 50, "Teklif Belgesi")

        # Logo
        if self.logo_path:
            try:
                logo = ImageReader(self.logo_path)
                pdf.drawImage(logo, self.width - 200, self.height - 160, width=120, height=80, preserveAspectRatio=True, mask="auto")
            except Exception as e:
                print(f"Logo yüklenirken hata oluştu: {e}")

        # Teklif ve Müşteri Bilgileri
        pdf.setFont("Arial", 10)
        pdf.drawString(50, self.height - 100, f"Teklif No: {proposal_data['reference']}")
        pdf.drawString(50, self.height - 115, f"Düzenleme Tarihi: {proposal_data['edit_date']}")
        pdf.drawString(50, self.height - 130, f"Geçerlilik Tarihi: {proposal_data['validity_date']}")
        pdf.drawString(50, self.height - 145, f"Müşteri: {proposal_data['customer_name']}")
        pdf.drawString(50, self.height - 160, f"Adres: {proposal_data['customer_address']}")

        # Hizmet Kalemleri
        y_position = self.height - 200
        pdf.drawString(50, y_position, "Hizmet Adı")
        pdf.drawString(200, y_position, "Miktar")
        pdf.drawString(300, y_position, "Birim Fiyat")
        pdf.drawString(400, y_position, "Para Birimi")
        pdf.drawString(500, y_position, "Toplam")
        y_position -= 20

        for item in proposal_data["items"]:
            pdf.drawString(50, y_position, item["service"])
            pdf.drawString(200, y_position, item["quantity"])
            pdf.drawString(300, y_position, item["unit_price"])
            pdf.drawString(400, y_position, item["currency"])
            pdf.drawString(500, y_position, item["cost"])
            y_position -= 20

        # Toplamlar
        pdf.drawString(400, y_position, f"KDV (%20): {proposal_data['tax']:.2f} TL")
        y_position -= 20
        pdf.drawString(400, y_position, f"Genel Toplam: {proposal_data['tax_included']:.2f} TL")

        pdf.save()
        print(f"PDF başarıyla oluşturuldu: {self.output_path}")
