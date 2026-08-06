"""
lista_compras_repository.py — Acesso a dados da tabela lista_compras.

Módulo independente do estoque: não referencia item_id nem a tabela `itens`.
Toda consulta SQL do módulo de Lista de Compras fica centralizada aqui.
"""

import sqlite3


class ListaComprasRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = connection.cursor()

    # ── ESCRITA ───────────────────────────────────────────────────────────

    def adicionar_item(self, dados: dict, usuario: str = "sistema") -> int:

        self.cursor.execute("""
            INSERT INTO lista_compras
            (
                nome,
                modelo,
                quantidade_atual,
                status,
                observacao,
                usuario,
                criado_em
            )
            VALUES (?, ?, ?, 'PENDENTE', ?, ?, CURRENT_TIMESTAMP)
        """, (
            dados.get("nome"),
            dados.get("modelo"),
            dados.get("quantidade", 1),
            dados.get("observacao"),
            usuario
        ))

        return self.cursor.lastrowid
    print("[ListaComprasRepository] Item {nome}, modelo {modelo} e quantidade -> {quantidade} adicionado à lista de compras com sucesso.")

    def editar_item(self, item_id: int, dados: dict):
        self.cursor.execute("""
            UPDATE lista_compras
            SET nome=?, modelo=?, quantidade_atual=?, observacao=?
            WHERE id=?
        """, (
            dados.get("nome"),
            dados.get("tipo"),
            dados.get("modelo"),
            dados.get("quantidade", 1),
            dados.get("observacao"),
            item_id
        ))
        print(f"[ListaComprasRepository] Item {item_id} atualizado com sucesso.")

    def remover_item(self, item_id: int):
        self.cursor.execute("DELETE FROM lista_compras WHERE id=?", (item_id,))
        print(f"[ListaComprasRepository] Item {item_id} removido da lista de compras com sucesso.")

    def marcar_comprado(self, item_id: int):
        self.cursor.execute("""
            UPDATE lista_compras
            SET status='COMPRADO'
            WHERE id=?
        """,(item_id,))
        print(f"[ListaComprasRepository] Item {item_id} marcado como comprado.")

    def desmarcar_comprado(self, item_id: int):
        self.cursor.execute("""
            UPDATE lista_compras
            SET status='PENDENTE'

            WHERE id=?
        """, (item_id,))

    # ── LEITURA ───────────────────────────────────────────────────────────

    _COLUNAS_SELECT = """
        id, item_id, nome, modelo, quantidade_atual, status, observacao, usuario, criado_em
        """

    def listar_itens(self):
        self.cursor.execute(f"""
            SELECT {self._COLUNAS_SELECT}
            FROM lista_compras
            ORDER BY status ASC, criado_em DESC
        """)
    
        return self.cursor.fetchall()

    def buscar_por_id(self, item_id: int):
        self.cursor.execute(f"""
            SELECT {self._COLUNAS_SELECT}
            FROM lista_compras
            WHERE id=?
        """, (item_id,))
        return self.cursor.fetchone()

    def pesquisar(self, termo: str):
        termo_like = f"%{termo}%"
        self.cursor.execute(f"""
            SELECT {self._COLUNAS_SELECT}
            FROM lista_compras
            WHERE nome LIKE ? OR modelo LIKE ?
            ORDER BY comprado ASC, data_adicionado DESC
        """, (termo_like, termo_like, termo_like))
        return self.cursor.fetchall()