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
        localizacao TEXT NOT NULL
    )
    """)

    conn.commit()
  
    
    # database/db.py
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            usuario TEXT,
            acao TEXT,          -- 'entrada' ou 'saida'
            item_id INTEGER,
            quantidade INTEGER,
            detalhes TEXT,
            FOREIGN KEY (item_id) REFERENCES itens(id)
        )
    """)

    conn.commit()
    conn.close() 