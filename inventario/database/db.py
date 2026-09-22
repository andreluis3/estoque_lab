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

    # ==========================================================
    # 1 - Tabela principal de itens
    # ==========================================================

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

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_itens_nome_modelo
        ON itens (nome, modelo)
    """)

    # ==========================================================
    # 2 - Tabela de movimentações
    # ==========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            tipo TEXT NOT NULL,
            quantidade INTEGER,
            usuario TEXT DEFAULT 'sistema',
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id)
                REFERENCES itens(id)
                ON DELETE SET NULL
        )
    """)

    # ==========================================================
    # 3 - Tabela de histórico
    # ==========================================================

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
            FOREIGN KEY (item_id)
                REFERENCES itens(id)
                ON DELETE SET NULL
        )
    """)

    # ==========================================================
    # 4 - Usuários
    # ==========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    # ==========================================================
    # 5 - Lista de compras
    # ==========================================================

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
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES itens(id)
        )
    """)

    # ==========================================================
    # 6 - Migração das FKs antigas
    # ==========================================================

    # ----------------------------------------------------------
    # Movimentações
    # ----------------------------------------------------------

    cursor.execute("""
        PRAGMA foreign_key_list(movimentacoes)
    """)

    fk_movimentacoes = cursor.fetchall()

    precisa_migrar_movimentacoes = not any(
        row[2] == "itens" and row[6].upper() == "SET NULL"
        for row in fk_movimentacoes
    )

    if precisa_migrar_movimentacoes:

        print("[DB] Migrando tabela movimentacoes...")

        cursor.execute("""
            ALTER TABLE movimentacoes
            RENAME TO movimentacoes_old
        """)

        cursor.execute("""
            CREATE TABLE movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                tipo TEXT NOT NULL,
                quantidade INTEGER,
                usuario TEXT DEFAULT 'sistema',
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id)
                    REFERENCES itens(id)
                    ON DELETE SET NULL
            )
        """)

        cursor.execute("""
            INSERT INTO movimentacoes (
                id,
                item_id,
                tipo,
                quantidade,
                usuario,
                data
            )
            SELECT
                id,
                item_id,
                tipo,
                quantidade,
                usuario,
                data
            FROM movimentacoes_old
        """)

        cursor.execute("""
            DROP TABLE movimentacoes_old
        """)

        print("[DB] movimentacoes migrada com sucesso.")

    # ----------------------------------------------------------
    # Histórico
    # ----------------------------------------------------------

    cursor.execute("""
        PRAGMA foreign_key_list(historico_alteracoes)
    """)

    fk_historico = cursor.fetchall()

    precisa_migrar_historico = not any(
        row[2] == "itens" and row[6].upper() == "SET NULL"
        for row in fk_historico
    )

    if precisa_migrar_historico:

        print("[DB] Migrando tabela historico_alteracoes...")

        cursor.execute("""
            ALTER TABLE historico_alteracoes
            RENAME TO historico_alteracoes_old
        """)

        cursor.execute("""
            CREATE TABLE historico_alteracoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                campo TEXT NOT NULL,
                valor_anterior TEXT,
                valor_novo TEXT,
                usuario TEXT DEFAULT 'sistema',
                acao TEXT NOT NULL,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id)
                    REFERENCES itens(id)
                    ON DELETE SET NULL
            )
        """)

        cursor.execute("""
            INSERT INTO historico_alteracoes (
                id,
                item_id,
                campo,
                valor_anterior,
                valor_novo,
                usuario,
                acao,
                data
            )
            SELECT
                id,
                item_id,
                campo,
                valor_anterior,
                valor_novo,
                usuario,
                acao,
                data
            FROM historico_alteracoes_old
        """)

        cursor.execute("""
            DROP TABLE historico_alteracoes_old
        """)

        print("[DB] historico_alteracoes migrada com sucesso.")


    # ==========================================================
    # 6.5 - Garantir dados históricos da movimentação
    # ==========================================================

    # Verifica se item_nome já existe
    cursor.execute("PRAGMA table_info(movimentacoes)")
    colunas_movimentacoes = [row[1] for row in cursor.fetchall()]

    if "item_nome" not in colunas_movimentacoes:
        cursor.execute("""
            ALTER TABLE movimentacoes
            ADD COLUMN item_nome TEXT
        """)

        print("[DB] Coluna item_nome adicionada em movimentacoes.")

    if "item_modelo" not in colunas_movimentacoes:
        cursor.execute("""
            ALTER TABLE movimentacoes
            ADD COLUMN item_modelo TEXT
        """)

        print("[DB] Coluna item_modelo adicionada em movimentacoes.")

    # Preenche registros antigos que ainda possuem item
    cursor.execute("""
        UPDATE movimentacoes
        SET
            item_nome = (
                SELECT nome
                FROM itens
                WHERE itens.id = movimentacoes.item_id
            ),
            item_modelo = (
                SELECT modelo
                FROM itens
                WHERE itens.id = movimentacoes.item_id
            )
        WHERE item_nome IS NULL
           OR item_modelo IS NULL
    """)

    # ==========================================================
    # 7 - Commit da criação/migração
    # ==========================================================

    conn.commit()
    conn.close()

    print("Banco atualizado com sucesso.")
    print(f"Tabelas verificadas em {__file__}")
    
    if __name__ == "__main__":
        criar_tabela()

     
                   
