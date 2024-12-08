import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import PyPDF2

# PDF létrehozása több oldallal
def create_multi_page_pdf(szoveg_list, fajl_nev):
    c = canvas.Canvas(fajl_nev, pagesize=letter)
    szelesseg, magassag = letter
    for oldalszam, szoveg in enumerate(szoveg_list):
        y_pozicio = magassag - 50  # Kezdő pozíció
        c.drawString(100, y_pozicio, f"Oldal {oldalszam + 1}")
        y_pozicio -= 20
        for sor in szoveg.split("\n"):
            if y_pozicio < 50:  # Ha elérjük az oldal alját
                c.showPage()  # Új oldal
                c.drawString(100, magassag - 50, f"Oldal {oldalszam + 1}")
                y_pozicio = magassag - 50
            c.drawString(100, y_pozicio, sor)
            y_pozicio -= 15
        c.showPage()  # Minden oldal végén új oldalt kezdünk
    c.save()
    messagebox.showinfo("PDF mentés", f"A PDF fájl sikeresen mentve: {fajl_nev}")

# PDF fájl megnyitása és olvasása
def open_pdf():
    fajl_utvonal = filedialog.askopenfilename(filetypes=[("PDF fájlok", "*.pdf")])
    if fajl_utvonal:
        try:
            with open(fajl_utvonal, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                szoveg = ""
                for oldal in reader.pages:
                    szoveg += oldal.extract_text()
                szoveg_mezo.delete(1.0, tk.END)
                szoveg_mezo.insert(tk.END, szoveg)
        except Exception as e:
            messagebox.showerror("Hiba", f"Nem sikerült megnyitni a fájlt: {e}")

# Szöveg mentése PDF fájlba
def save_pdf():
    szoveg = szoveg_mezo.get(1.0, tk.END).strip()
    if szoveg:
        fajl_utvonal = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF fájlok", "*.pdf")])
        if fajl_utvonal:
            create_multi_page_pdf([szoveg], fajl_utvonal)  # Többoldalas PDF létrehozása
    else:
        messagebox.showwarning("Figyelmeztetés", "A szöveg nem lehet üres!")

# Kép hozzáadása PDF-hez
def add_image_to_pdf():
    szoveg = szoveg_mezo.get(1.0, tk.END).strip()
    if szoveg:
        kep_fajl = filedialog.askopenfilename(filetypes=[("Képek", "*.png;*.jpg;*.jpeg")])
        if kep_fajl:
            fajl_utvonal = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF fájlok", "*.pdf")])
            if fajl_utvonal:
                c = canvas.Canvas(fajl_utvonal, pagesize=letter)
                c.drawString(100, 750, szoveg)  # Szöveg hozzáadása
                c.drawImage(kep_fajl, 100, 500, width=200, height=200)  # Kép hozzáadása
                c.save()
                messagebox.showinfo("PDF mentés", f"A PDF fájl sikeresen mentve: {fajl_utvonal}")
    else:
        messagebox.showwarning("Figyelmeztetés", "Nincs szöveg a PDF-ben!")

# GUI beállítások
root = tk.Tk()
root.title("PDF Készítő és Szerkesztő")
root.geometry("800x600")  # A méret növelése
root.config(bg="#f4f4f4")  # Világos háttérszín

# Cím szöveg
title_label = tk.Label(root, text="PDF Készítő és Szerkesztő", font=("Helvetica", 18, "bold"), bg="#f4f4f4", fg="#333")
title_label.pack(pady=20)

# Szöveges mező a PDF szerkesztéséhez
szoveg_mezo = tk.Text(root, wrap=tk.WORD, height=15, width=70, font=("Arial", 12), bd=2, relief="sunken")
szoveg_mezo.pack(pady=10)

# Menü létrehozása
menu = tk.Menu(root)
root.config(menu=menu)

# Fájl menü
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Fájl", menu=file_menu)
file_menu.add_command(label="PDF megnyitása", command=open_pdf)
file_menu.add_command(label="PDF mentése", command=save_pdf)
file_menu.add_command(label="Kép hozzáadása PDF-hez", command=add_image_to_pdf)
file_menu.add_separator()
file_menu.add_command(label="Kilépés", command=root.quit)

# Gombok stílusa
button_font = ("Arial", 12, "bold")
button_bg = "#4CAF50"  # Zöld gomb
button_fg = "white"

# Mentés gomb
save_button = tk.Button(root, text="Mentés PDF-be", command=save_pdf, font=button_font, bg=button_bg, fg=button_fg, relief="flat", padx=20, pady=10)
save_button.pack(pady=20)

# Megnyitás gomb
open_button = tk.Button(root, text="PDF megnyitása", command=open_pdf, font=button_font, bg="#008CBA", fg="white", relief="flat", padx=20, pady=10)
open_button.pack(pady=10)

# Kép hozzáadása gomb
image_button = tk.Button(root, text="Kép hozzáadása PDF-hez", command=add_image_to_pdf, font=button_font, bg="#FF9800", fg="white", relief="flat", padx=20, pady=10)
image_button.pack(pady=10)

root.mainloop()
