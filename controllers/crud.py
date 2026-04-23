from database.db import conectar_db

class Crud:
    def __init__(self):
        self.conn = conectar_db()
        self.cursor = self.conn.cursor()
       
    
    
    def inserir_item(self, dados, usuario="sistema"):
        try:
            # 1. validar
            self.validar_dados_item(dados)

            # 2. normalizar
            dados = self.normalizar_dados(dados)

            # 3. verificar duplicidade
            existente = self.item_existe(dados["nome"], dados["modelo"])

            if existente:
                item_id, quantidade_atual = existente
                nova_qtd = quantidade_atual + dados["quantidade"]

                self.cursor.execute("""
                    UPDATE itens
                    SET quantidade = ?
                    WHERE id = ?
                """, (nova_qtd, item_id))

                acao = "atualizado"

            else:
                self.cursor.execute("""
                    INSERT INTO itens (nome, tipo, modelo, quantidade, caixa, localizacao, slot)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    dados["nome"],
                    dados["tipo"],
                    dados["modelo"],
                    dados["quantidade"],
                    dados["caixa"],
                    dados["localizacao"],
                    dados["slot"]
                ))

                item_id = self.cursor.lastrowid
                acao = "inserido"

            # 🔥 REGISTRAR MOVIMENTAÇÃO (AQUI!)
            self.registrar_movimentacao(
                item_id,
                "entrada",
                dados["quantidade"],
                usuario
            )

            # commit final
            self.conn.commit()

            return {
                "status": "ok",
                "acao": acao,
                "item_id": item_id
            }

        except Exception as e:
            return {
                "status": "erro",
                "mensagem": str(e)
            }

    def registrar_movimentacao(self, item_id, tipo, quantidade, usuario):
        self.cursor.execute("""
            INSERT INTO movimentacoes (item_id, tipo, quantidade, usuario)
            VALUES (?, ?, ?, ?)
        """, (item_id, tipo, quantidade, usuario))
        try:
            self.conn.commit()
        except Exception as e:
            print("Erro ao registrar movimentação:", e)


            
    def listar_itens(self):
        resultado = self.cursor.execute("""
            SELECT id, nome, tipo, modelo, quantidade, caixa, localizacao, slot FROM itens
        """).fetchall()

        itens = []
        for row in resultado:
            itens.append({
                "id": row[0],
                "nome": row[1],
                "tipo": row[2],
                "modelo": row[3],
                "quantidade": row[4],
                "caixa": row[5],
                "localizacao": row[6],
                "slot": row[7]
            })
        return itens

    def validar_dados_item(self, dados):
        campos_obrigatorios = ["nome", "tipo", "modelo", "quantidade", "caixa", "localizacao"]

        for campo in campos_obrigatorios:
            if campo not in dados or not str(dados[campo]).strip():
                raise ValueError(f"O campo '{campo}' é obrigatório e não pode estar vazio.")      
        
        quantidade = dados["quantidade"]
        if not isinstance(quantidade, int) or quantidade < 0:
            raise ValueError("A quantidade deve ser um número inteiro não negativo.")
        
        if not isinstance(quantidade, int) or quantidade < 0:
                raise ValueError("A quantidade deve ser um número inteiro não negativo.")
            
        for campo in ["nome", "tipo", "modelo", "caixa", "localizacao", "slot"]:
            if not isinstance(dados[campo], str):
                raise ValueError(f"O campo '{campo}' deve ser uma string.")
            
        for campo in ["nome", "tipo", "modelo", "caixa", "localizacao", "slot"]:
            if len(dados[campo]) > 255:
                raise ValueError(f"O campo '{campo}' não pode exceder 255 caracteres.")
            
        for campo in  [";", "--", "/*", "*/"]:
            for valor in [dados["nome"], dados["tipo"], dados["modelo"], dados["caixa"], dados["localizacao"], dados["slot"]]:
                if campo in valor:
                    raise ValueError(f"O campo '{valor}' contém caracteres proibidos: {campo}")    
            
    def item_existe(self, nome, modelo):
        return self.cursor.execute("""
            SELECT id, quantidade FROM itens
            WHERE nome = ? AND modelo = ?
        """, (nome, modelo)).fetchone()


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

    def controlar_duplicidade(self, nome, modelo, item_id=None):
        query = """
            SELECT id FROM itens
            WHERE nome = ? AND modelo = ?
        """
        params = [nome, modelo]

        if item_id:
            query += " AND id != ?"
            params.append(item_id)
            print("Verificando duplicidade para atualização:", params)
        else:
            print("Verificando duplicidade para inserção:", params)

        return self.cursor.execute(query, params).fetchone()

    #função de update
    def atualizar_item(self, item_id, novos_dados, usuario="sistema"):
        try:
            # verificar se item existe
            item_atual = self.cursor.execute("""
                SELECT nome, tipo, modelo, quantidade, caixa, localizacao, slot
                FROM itens WHERE id = ?
            """, (item_id,)).fetchone()

            if not item_atual:
                raise ValueError("Item não encontrado")

            # montar dicionário atual
            item_dict = {
                "nome": item_atual[0],
                "tipo": item_atual[1],
                "modelo": item_atual[2],
                "quantidade": item_atual[3],
                "caixa": item_atual[4],
                "localizacao": item_atual[5],
                "slot": item_atual[6]
            }

            # atualizar apenas campos enviados
            item_dict.update(novos_dados)

            #  validar
            self.validar_dados_item(item_dict)

            #  normalizar
            item_dict = self.normalizar_dados(item_dict)

            # verificar duplicidade (outro item igual)
            existente = self.cursor.execute("""
                SELECT id FROM itens
                WHERE nome = ? AND modelo = ? AND id != ?
            """, (item_dict["nome"], item_dict["modelo"], item_id)).fetchone()

            if existente:
                raise ValueError("Já existe outro item com mesmo nome e modelo")

            # verificar mudança de quantidade
            quantidade_antiga = item_atual[3]
            quantidade_nova = item_dict["quantidade"]

            diferenca = quantidade_nova - quantidade_antiga

            # atualizar banco
            self.cursor.execute("""
                UPDATE itens
                SET nome=?, tipo=?, modelo=?, quantidade=?, caixa=?, localizacao=?, slot=?
                WHERE id=?
            """, (
                item_dict["nome"],
                item_dict["tipo"],
                item_dict["modelo"],
                item_dict["quantidade"],
                item_dict["caixa"],
                item_dict["localizacao"],
                item_dict["slot"],
                item_id
            ))

            #registrar movimentação se mudou quantidade
            if diferenca != 0:
                tipo = "entrada" if diferenca > 0 else "saida"

                self.registrar_movimentacao(
                    item_id,
                    tipo,
                    abs(diferenca),
                    usuario
                )

            # commit
            self.conn.commit()

            return {
                "status": "ok",
                "mensagem": "Item atualizado com sucesso",
                "item_id": item_id
            }

        except Exception as e:
            return {
                "status": "erro",
                "mensagem": str(e)
            }

    #deletar item
    def deletar_item(self, item_id, usuario="sistema"):
        try:
            # verificar se item existe
            item_atual = self.cursor.execute("""
                SELECT quantidade FROM itens WHERE id = ?
            """, (item_id,)).fetchone()

            if not item_atual:
                raise ValueError("Item não encontrado")
            
            quantidade = item_atual[0]

            #Registrar saída antes de deletar 
            if quantidade >0:
                self.registrar_movimentacao(
                    item_id,
                    "saida",
                    quantidade,
                    usuario
                )

            # deletar item
            self.cursor.execute("""
                DELETE FROM itens WHERE id = ?
            """, (item_id,))

            # commit
            self.conn.commit()

            return {
                "status": "ok",
                "mensagem": "Item deletado com sucesso",
                "item_id": item_id
            }

        except Exception as e:
            return {
                "status": "erro",
                "mensagem": str(e)
            }
            
            