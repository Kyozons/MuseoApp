#!/usr/bin/env python3

import customtkinter as tk

class AddItemFrame(tk.CTkFrame):
    def __init__(self, *args, header_name="Añadir Item", btn_ok_command, btn_cancel_command, ok_btn_name="Añadir", **kwargs):
        super().__init__(*args, **kwargs)

        self.header_name = header_name
        self.width = 600
        self.height = 500

        self.grid_rowconfigure(0, weight=1)
        self.header = tk.CTkLabel(self, text=self.header_name)
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="new")

        self.desc_label = tk.CTkLabel(self, text="Descripción")
        self.desc_label.grid(row=1, column=0, padx=10, pady=10)
        self.desc_entry = tk.CTkEntry(self)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=10)
        self.barcode_label = tk.CTkLabel(self, text="Código de barras")
        self.barcode_label.grid(row=2, column=0, padx=10, pady=10)
        self.barcode_entry = tk.CTkEntry(self)
        self.barcode_entry.grid(row=2, column=1, padx=10, pady=10)
        self.quantity_label = tk.CTkLabel(self, text="Cantidad")
        self.quantity_label.grid(row=3, column=0, padx=10, pady=10)
        self.quantity_entry = tk.CTkEntry(self)
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=10)

        self.ok_btn = tk.CTkButton(self, text=ok_btn_name, command=btn_ok_command)
        self.ok_btn.grid(row=5, column=0, padx=10, pady=10)
        self.cancel_btn = tk.CTkButton(self, text="Cancelar", command=btn_cancel_command)
        self.cancel_btn.grid(row=5, column=1, padx=10, pady=10)
