import sqlite3

class MovimentacaoRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def registrar(self, item_id: int, tipo: str, quantidade: int, usuario: str):
        self.cursor.execute("""
            INSERT INTO movimentacoes (item_id, tipo, quantidade, usuario)
            VALUES (?, ?, ?, ?)
        """, (item_id, tipo, quantidade, usuario))

    def listar(self, query_complemento: str, params: list) -> list[tuple]:
        query = """
            SELECT m.id, m.item_id, i.nome, i.modelo, m.tipo, m.quantidade, m.usuario, m.data
            FROM movimentacoes m
            LEFT JOIN itens i ON i.id = m.item_id
            WHERE 1=1
        """ + query_complemento
        return self.cursor.execute(query, params).fetchall()