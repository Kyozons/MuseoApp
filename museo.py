#!/usr/bin/env python3

import customtkinter as tk
from inventory import Inventory
from frames import AddItemFrame
from GenerarInforme import App
from tkinter import *

class MainApp(tk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Museo Precolombino")
        self.geometry("600x550")
        self.minsize(600, 550)
        self.create_widgets()

    def create_widgets(self):
        self.inventario = Inventory(self)
        self.informe = App()
        self.segmented_button = tk.CTkOptionMenu(self, values=["Inventario", "Generar Informe"], command=self.switch_app)
        self.segmented_button.set("Inventario")
        self.segmented_button.pack()
        self.inventario.pack(fill=BOTH, expand=True)

    def switch_app(self, value):
        if value == "Inventario":
            self.informe.pack_forget()
            self.inventario.pack(fill=BOTH, expand=True)
        elif value == "Generar Informe":
            self.inventario.pack_forget()
            self.informe.pack()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
