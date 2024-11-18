from tkinter import Tk, Frame, Button, Label
from screens.customer_screen import CustomerScreen
from screens.proposal_screen import ProposalScreen
from db.database import Database
from pdf.pdf_creator import PDFCreator  # PDF oluşturucu sınıfını içe aktarın

class CRMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRM Yazılımı")
        self.root.geometry("1200x800")  # Daha geniş bir ekran düzeni

        # Veritabanı nesnesi
        try:
            self.database = Database()
            print("Veritabanı başarıyla bağlandı.")
        except Exception as e:
            print(f"Veritabanı hatası: {e}")

        # PDFCreator nesnesi (PDF'ler için bir çıkış yolu belirtin)
        try:
            self.pdf_creator = PDFCreator(output_path="output/proposal.pdf", logo_path="logo.png")
        except Exception as e:
            print(f"PDF oluşturucu hatası: {e}")

        # Sol tarafta menü çerçevesi
        self.menu_frame = Frame(root, width=200, bg="#f0f0f0")
        self.menu_frame.pack(side="left", fill="y")

        # Sağ tarafta içerik çerçevesi
        self.content_frame = Frame(root, bg="#ffffff")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Menü butonları
        Button(self.menu_frame, text="Müşteri Yönetimi", command=self.show_customer_screen).pack(pady=10, fill="x")
        Button(self.menu_frame, text="Teklif Oluştur", command=self.show_proposal_screen).pack(pady=10, fill="x")
        Button(self.menu_frame, text="Teklif Listesi", command=self.show_proposal_list_screen).pack(pady=10, fill="x")
        Button(self.menu_frame, text="Kâr/Zarar Analizi", command=self.show_profit_analysis_screen).pack(pady=10, fill="x")
        Button(self.menu_frame, text="Ayarlar", command=self.show_settings_screen).pack(pady=10, fill="x")

        # Varsayılan içerik
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Varsayılan içerik ekranı."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Hoş Geldiniz!", font=("Arial", 20), bg="#ffffff").pack(expand=True)

    def show_customer_screen(self):
        """Müşteri yönetimi ekranını gösterir."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        try:
            CustomerScreen(self.content_frame, self.show_welcome_screen, self.database)
        except Exception as e:
            self.show_error_screen(f"Müşteri Yönetimi ekranı yüklenirken hata oluştu: {e}")

    def show_proposal_screen(self):
        """Teklif oluşturma ekranını gösterir."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        try:
            ProposalScreen(self.content_frame, self.show_welcome_screen, self.database, self.pdf_creator)
        except Exception as e:
            self.show_error_screen(f"Teklif Oluşturma ekranı yüklenirken hata oluştu: {e}")

    def show_proposal_list_screen(self):
        """Teklif listesi ekranını gösterir (henüz uygulanmamış)."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Teklif Listesi Henüz Eklenmedi.", font=("Arial", 16), bg="#ffffff").pack(expand=True)

    def show_profit_analysis_screen(self):
        """Kâr/Zarar Analizi ekranını gösterir (henüz uygulanmamış)."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Kâr/Zarar Analizi Henüz Eklenmedi.", font=("Arial", 16), bg="#ffffff").pack(expand=True)

    def show_settings_screen(self):
        """Ayarlar ekranını gösterir (henüz uygulanmamış)."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Ayarlar Henüz Eklenmedi.", font=("Arial", 16), bg="#ffffff").pack(expand=True)

    def show_error_screen(self, error_message):
        """Hata ekranı gösterir."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Hata Oluştu!", font=("Arial", 20), fg="red", bg="#ffffff").pack(pady=20)
        Label(self.content_frame, text=error_message, font=("Arial", 12), fg="red", bg="#ffffff").pack(pady=20)


if __name__ == "__main__":
    try:
        root = Tk()
        app = CRMApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Program başlatılamadı: {e}")
