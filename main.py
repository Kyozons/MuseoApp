#!/usr/bin/env python3

import tkinter
import customtkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
import data

# Main App/GUI class

class Application(tk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.resizable(False,False)
        master.title('Generar Excel informe ventas')
        master.minsize(500, 300)
        master.geometry("500x300")
        self.create_widgets()
        self.shopify_filename = ""
        self.shipit_filename = ""
        self.file_types = [('CSV and Excel', "*.csv"),
                           ('CSV and Excel', "*.xlsx"),
                           ('CSV and Excel', "*.xls")]

    def create_widgets(self):

        # Boton carga archivo
        self.browse_shopify_btn = tk.CTkButton(self.master, text="Buscar Archivo" , width=12, command=self.browse_shopify)
        self.browse_shopify_btn.grid(row=0, column=0, pady=20)
        self.browse_shipit_btn = tk.CTkButton(self.master, text="Buscar Archivo", width=12, command=self.browse_shipit)
        self.browse_shipit_btn.grid(row=1, column=0, pady=20)

        # Descripcion archivo
        global file_title_shopify
        global file_title_shipit
        file_title_shopify = StringVar()
        file_title_shipit = StringVar()
        file_title_shipit.set("Seleccione Archivo Shipit")
        file_title_shopify.set("Seleccione Archivo Shopify")

        self.browse_shopify_label = tk.CTkLabel(self.master, width=50 ,textvariable=file_title_shopify)
        self.browse_shipit_label = tk.CTkLabel(self.master, width=50 ,textvariable=file_title_shipit)
        self.browse_shopify_label.grid(row=0, column=1)
        self.browse_shipit_label.grid(row=1, column=1)
        self.export_files_btn = tk.CTkButton(self.master, text="Generar", width=12, command=self.export_files)
        self.export_files_btn.grid(row=2, column=0, padx=1, pady=1)
        self.clear_route_btn = tk.CTkButton(self.master, text="Borrar texto", width=12, command=self.clear_route)
        self.clear_route_btn.grid(row=2, column=1, padx=1, pady=1)

    def clear_route(self):
        file_title_shipit.set("Seleccione Archivo Shipit")
        self.shopify_filename = ""
        file_title_shopify.set("Seleccione Archivo Shopify")
        self.shipit_filename = ""

    def browse_shopify(self):
        self.shopify_filename = filedialog.askopenfilename(filetypes=self.file_types)
        if self.shopify_filename:
            file_title_shopify.set(self.shopify_filename)
        else:
            messagebox.showerror('Archivo requerido', 'Favor seleccionar una planilla de Shopify')

    def browse_shipit(self):
        self.shipit_filename = filedialog.askopenfilename(filetypes=self.file_types)
        if self.shipit_filename:
            file_title_shipit.set(self.shipit_filename)
        else:
            messagebox.showerror('Archivo requerido', 'Favor seleccionar una planilla de Shipit')

    def export_files(self):
        if self.shopify_filename and self.shipit_filename:
            data.create_excel(self.shopify_filename, self.shipit_filename)
            messagebox.showinfo('Operación exitosa', f'Archivo guardado en {Path.cwd()}/informe_ventas.xlsx ')
        else:
            messagebox.showerror('No se encuentra archivo', 'Favor cargar archivos para continuar')


if __name__ == "__main__":
    root = tk.CTk()
    app = Application(master=root)
    app.mainloop()
