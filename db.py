#!/usr/bin/env python3

import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS inventario (id INTEGER PRIMARY KEY, descripcion text, codigo_barras text UNIQUE, cantidad text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM inventario")
        rows = self.cur.fetchall()
        return rows

    def insert(self, descripcion, codigo_barras, cantidad):
        self.cur.execute("INSERT into inventario VALUES (NULL, ?, ?, ?)", (descripcion, codigo_barras, cantidad))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM inventario WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, descripcion, codigo_barras, cantidad):
        self.cur.execute("UPDATE inventario SET descripcion = ?, codigo_barras = ?, cantidad = ? WHERE id = ?", (descripcion, codigo_barras, cantidad, id))
        self.conn.commit()

    def search(self, codigo_barras):
        self.cur.execute("SELECT * FROM inventario WHERE codigo_barras = ?", (codigo_barras,))
        data = self.cur.fetchall()
        return data

    def __del__(self):
        self.conn.close()
