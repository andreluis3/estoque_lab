import sqlite3

def conectar():
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

    conn.commit()
    conn.close() 