import sqlite3
from datetime import datetime
class HistoricoRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def registrar(self, item_id: int, campo: str, anterior: str | None, novo: str | None, usuario: str, acao: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT INTO historico_alteracoes
                (item_id, campo, valor_anterior, valor_novo, usuario, acao, data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (item_id, campo, anterior, novo, usuario, acao, ts))

    def listar(self, item_id=None, usuario=None):
        cursor = self.conn.cursor()

        sql = """
            SELECT
                h.id,
                h.item_id,
                i.nome,
                i.modelo,
                h.campo,
                h.valor_anterior,
                h.valor_novo,
                h.usuario,
                h.acao,
                h.data
            FROM historico_alteracoes h
            LEFT JOIN itens i ON i.id = h.item_id
            WHERE 1=1
        """

        params = []

        if item_id is not None:
            sql += " AND h.item_id = ?"
            params.append(item_id)

        if usuario is not None:
            sql += " AND h.usuario LIKE ?"
            params.append(f"%{usuario}%")

        sql += " ORDER BY h.data DESC"

        cursor.execute(sql, params)
        return cursor.fetchall()