from tkinter import Frame, Label, Entry, Button, Listbox, messagebox
from tkinter import Toplevel


class CustomerScreen:
    def __init__(self, root, back_callback, database):
        self.root = root
        self.back_callback = back_callback
        self.database = database
        self.frame = Frame(root)
        self.frame.pack(fill="both", expand=True)

        Label(self.frame, text="Müşteri Yönetimi", font=("Arial", 16)).pack(pady=10)

        # Müşteri ekleme formu
        Label(self.frame, text="Firma Adı:").pack()
        self.company_name = Entry(self.frame)
        self.company_name.pack()

        Label(self.frame, text="Adres:").pack()
        self.address = Entry(self.frame)
        self.address.pack()

        Label(self.frame, text="Vergi Numarası:").pack()
        self.tax_number = Entry(self.frame)
        self.tax_number.pack()

        Label(self.frame, text="Telefon Numarası:").pack()
        self.phone_number = Entry(self.frame)
        self.phone_number.pack()

        Button(self.frame, text="Kaydet", command=self.save_customer).pack(pady=10)

        # Müşteri listesi
        self.customer_list = Listbox(self.frame)
        self.customer_list.pack(pady=10, fill="both", expand=True)
        self.customer_list.bind("<Double-1>", self.edit_customer)

        # Geri dön
        Button(self.frame, text="Ana Menüye Dön", command=self.back_to_menu).pack(pady=10)

        self.load_customers()

    def load_customers(self):
        """Müşteri listesini yükle."""
        self.customer_list.delete(0, "end")
        customers = self.database.get_customers()
        for customer in customers:
            self.customer_list.insert("end", f"{customer['company_name']} - {customer['phone_number']}")

    def save_customer(self):
        """Yeni müşteri ekle."""
        company = self.company_name.get().strip()
        address = self.address.get().strip()
        tax_number = self.tax_number.get().strip()
        phone_number = self.phone_number.get().strip()

        if company and address and tax_number and phone_number:
            self.database.add_customer(company, address, tax_number, phone_number)
            self.load_customers()
            self.clear_form()
        else:
            messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")

    def clear_form(self):
        """Formu temizle."""
        self.company_name.delete(0, "end")
        self.address.delete(0, "end")
        self.tax_number.delete(0, "end")
        self.phone_number.delete(0, "end")

    def edit_customer(self, event):
        """Seçili müşteriyi düzenle veya sil."""
        selected = self.customer_list.curselection()
        if not selected:
            return

        customer_name = self.customer_list.get(selected).split(" - ")[0]
        customer_data = self.database.get_customer_by_name(customer_name)

        edit_window = Toplevel(self.root)
        edit_window.title("Müşteri Düzenle")

        Label(edit_window, text="Firma Adı:").grid(row=0, column=0, pady=5, padx=5)
        company_name = Entry(edit_window)
        company_name.insert(0, customer_data["company_name"])
        company_name.grid(row=0, column=1, pady=5, padx=5)

        Label(edit_window, text="Adres:").grid(row=1, column=0, pady=5, padx=5)
        address = Entry(edit_window)
        address.insert(0, customer_data["address"])
        address.grid(row=1, column=1, pady=5, padx=5)

        Label(edit_window, text="Vergi Numarası:").grid(row=2, column=0, pady=5, padx=5)
        tax_number = Entry(edit_window)
        tax_number.insert(0, customer_data["tax_number"])
        tax_number.grid(row=2, column=1, pady=5, padx=5)

        Label(edit_window, text="Telefon Numarası:").grid(row=3, column=0, pady=5, padx=5)
        phone_number = Entry(edit_window)
        phone_number.insert(0, customer_data["phone_number"])
        phone_number.grid(row=3, column=1, pady=5, padx=5)

        Button(edit_window, text="Kaydet", command=lambda: self.update_customer(
            customer_data["company_name"],
            company_name.get(),
            address.get(),
            tax_number.get(),
            phone_number.get(),
            edit_window
        )).grid(row=4, column=0, pady=10, padx=5)

        Button(edit_window, text="Sil", command=lambda: self.delete_customer(
            customer_data["company_name"],
            edit_window
        )).grid(row=4, column=1, pady=10, padx=5)

    def update_customer(self, old_name, new_name, address, tax_number, phone_number, window):
        """Müşteri bilgilerini güncelle."""
        self.database.update_customer(old_name, new_name, address, tax_number, phone_number)
        self.load_customers()
        window.destroy()

    def delete_customer(self, company_name, window):
        """Seçili müşteriyi sil."""
        self.database.delete_customer(company_name)
        self.load_customers()
        window.destroy()

    def back_to_menu(self):
        """Ana menüye dön."""
        self.frame.pack_forget()
        self.back_callback()
