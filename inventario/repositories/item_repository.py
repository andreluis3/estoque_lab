import sqlite3

class ItemRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def salvar(self, dados: dict) -> int:
        self.cursor.execute("""
            INSERT INTO itens (nome, tipo, modelo, quantidade, caixa, localizacao, slot)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            dados["nome"], dados["tipo"], dados["modelo"], dados["quantidade"],
            dados["caixa"], dados["localizacao"], dados["slot"]
        ))
        return self.cursor.lastrowid

    def atualizar_quantidade(self, item_id: int, nova_qtd: int):
        self.cursor.execute("""
            UPDATE itens SET quantidade=?, atualizado_em=CURRENT_TIMESTAMP
            WHERE id=?
        """, (nova_qtd, item_id))

    def atualizar_item_completo(self, item_id: int, dados: dict):
        self.cursor.execute("""
            UPDATE itens
            SET nome=?, tipo=?, modelo=?, quantidade=?, caixa=?, localizacao=?, slot=?,
                atualizado_em=CURRENT_TIMESTAMP
            WHERE id=?
        """, (
            dados["nome"], dados["tipo"], dados["modelo"],
            dados["quantidade"], dados["caixa"],
            dados["localizacao"], dados["slot"], item_id
        ))

    def deletar(self, item_id: int):
        self.cursor.execute("DELETE FROM itens WHERE id=?", (item_id,))

    def buscar_por_id(self, item_id: int) -> tuple | None:
        return self.cursor.execute("""
            SELECT nome, tipo, modelo, quantidade, caixa, localizacao, slot
            FROM itens WHERE id=?
        """, (item_id,)).fetchone()

    def buscar_por_nome_e_modelo(self, nome: str, modelo: str) -> tuple | None:
        return self.cursor.execute("""
            SELECT id, quantidade FROM itens WHERE nome=? AND modelo=?
        """, (nome, modelo)).fetchone()

    def listar_todos(self) -> list[tuple]:
        return self.cursor.execute("""
            SELECT id, nome, tipo, modelo, quantidade, caixa, localizacao, slot
            FROM itens ORDER BY nome
        """).fetchall()

    def buscar_por_termo(self, texto: str, filtro: str) -> list[tuple]:
        texto_like = f"%{texto}%"
        if filtro == "nome":
            q = "SELECT * FROM itens WHERE nome LIKE ? ORDER BY id ASC LIMIT 20"
            return self.cursor.execute(q, (texto_like,)).fetchall()
        elif filtro == "modelo":
            q = "SELECT * FROM itens WHERE modelo LIKE ? ORDER BY id ASC LIMIT 20"
            return self.cursor.execute(q, (texto_like,)).fetchall()
        else:
            q = "SELECT * FROM itens WHERE nome LIKE ? OR modelo LIKE ? ORDER BY id ASC LIMIT 20"
            return self.cursor.execute(q, (texto_like, texto_like)).fetchall()

    def buscar_por_nome_like(self, nome: str) -> list[tuple]:
        return self.cursor.execute("""
            SELECT nome, tipo, modelo, caixa, localizacao, slot
            FROM itens WHERE LOWER(nome) LIKE LOWER(?) LIMIT 1
        """, (nome + "%",)).fetchall()

    def buscar_distinct_nomes(self, texto: str) -> list[tuple]:
        return self.cursor.execute("""
            SELECT DISTINCT nome FROM itens WHERE nome LIKE ? LIMIT 10
        """, (f"%{texto}%",)).fetchall()