import sqlite3

class HistoricoRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def registrar(self, item_id: int, campo: str, anterior: str | None, novo: str | None, usuario: str, acao: str):
        self.cursor.execute("""
            INSERT INTO historico_alteracoes (item_id, campo, valor_anterior, valor_novo, usuario, acao)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (item_id, campo, anterior, novo, usuario, acao))

    def listar(self, query_complemento: str, params: list) -> list[tuple]:
        query = """
            SELECT h.id, h.item_id, i.nome, i.modelo, h.campo, h.valor_anterior, h.valor_novo, h.usuario, h.acao, h.data
            FROM historico_alteracoes h
            LEFT JOIN itens i ON i.id = h.item_id
            WHERE 1=1
        """ + query_complemento
        return self.cursor.execute(query, params).fetchall()