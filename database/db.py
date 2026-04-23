import sqlite3
import os

def conectar_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "..", "database/estoque.db")
    conn = sqlite3.connect(db_path)
    return conn

def criar_tabela():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL,
        modelo TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        caixa TEXT NOT NULL,
        localizacao TEXT NOT NULL,
        slot TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        tipo TEXT,
        quantidade INTEGER,
        usuario TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

  