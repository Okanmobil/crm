from tkinter import Frame, Label, Entry, Button, Text, Toplevel, StringVar, OptionMenu, messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import datetime


class ProposalScreen:
    def __init__(self, root, back_callback, database, pdf_creator):
        self.root = root
        self.back_callback = back_callback
        self.database = database
        self.pdf_creator = pdf_creator
        self.frame = Frame(root)
        self.frame.pack(fill="both", expand=True)

        # Üst Panel
        top_frame = Frame(self.frame)
        top_frame.pack(fill="x", pady=5)

        # Teklif Bilgileri
        Label(top_frame, text="Düzenleme Tarihi:").grid(row=0, column=0, padx=5, sticky="w")
        self.edit_date = Label(top_frame, text=datetime.datetime.now().strftime("%d/%m/%Y"))
        self.edit_date.grid(row=0, column=1, padx=5)

        Label(top_frame, text="Son Kullanma Tarihi:").grid(row=0, column=2, padx=5, sticky="w")
        self.validity_date = DateEntry(top_frame, date_pattern="dd/MM/yyyy")
        self.validity_date.grid(row=0, column=3, padx=5)

        Label(top_frame, text="Referans:").grid(row=0, column=4, padx=5, sticky="w")
        self.reference = Entry(top_frame)
        self.reference.insert(0, self.generate_reference())
        self.reference.grid(row=0, column=5, padx=5)

        # Müşteri Bilgileri
        Label(top_frame, text="Müşteri:").grid(row=1, column=0, padx=5, sticky="w")
        self.customer_name = ttk.Combobox(top_frame, values=self.fetch_customers(), state="readonly")
        self.customer_name.grid(row=1, column=1, columnspan=3, padx=5, sticky="we")
        self.customer_name.bind("<<ComboboxSelected>>", self.populate_customer_address)

        Label(top_frame, text="Adres:").grid(row=2, column=0, padx=5, sticky="w")
        self.customer_address = Text(top_frame, height=3, width=50, state="disabled")
        self.customer_address.grid(row=2, column=1, columnspan=5, padx=5, sticky="we")

        # Açıklama Alanı
        Label(top_frame, text="Açıklama:").grid(row=3, column=0, padx=5, sticky="w")
        self.description = Text(top_frame, height=3, width=50)
        self.description.grid(row=3, column=1, columnspan=5, padx=5, sticky="we")

        # Hizmet Kalemleri
        middle_frame = Frame(self.frame)
        middle_frame.pack(fill="both", expand=True, pady=10)

        Label(middle_frame, text="Hizmet Adı").grid(row=0, column=0, padx=5, sticky="w")
        Label(middle_frame, text="Miktar").grid(row=0, column=1, padx=5, sticky="w")
        Label(middle_frame, text="Birim Fiyat").grid(row=0, column=2, padx=5, sticky="w")
        Label(middle_frame, text="Maliyet").grid(row=0, column=3, padx=5, sticky="w")
        Label(middle_frame, text="Para Birimi").grid(row=0, column=4, padx=5, sticky="w")
        Label(middle_frame, text="Toplam").grid(row=0, column=5, padx=5, sticky="w")

        self.rows = []
        self.middle_frame = middle_frame
        self.add_row()

        Button(middle_frame, text="Satır Ekle", command=self.add_row).grid(row=1, column=6, padx=5)
        Button(middle_frame, text="Satır Sil", command=self.delete_row).grid(row=2, column=6, padx=5)

        # Alt Panel
        bottom_frame = Frame(self.frame)
        bottom_frame.pack(fill="x", pady=5)

        Label(bottom_frame, text="KDV Hariç Satış:").grid(row=0, column=3, padx=5, sticky="e")
        self.tax_excluded = Label(bottom_frame, text="0")
        self.tax_excluded.grid(row=0, column=4, padx=5, sticky="w")

        Label(bottom_frame, text="KDV Dahil Satış:").grid(row=1, column=3, padx=5, sticky="e")
        self.tax_included = Label(bottom_frame, text="0")
        self.tax_included.grid(row=1, column=4, padx=5, sticky="w")

        Label(bottom_frame, text="Toplam Maliyet:").grid(row=2, column=3, padx=5, sticky="e")
        self.total_cost = Label(bottom_frame, text="0")
        self.total_cost.grid(row=2, column=4, padx=5, sticky="w")

        Label(bottom_frame, text="Edinilecek Kâr:").grid(row=3, column=3, padx=5, sticky="e")
        self.total_profit = Label(bottom_frame, text="0")
        self.total_profit.grid(row=3, column=4, padx=5, sticky="w")

        Button(bottom_frame, text="Kaydet", command=self.ask_preview).grid(row=4, column=4, pady=10, sticky="e")
        Button(bottom_frame, text="Ana Menüye Dön", command=self.back_to_menu).grid(row=4, column=0, pady=10, sticky="w")

    def generate_reference(self):
        """Teklif için otomatik referans numarası oluşturur."""
        return f"REF-{int(datetime.datetime.now().timestamp())}"

    def fetch_customers(self):
        """Veritabanından müşteri bilgilerini çeker."""
        try:
            customers = self.database.get_customers()
            return [customer["company_name"] for customer in customers]
        except Exception as e:
            print(f"Müşteri bilgileri alınırken hata oluştu: {e}")
            return []

    def populate_customer_address(self, event):
        """Seçilen müşterinin adresini doldurur."""
        selected_customer = self.customer_name.get()
        customer_info = self.database.get_customer_by_name(selected_customer)
        if customer_info:
            self.customer_address.config(state="normal")
            self.customer_address.delete("1.0", "end")
            self.customer_address.insert("end", customer_info["address"])
            self.customer_address.config(state="disabled")

    def add_row(self):
        """Hizmet için yeni bir satır ekler."""
        row = {
            "service": Entry(self.middle_frame),
            "quantity": Entry(self.middle_frame),
            "unit_price": Entry(self.middle_frame),
            "cost": Entry(self.middle_frame),
            "currency": StringVar(value=""),
            "total": Label(self.middle_frame, text="0"),
        }
        row["service"].grid(row=len(self.rows) + 1, column=0, padx=5)
        row["quantity"].grid(row=len(self.rows) + 1, column=1, padx=5)
        row["quantity"].bind("<FocusOut>", lambda e: self.calculate_totals())
        row["unit_price"].grid(row=len(self.rows) + 1, column=2, padx=5)
        row["unit_price"].bind("<FocusOut>", lambda e: self.calculate_totals())
        row["cost"].grid(row=len(self.rows) + 1, column=3, padx=5)
        row["cost"].bind("<FocusOut>", lambda e: self.calculate_totals())
        OptionMenu(
            self.middle_frame,
            row["currency"],
            "",
            "TL",
            "$",
            "€",
            command=lambda _: self.calculate_totals()
        ).grid(row=len(self.rows) + 1, column=4, padx=5)
        row["total"].grid(row=len(self.rows) + 1, column=5, padx=5)
        self.rows.append(row)

    def calculate_totals(self):
        """Dinamik toplam hesaplamaları yapar."""
        total_sales = 0
        total_cost = 0

        for row in self.rows:
            try:
                quantity = float(row["quantity"].get()) if row["quantity"].get() else 0
                unit_price = float(row["unit_price"].get()) if row["unit_price"].get() else 0
                cost = float(row["cost"].get()) if row["cost"].get() else 0

                row_total = quantity * unit_price
                row_cost = quantity * cost

                total_sales += row_total
                total_cost += row_cost

                currency = row["currency"].get()
                row["total"].config(text=f"{row_total:.2f} {currency}")
            except ValueError:
                row["total"].config(text="0")

        profit = total_sales - total_cost
        vat = total_sales * 0.20
        total_with_vat = total_sales + vat

        self.tax_excluded.config(text=f"{total_sales:.2f}")
        self.tax_included.config(text=f"{total_with_vat:.2f}")
        self.total_cost.config(text=f"{total_cost:.2f}")
        self.total_profit.config(text=f"{profit:.2f}")

    def delete_row(self):
        """Son eklenen satırı siler."""
        if self.rows:
            row = self.rows.pop()
            for widget in row.values():
                widget.destroy()

    def ask_preview(self):
        """Kaydetmeden önce önizleme yapmak ister."""
        if messagebox.askyesno("Önizleme", "Önizleme yapmak ister misiniz?"):
            self.show_preview()

    def show_preview(self):
        """PDF önizlemesi yapar ve gerekli işlemleri çalıştırır."""
        try:
            preview_window = Toplevel(self.root)
            preview_window.title("Teklif Önizleme")
            preview_window.geometry("600x400")
            Label(preview_window, text="Teklif Önizleme Ekranı", font=("Arial", 20)).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Hata", f"Önizleme ekranı yüklenirken hata oluştu: {e}")

    def back_to_menu(self):
        """Ana menüye döner."""
        self.frame.pack_forget()
        self.back_callback()
