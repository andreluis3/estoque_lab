import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "estoque.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def conectar_db():
    print(f"📦 DB USADO PELO SISTEMA: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    
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
        quantidade INTEGER NOT NULL DEFAULT 0,
        caixa TEXT NOT NULL,
        localizacao TEXT NOT NULL DEFAULT 'Não informado',
        slot TEXT DEFAULT '',
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Índice para buscas rápidas por nome+modelo (chave de identidade do item)
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_itens_nome_modelo
    ON itens (nome, modelo)
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        tipo TEXT NOT NULL,
        quantidade INTEGER,
        usuario TEXT DEFAULT 'sistema',
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_id) REFERENCES itens(id)
    )
    """)

    # Tabela de auditoria — registra QUALQUER mudança de campo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_alteracoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        campo TEXT NOT NULL,
        valor_anterior TEXT,
        valor_novo TEXT,
        usuario TEXT DEFAULT 'sistema',
        acao TEXT NOT NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_id) REFERENCES itens(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    
      """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lista_compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        nome TEXT NOT NULL,
        modelo TEXT,
        quantidade_atual INTEGER DEFAULT 1,
        status TEXT DEFAULT 'PENDENTE',
        observacao TEXT,
        usuario TEXT,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    if __name__ == "__main__":
        criar_tabela()
    print (f"tabela criada {__file__} com sucesso.")
    print("Banco atualizado com sucesso.")
     
                   
    conn.commit()
    conn.close()