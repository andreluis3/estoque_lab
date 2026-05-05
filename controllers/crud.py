"""
crud.py — Operações CRUD com auditoria completa.

Toda inserção, atualização e exclusão é registrada em:
  - movimentacoes: rastreia entradas/saídas de quantidade
  - historico_alteracoes: rastreia qualquer mudança de campo
"""

from database.db import conectar_db
from services.log_service import registrar_log

class Crud:
    def __init__(self):
        self.conn = conectar_db()
        self.cursor = self.conn.cursor()

    # ═══════════════════════════════════════════════════════════════════════
    #  INSERIR
    # ═══════════════════════════════════════════════════════════════════════

    def inserir_item(self, dados, usuario="sistema"):
        try:
            self.validar_dados_item(dados)
            dados = self.normalizar_dados(dados)

            existente = self.item_existe(dados["nome"], dados["modelo"])

            if existente:
                # Item já existe: APENAS soma a quantidade (entrada manual)
                item_id, quantidade_atual = existente
                nova_qtd = quantidade_atual + dados["quantidade"]

                self.cursor.execute("""
                    UPDATE itens SET quantidade=?, atualizado_em=CURRENT_TIMESTAMP
                    WHERE id=?
                """, (nova_qtd, item_id))

                self._registrar_historico(
                    item_id, "quantidade",
                    str(quantidade_atual), str(nova_qtd),
                    usuario, "entrada_manual"
                )
                self._registrar_movimentacao(item_id, "entrada", dados["quantidade"], usuario)
                acao = "atualizado"
                log_acao = "ENTRADA_MANUAL"
                detalhe = f"{dados['nome']} | {dados['modelo']} | soma={dados['quantidade']} para {nova_qtd}"

            else:
                self.cursor.execute("""
                    INSERT INTO itens (nome, tipo, modelo, quantidade, caixa, localizacao, slot)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    dados["nome"], dados["tipo"], dados["modelo"], dados["quantidade"],
                    dados["caixa"], dados["localizacao"], dados["slot"]
                ))
                item_id = self.cursor.lastrowid

                self._registrar_historico(
                    item_id, "*", None,
                    f"{dados['nome']} | {dados['modelo']}",
                    usuario, "inserido"
                )
                self._registrar_movimentacao(item_id, "entrada", dados["quantidade"], usuario)
                acao = "inserido"
                log_acao = "INSERIR_ITEM"
                detalhe = f"{dados['nome']} | {dados['modelo']} | qtd={dados['quantidade']}"

            registrar_log(usuario, log_acao, detalhe)
            self.conn.commit()
            return {"status": "ok", "acao": acao, "item_id": item_id}

        except Exception as e:
            return {"status": "erro", "mensagem": str(e)}

    # ═══════════════════════════════════════════════════════════════════════
    #  LISTAR
    # ═══════════════════════════════════════════════════════════════════════

    def listar_itens(self):
        rows = self.cursor.execute("""
            SELECT id, nome, tipo, modelo, quantidade, caixa, localizacao, slot
            FROM itens ORDER BY nome
        """).fetchall()

        return [
            {"id": r[0], "nome": r[1], "tipo": r[2], "modelo": r[3],
             "quantidade": r[4], "caixa": r[5], "localizacao": r[6], "slot": r[7]}
            for r in rows
        ]

    # ═══════════════════════════════════════════════════════════════════════
    #  ATUALIZAR
    # ═══════════════════════════════════════════════════════════════════════

    def atualizar_item(self, item_id, novos_dados, usuario="sistema"):
        try:
            item_atual = self.cursor.execute("""
                SELECT nome, tipo, modelo, quantidade, caixa, localizacao, slot
                FROM itens WHERE id=?
            """, (item_id,)).fetchone()

            if not item_atual:
                raise ValueError("Item não encontrado")

            item_dict = {
                "nome": item_atual[0], "tipo": item_atual[1], "modelo": item_atual[2],
                "quantidade": item_atual[3], "caixa": item_atual[4],
                "localizacao": item_atual[5], "slot": item_atual[6]
            }

            # Guarda snapshot antes da mudança
            snapshot_antes = dict(item_dict)

            item_dict.update(novos_dados)
            self.validar_dados_item(item_dict)
            item_dict = self.normalizar_dados(item_dict)

            # Checa duplicidade (outro item com mesmo nome+modelo)
            duplicado = self.cursor.execute("""
                SELECT id FROM itens WHERE nome=? AND modelo=? AND id!=?
            """, (item_dict["nome"], item_dict["modelo"], item_id)).fetchone()

            if duplicado:
                raise ValueError("Já existe outro item com mesmo nome e modelo")

            self.cursor.execute("""
                UPDATE itens
                SET nome=?, tipo=?, modelo=?, quantidade=?, caixa=?, localizacao=?, slot=?,
                    atualizado_em=CURRENT_TIMESTAMP
                WHERE id=?
            """, (
                item_dict["nome"], item_dict["tipo"], item_dict["modelo"],
                item_dict["quantidade"], item_dict["caixa"],
                item_dict["localizacao"], item_dict["slot"], item_id
            ))
    
            campos = ["nome", "tipo", "modelo", "quantidade", "caixa", "localizacao", "slot"]
            changes = []
            for campo in campos:
                antes = str(snapshot_antes[campo])
                depois = str(item_dict[campo])
                if antes != depois:
                    self._registrar_historico(item_id, campo, antes, depois, usuario, "editado")
                    changes.append(f"{campo}:{antes}->{depois}")

            if changes:
                registrar_log(
                    usuario,
                    "EDITAR_ITEM",
                    f"{item_dict['nome']} | {item_dict['modelo']} | " + "; ".join(changes)
                )

            diff = item_dict["quantidade"] - snapshot_antes["quantidade"]
            if diff != 0:
                tipo_mov = "entrada" if diff > 0 else "saida"
                self._registrar_movimentacao(item_id, tipo_mov, abs(diff), usuario)

            self.conn.commit()
            return {"status": "ok", "mensagem": "Item atualizado com sucesso", "item_id": item_id}

        except Exception as e:
            return {"status": "erro", "mensagem": str(e)}


    def deletar_item(self, item_id, usuario="sistema"):
        try:
            item_atual = self.cursor.execute("""
                SELECT nome, modelo, quantidade FROM itens WHERE id=?
            """, (item_id,)).fetchone()

            if not item_atual:
                raise ValueError("Item não encontrado")

            nome, modelo, quantidade = item_atual

            if quantidade > 0:
                self._registrar_movimentacao(item_id, "saida", quantidade, usuario)

            self._registrar_historico(
                item_id, "*",
                f"{nome} | {modelo} | qtd={quantidade}",
                None, usuario, "deletado"
            )

            self.cursor.execute("DELETE FROM itens WHERE id=?", (item_id,))
            registrar_log(usuario, "DELETAR_ITEM", f"{nome} | {modelo} | qtd={quantidade}")
            self.conn.commit()

            return {"status": "ok", "mensagem": "Item deletado com sucesso", "item_id": item_id}

        except Exception as e:
            return {"status": "erro", "mensagem": str(e)}


    def listar_historico(self, item_id=None, usuario=None, acao=None, limite=200) -> list[dict]:
        """
        Retorna o histórico de alterações com filtros opcionais.
        """
        query = """
            SELECT
                h.id, h.item_id, i.nome, i.modelo,
                h.campo, h.valor_anterior, h.valor_novo,
                h.usuario, h.acao, h.data
            FROM historico_alteracoes h
            LEFT JOIN itens i ON i.id = h.item_id
            WHERE 1=1
        """
        params = []

        if item_id is not None:
            query += " AND h.item_id = ?"
            params.append(item_id)

        if usuario:
            query += " AND h.usuario = ?"
            params.append(usuario)

        if acao:
            query += " AND h.acao = ?"
            params.append(acao)

        query += " ORDER BY h.data DESC LIMIT ?"
        params.append(limite)

        rows = self.cursor.execute(query, params).fetchall()

        return [
            {
                "id": r[0],
                "item_id": r[1],
                "item_nome": r[2] or "—",
                "item_modelo": r[3] or "—",
                "campo": r[4],
                "valor_anterior": r[5],
                "valor_novo": r[6],
                "usuario": r[7],
                "acao": r[8],
                "data": r[9]
            }
            for r in rows
        ]

    def listar_movimentacoes(self, item_id=None, tipo=None, usuario=None, limite=200) -> list[dict]:
        """
        Retorna movimentações (entradas/saídas de quantidade).
        """
        query = """
            SELECT
                m.id, m.item_id, i.nome, i.modelo,
                m.tipo, m.quantidade, m.usuario, m.data
            FROM movimentacoes m
            LEFT JOIN itens i ON i.id = m.item_id
            WHERE 1=1
        """
        params = []

        if item_id is not None:
            query += " AND m.item_id = ?"
            params.append(item_id)

        if tipo:
            query += " AND m.tipo = ?"
            params.append(tipo)

        if usuario:
            query += " AND m.usuario = ?"
            params.append(usuario)

        query += " ORDER BY m.data DESC LIMIT ?"
        params.append(limite)

        rows = self.cursor.execute(query, params).fetchall()

        return [
            {
                "id": r[0],
                "item_id": r[1],
                "item_nome": r[2] or "—",
                "item_modelo": r[3] or "—",
                "tipo": r[4],
                "quantidade": r[5],
                "usuario": r[6],
                "data": r[7]
            }
            for r in rows
        ]

    # ═══════════════════════════════════════════════════════════════════════
    #  BUSCAS
    # ═══════════════════════════════════════════════════════════════════════

    def buscar_item(self, texto, filtro="nome"):
        if filtro == "nome":
            q = "SELECT * FROM itens WHERE nome LIKE ? LIMIT 20"
            p = (f"%{texto}%",)
        elif filtro == "modelo":
            q = "SELECT * FROM itens WHERE modelo LIKE ? LIMIT 20"
            p = (f"%{texto}%",)
        else:
            q = "SELECT * FROM itens WHERE nome LIKE ? OR modelo LIKE ? LIMIT 20"
            p = (f"%{texto}%", f"%{texto}%")

        return self.cursor.execute(q, p).fetchall()

    def buscar_por_nome(self, nome):
        row = self.cursor.execute("""
            SELECT nome, tipo, modelo, caixa, localizacao, slot
            FROM itens WHERE LOWER(nome) LIKE LOWER(?) LIMIT 1
        """, (nome + "%",)).fetchone()

        if not row:
            return None

        return {"nome": row[0], "tipo": row[1], "modelo": row[2],
                "caixa": row[3], "localizacao": row[4], "slot": row[5]}

    def buscar_por_nome_exato(self, nome):
        row = self.cursor.execute("""
            SELECT nome, tipo, modelo, caixa, localizacao, slot
            FROM itens WHERE nome = ?
        """, (nome,)).fetchone()

        if not row:
            return None

        return {"nome": row[0], "tipo": row[1], "modelo": row[2],
                "caixa": row[3], "localizacao": row[4], "slot": row[5]}

    def buscar_nomes_like(self, texto):
        return [r[0] for r in self.cursor.execute("""
            SELECT DISTINCT nome FROM itens WHERE nome LIKE ? LIMIT 10
        """, (f"%{texto}%",)).fetchall()]

    def buscar_padrao_mais_comum(self, texto):
        row = self.cursor.execute("""
            SELECT tipo, caixa, localizacao, slot, COUNT(*) as freq
            FROM itens WHERE LOWER(nome) LIKE LOWER(?)
            GROUP BY tipo, caixa, localizacao, slot
            ORDER BY freq DESC LIMIT 1
        """, (f"%{texto}%",)).fetchone()

        if not row:
            return None

        return {"tipo": row[0], "caixa": row[1], "localizacao": row[2],
                "slot": row[3], "frequencia": row[4]}

    def atualizar_quantidade(self, nome, modelo, nova_qtd):
        self.cursor.execute("""
            UPDATE itens SET quantidade=?, atualizado_em=CURRENT_TIMESTAMP
            WHERE nome=? AND modelo=?
        """, (nova_qtd, nome, modelo))
        self.conn.commit()

    # ═══════════════════════════════════════════════════════════════════════
    #  HELPERS INTERNOS
    # ═══════════════════════════════════════════════════════════════════════

    def item_existe(self, nome, modelo):
        return self.cursor.execute("""
            SELECT id, quantidade FROM itens WHERE nome=? AND modelo=?
        """, (nome, modelo)).fetchone()

    def _registrar_movimentacao(self, item_id, tipo, quantidade, usuario):
        self.cursor.execute("""
            INSERT INTO movimentacoes (item_id, tipo, quantidade, usuario)
            VALUES (?, ?, ?, ?)
        """, (item_id, tipo, quantidade, usuario))
        registrar_log(
            usuario,
            f"MOVIMENTACAO_{tipo.upper()}",
            f"item_id={item_id} | qtd={quantidade}"
        )

    def _registrar_historico(self, item_id, campo, valor_anterior, valor_novo, usuario, acao):
        self.cursor.execute("""
            INSERT INTO historico_alteracoes
                (item_id, campo, valor_anterior, valor_novo, usuario, acao)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (item_id, campo, valor_anterior, valor_novo, usuario, acao))

    def validar_dados_item(self, dados):
        obrigatorios = ["nome", "tipo", "modelo", "quantidade", "caixa", "localizacao"]
        for campo in obrigatorios:
            if campo not in dados or not str(dados[campo]).strip():
                raise ValueError(f"Campo '{campo}' obrigatório e não pode estar vazio.")

        qtd = dados["quantidade"]
        if not isinstance(qtd, int) or qtd < 0:
            raise ValueError("Quantidade deve ser um inteiro não negativo.")

        proibidos = [";", "--", "/*", "*/"]
        campos_texto = ["nome", "tipo", "modelo", "caixa", "localizacao", "slot"]
        for campo in campos_texto:
            valor = str(dados.get(campo, ""))
            if len(valor) > 255:
                raise ValueError(f"Campo '{campo}' não pode exceder 255 caracteres.")
            for p in proibidos:
                if p in valor:
                    raise ValueError(f"Campo '{campo}' contém caractere proibido: {p}")

    def normalizar_dados(self, dados):
        return {
            "nome": dados.get("nome", "").strip().title(),
            "tipo": dados.get("tipo", "").strip().title(),
            "modelo": dados.get("modelo", "").strip().upper(),
            "quantidade": int(dados.get("quantidade", 0)),
            "caixa": dados.get("caixa", "").strip(),
            "localizacao": dados.get("localizacao", "Não informado").strip().title(),
            "slot": dados.get("slot", "").strip().upper()
        }