import sqlite3
from datetime import datetime

class MovimentacaoRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = connection.cursor()
        
    def registrar(self, item_id: int, tipo: str, quantidade: int, usuario: str):

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Recupera os dados atuais do item
        self.cursor.execute("""
            SELECT nome, modelo
            FROM itens
            WHERE id = ?
        """, (item_id,))

        item = self.cursor.fetchone()

        if item is None:
            raise ValueError(
                f"Não foi possível registrar a movimentação. "
                f"Item ID {item_id} não encontrado."
            )

        item_nome, item_modelo = item

        # Registra a movimentação com snapshot
        self.cursor.execute("""
            INSERT INTO movimentacoes (
                item_id,
                item_nome,
                item_modelo,
                tipo,
                quantidade,
                usuario,
                data
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            item_id,
            item_nome,
            item_modelo,
            tipo,
            quantidade,
            usuario,
            ts
        ))

    def listar(self, item_id=None, tipo=None, usuario=None):
        cursor = self.conn.cursor()

        sql = """
            SELECT
                m.id,
                m.item_id,
                m.item_nome,
                m.item_modelo,
                m.tipo,
                m.quantidade,
                m.usuario,
                m.data
            FROM movimentacoes m
            WHERE 1=1
        """

        params = []

        if item_id is not None:
            sql += " AND m.item_id = ?"
            params.append(item_id)

        if tipo is not None:
            sql += " AND m.tipo = ?"
            params.append(tipo)

        if usuario is not None:
            sql += " AND m.usuario LIKE ?"
            params.append(f"%{usuario}%")

        sql += " ORDER BY m.data DESC, m.id DESC"

        cursor.execute(sql, params)

        return cursor.fetchall()