import sqlite3
from tkinter import messagebox
import json

class Database:
    def __init__(self, db_path="db/crm.db"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Müşteriler tablosu
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            address TEXT NOT NULL,
            tax_number TEXT NOT NULL,
            phone_number TEXT NOT NULL
        )
        """)

        # Teklifler tablosu
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference TEXT NOT NULL,
            edit_date TEXT NOT NULL,
            validity_date TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            customer_address TEXT NOT NULL,
            items TEXT NOT NULL,
            tax_excluded REAL NOT NULL,
            tax REAL NOT NULL,
            tax_included REAL NOT NULL,
            total_cost REAL NOT NULL,
            profit REAL NOT NULL,
            profit_percentage REAL NOT NULL
        )
        """)
        self.connection.commit()

    def add_customer(self, company_name, address, tax_number, phone_number):
        """Yeni müşteri ekle."""
        self.cursor.execute("SELECT * FROM customers WHERE company_name = ?", (company_name,))
        result = self.cursor.fetchone()

        if result:
            messagebox.showwarning("Kayıt Hatası", f"Firma adı '{company_name}' zaten kayıtlı!")
        else:
            self.cursor.execute("""
            INSERT INTO customers (company_name, address, tax_number, phone_number)
            VALUES (?, ?, ?, ?)
            """, (company_name, address, tax_number, phone_number))
            self.connection.commit()
            messagebox.showinfo("Başarılı", "Müşteri başarıyla kaydedildi.")

    def get_customers(self):
        """Tüm müşteri bilgilerini getir."""
        self.cursor.execute("SELECT company_name, address, tax_number, phone_number FROM customers")
        customers = self.cursor.fetchall()
        return [
            {
                "company_name": row[0],
                "address": row[1],
                "tax_number": row[2],
                "phone_number": row[3]
            }
            for row in customers
        ]

    def get_customer_by_name(self, company_name):
        """Firma adına göre müşteri getir."""
        self.cursor.execute("SELECT * FROM customers WHERE company_name = ?", (company_name,))
        row = self.cursor.fetchone()
        if row:
            return {
                "company_name": row[1],
                "address": row[2],
                "tax_number": row[3],
                "phone_number": row[4]
            }
        return None

    def update_customer(self, old_name, new_name, address, tax_number, phone_number):
        """Müşteri bilgilerini güncelle."""
        self.cursor.execute("""
        UPDATE customers
        SET company_name = ?, address = ?, tax_number = ?, phone_number = ?
        WHERE company_name = ?
        """, (new_name, address, tax_number, phone_number, old_name))
        self.connection.commit()

    def delete_customer(self, company_name):
        """Müşteri sil."""
        self.cursor.execute("DELETE FROM customers WHERE company_name = ?", (company_name,))
        self.connection.commit()

    def add_proposal(self, proposal_data):
        """Yeni teklif ekle."""
        self.cursor.execute("""
        INSERT INTO proposals (
            reference, edit_date, validity_date, customer_name,
            customer_address, items, tax_excluded, tax, tax_included,
            total_cost, profit, profit_percentage
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            proposal_data["reference"],
            proposal_data["edit_date"],
            proposal_data["validity_date"],
            proposal_data["customer_name"],
            proposal_data["customer_address"],
            json.dumps(proposal_data["items"]),  # JSON formatına dönüştür
            proposal_data["tax_excluded"],
            proposal_data["tax"],
            proposal_data["tax_included"],
            proposal_data["total_cost"],
            proposal_data["profit"],
            proposal_data["profit_percentage"],
        ))
        self.connection.commit()
        messagebox.showinfo("Başarılı", "Teklif başarıyla kaydedildi.")
