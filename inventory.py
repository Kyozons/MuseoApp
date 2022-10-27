#!/usr/bin/env python3

import customtkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db import Database
from frames import AddItemFrame

db = Database('Inventario.db')

tk.set_appearance_mode("dark")

class Inventory(tk.CTkFrame):
    def __init__(self, *args, width: int =600, height: int =400, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        # self.title("Inventario")
        # self.geometry("600x400")
        # self.minsize(600, 400)
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()
        self.frame_active = 1
        self.add_item_frame = ""
        self.modify_item_frame = ""
        self.selected_item = ""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Vertical.TScrollbar", bordercolor="#1a1b1c", background="#2f3030", arrowcolor="white")
        self.populate_list()
        print(self.modify_item_frame, self.add_item_frame)

    def populate_list(self):
        self.text_area.delete(0, END)
        for row in db.fetch():
            self.text_area.insert(END, row)

    def create_widgets(self):

        self.scrollbar = tk.CTkScrollbar(self, orientation='vertical')
        self.text_area = Listbox(self, bg="#2f3030", borderwidth=0, fg="white", highlightcolor="#1a1b1c", highlightbackground="#1a1b1c", yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.text_area.yview)
        self.text_area.bind('<<ListboxSelect>>', self.select_item)
        self.scrollbar.grid(row=1, column=1)
        self.text_area.grid(row=1, column=0, rowspan=4, padx=20, pady=(0,20), sticky="snew")

        self.main_entry = tk.CTkEntry(self, placeholder_text="Escriba aquí...")
        self.main_entry.grid(row=5, column=0, padx=10, pady=10, sticky="sew")
        self.main_entry.bind('<Return>', self.search)
        self.main_entry.focus()

        self.title_list_label = tk.CTkLabel(self, text="ID  |  Descripción  |  CódigoBarra  |  Cantidad")
        self.title_list_label.grid(row=0, column=0, pady=(20,0), sticky="sew")

        self.populate_button = tk.CTkButton(self, text="Cargar Inventario", command=self.populate_list)
        self.populate_button.grid(row=2, column=2, padx=10, pady=10, sticky="new")
        self.add_button = tk.CTkButton(self, text="Agregar Item", command=self.add_item)
        self.add_button.grid(row=3, column=2, padx=10, pady=10, sticky="new")
        self.clear_button = tk.CTkButton(self, text="Borrar Pantalla", command=self.clear_data)
        self.clear_button.grid(row=4, column=2, padx=10, pady=10, sticky="new")
        self.modify_button = tk.CTkButton(self, text="Modificar Item", command=self.modify_item)
        self.modify_button.grid(row=5, column=2, padx=10, pady=10, sticky="new")
        self.search_button = tk.CTkButton(self, text="Buscar", command=self.btn_search)
        self.search_button.grid(row=6, column=0, padx=10, pady=10, sticky="ws")
        self.delete_button = tk.CTkButton(self, text="Eliminar Item", command=self.delete_item)
        self.delete_button.grid(row=6, column=2, padx=10, pady=10, sticky="new")

    def select_item(self, event):
        try:
            index = self.text_area.curselection()[0]
            self.selected_item = self.text_area.get(index)
        except IndexError:
            pass

    def add_item(self):
        self.add_item_frame = AddItemFrame(self, btn_ok_command=self.insert_item, btn_cancel_command=self.switch_frames)
        self.add_item_frame.grid(row=0, column=0)
        self.switch_frames()


    def modify_item(self):
        if self.selected_item:
            self.modify_item_frame = AddItemFrame(self, header_name="Modificar Item", ok_btn_name="Modificar", btn_ok_command=self.update_item, btn_cancel_command=self.switch_frames)
            self.modify_item_frame.grid(row=0, column=0)
            self.modify_item_frame.desc_entry.insert(END, self.selected_item[1])
            self.modify_item_frame.barcode_entry.insert(END, self.selected_item[2])
            self.modify_item_frame.quantity_entry.insert(END, self.selected_item[3])
            self.switch_frames()
        else:
            messagebox.showinfo('Ningun elemento seleccionado', 'Seleccione elemento para modificar')

    def update_item(self):
        db.update(self.selected_item[0], self.modify_item_frame.desc_entry.get(), self.modify_item_frame.barcode_entry.get(), self.modify_item_frame.quantity_entry.get())
        self.switch_frames()



    def insert_item(self):
        db.insert(self.add_item_frame.desc_entry.get(), self.add_item_frame.barcode_entry.get(), self.add_item_frame.quantity_entry.get())
        self.switch_frames()

    def switch_frames(self):
        if self.frame_active == 1:
            self.frame_active = 2
            self.text_area.grid_remove()
            self.add_button.grid_remove()
            self.populate_button.grid_remove()
            self.clear_button.grid_remove()
            self.modify_button.grid_remove()
            self.scrollbar.grid_remove()
            self.main_entry.grid_remove()
            self.search_button.grid_remove()
            self.delete_button.grid_remove()
            if self.add_item_frame or self.modify_item_frame:
                if self.add_item_frame:
                    self.add_item_frame.grid()
                elif self.modify_item_frame:
                    self.modify_item_frame.grid()
            self.populate_list()

        elif self.frame_active == 2:
            self.frame_active = 1
            self.text_area.grid()
            self.add_button.grid()
            self.populate_button.grid()
            self.clear_button.grid()
            self.modify_button.grid()
            self.scrollbar.grid()
            self.main_entry.grid()
            self.search_button.grid()
            self.delete_button.grid()
            if self.add_item_frame or self.modify_item_frame:
                if self.add_item_frame:
                    self.add_item_frame.grid_remove()
                    self.add_item_frame = ""
                elif self.modify_item_frame:
                    self.modify_item_frame.grid_remove()
                    self.modify_item_frame = ""
            self.populate_list()

    def clear_data(self):
        self.text_area.delete(0, END)

    def search(self, event):
        res = db.search(self.main_entry.get())

        if not res:
            messagebox.showerror('No encontrado', 'Producto no encontrado en base de datos')

        if self.main_entry.get() and res:
            self.main_entry.delete(0, tk.END)
            self.text_area.delete(0, tk.END)
            self.text_area.insert(END, res[0])
            self.text_area.focus()
            self.main_entry.focus()
        else:
            pass

    def btn_search(self):
        res = db.search(self.main_entry.get())

        if not res:
            messagebox.showerror('No encontrado', 'Producto no encontrado en base de datos')

        if self.main_entry.get() and res:
            self.text_area.insert(END, res)
            self.main_entry.delete(0, tk.END)
            self.text_area.focus()
            self.main_entry.focus()

    def delete_item(self):
        if self.selected_item:
            question_delete = messagebox.askyesno(message=f"¿Eliminar item {self.selected_item[1]}?", title="Eliminar")
            if question_delete:
                db.remove(self.selected_item[0])
                messagebox.showinfo('Completado', 'item eliminado correctamente')
                self.populate_list()
            else:
                messagebox.showinfo('Sin cambios', 'No se ha eliminado item')
        else:
            messagebox.showinfo('Nada seleccionado', 'Seleccione item para eliminar')



if __name__ == "__main__":
    app = Inventory()
    app.mainloop()
