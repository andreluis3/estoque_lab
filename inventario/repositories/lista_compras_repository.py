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

        item_id = self.cursor.lastrowid

        print(
            f"[ListaComprasRepository] [SUCESSO] "
            f"Item salvo na lista de compras | "
            f"ID={item_id} | "
            f"Nome={dados.get('nome')} | "
            f"Modelo={dados.get('modelo') or '—'} | "
            f"Quantidade={dados.get('quantidade', 1)}"
        )
        return item_id

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
        try:
            self.cursor.execute(
                "DELETE FROM lista_compras WHERE id=?",
                (item_id,)
            )

            print(
                f"[ListaComprasRepository] [SUCESSO] "
                f"Item removido da lista de compras | ID={item_id}"
            )

        except Exception as e:
            print(
                f"[ListaComprasRepository] [ERRO] "
                f"Falha ao remover item | ID={item_id} | "
                f"Tipo={type(e).__name__} | Erro={e}"
            )
            raise
        
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