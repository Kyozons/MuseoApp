#!/usr/bin/env python3

import customtkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
import data, os

tk.set_appearance_mode("dark")

class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Generar Excel informe ventas")
        self.geometry("700x300")
        self.minsize(500, 300)
        self.create_widgets()
        self.shopify_filename = ""
        self.shipit_filename = ""
        self.csv_only = [('CSV Files', "*.csv"),]
        self.excel_only = [('Excel Files', "*.xlsx"),
                           ('Excel Files', "*.xls")]

        self.grid_columnconfigure(1, weight=3)

    def create_widgets(self):
        self.browse_shopify_btn = tk.CTkButton(self, text="Buscar Archivo", command=self.browse_shopify)
        self.browse_shopify_btn.grid(row=0, column=0, pady=20, padx=20, sticky="w")
        self.browse_shipit_btn = tk.CTkButton(self, text="Buscar Archivo", command=self.browse_shipit)
        self.browse_shipit_btn.grid(row=1, column=0, pady=20, padx=20, sticky="w")

        global file_title_shopify
        global file_title_shipit
        file_title_shopify = tk.StringVar()
        file_title_shipit = tk.StringVar()
        file_title_shopify.set("Seleccione Archivo Shopify")
        file_title_shipit.set("Seleccione Archivo Shipit")

        self.browse_shopify_label = tk.CTkLabel(self, textvariable=file_title_shopify)
        self.browse_shipit_label = tk.CTkLabel(self, textvariable=file_title_shipit)
        self.browse_shopify_label.grid(row=0, column=1, pady=20, sticky="we")
        self.browse_shipit_label.grid(row=1, column=1, pady=20, sticky="we")

        self.export_files_btn = tk.CTkButton(self, text="Generar", command=self.export_files)
        self.export_files_btn.grid(row=2, column=0, pady=20, padx=20, sticky="w")
        self.clear_route_btn = tk.CTkButton(self, text="Borrar Texto", command=self.clear_route)
        self.clear_route_btn.grid(row=2, column=1, pady=20, padx=20, sticky="e")

    def browse_shopify(self):
        self.shopify_filename = filedialog.askopenfilename(filetypes=self.csv_only)
        if self.shopify_filename:
            file_title_shopify.set(self.shopify_filename)
        else:
            messagebox.showerror('Archivo requerido', 'Favor seleccionar una planilla de Shopify')

    def browse_shipit(self):
        self.shipit_filename = filedialog.askopenfilename(filetypes=self.excel_only)
        if self.shipit_filename:
            file_title_shipit.set(self.shipit_filename)
        else:
            messagebox.showerror('Archivo requerido', 'Favor seleccionar una planilla de Shipit')

    def export_files(self):
        if self.shopify_filename and self.shipit_filename:
            data.create_excel(self.shopify_filename, self.shipit_filename)
            messagebox.showinfo('Operación exitosa', f'Archivo guardado en {os.path.abspath("Informes/informe_ventas.xlsx")}')
        else:
            messagebox.showerror('No se encuentra archivo', 'Favor cargar archivos para continuar')

    def clear_route(self):
        file_title_shipit.set("Seleccione Archivo Shipit")
        self.shopify_filename = ""
        file_title_shopify.set("Seleccione Archivo Shopify")
        self.shipit_filename = ""

if __name__ == "__main__":
    app = App()
    app.mainloop()
