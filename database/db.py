import sqlite3
import os


def conectar():
    os.makedirs("database", exist_ok=True)  # 👈 garante pasta
    return sqlite3.connect("database/estoque.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        modelo TEXT,
        categoria TEXT,
        quantidade INTEGER,
        local_caixa TEXT,
        local_slot TEXT,
        descricao TEXT,
        status TEXT
    )
    """)
    
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