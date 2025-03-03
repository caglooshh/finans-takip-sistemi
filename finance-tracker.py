#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 19:51:04 2025

@author: camkardesler
"""
import sqlite3
import datetime


def create_table():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    amount REAL,
                    description TEXT,
                    date TEXT)''')
    conn.commit()
    conn.close()

def add_transaction(transaction_type, amount, description):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO transactions (type, amount, description, date) VALUES (?, ?, ?, ?)",
              (transaction_type, amount, description, date))
    conn.commit()
    conn.close()

def list_transactions():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    conn.close()
    return transactions

def show_summary():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    summary = c.fetchall()
    conn.close()
    return summary

def main():
    create_table() 
    while True:
        print("\n==== Finans Takip Sistemi ====")
        print("1. Gelir Ekle")
        print("2. Gider Ekle")
        print("3. Tüm İşlemleri Görüntüle")
        print("4. Özet")
        print("5. Çıkış")
        choice = input("Seçiminizi yapınız: ")

        if choice == '1':
            try:
                amount = float(input("Gelir miktarı: "))
            except ValueError:
                print("Geçerli bir sayı giriniz!")
                continue
            description = input("Açıklama: ")
            add_transaction("Gelir", amount, description)
            print("Gelir eklendi!")
        elif choice == '2':
            try:
                amount = float(input("Gider miktarı: "))
            except ValueError:
                print("Geçerli bir sayı giriniz!")
                continue
            description = input("Açıklama: ")
            add_transaction("Gider", amount, description)
            print("Gider eklendi!")
        elif choice == '3':
            transactions = list_transactions()
            if transactions:
                print("\nTüm İşlemler:")
                for t in transactions:
                    print(f"ID: {t[0]} | Tip: {t[1]} | Miktar: {t[2]} | Açıklama: {t[3]} | Tarih: {t[4]}")
            else:
                print("Henüz kayıt yok.")
        elif choice == '4':
            summary = show_summary()
            if summary:
                for s in summary:
                    print(f"{s[0]} Toplamı: {s[1]}")
            else:
                print("Henüz özet bilgisi bulunamadı.")
        elif choice == '5':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin!")

if __name__ == "__main__":
    main()

