from inventario.database.db import conectar_db
from inventario.regras_dominio.item_rules import ItemRules
from inventario.services.log_service import registrar_log
from inventario.repositories.item_repository import ItemRepository
from inventario.repositories.movimentacao_repository import MovimentacaoRepository
from inventario.repositories.historico_repository import HistoricoRepository

class EstoqueService:
    def __init__(self, conn=None):
        # Gerencia a conexão e distribui para os Repositories puros
        self.conn = conn or conectar_db()
        self.item_repo = ItemRepository(self.conn)
        self.mov_repo = MovimentacaoRepository(self.conn)
        self.hist_repo = HistoricoRepository(self.conn)

    # ── VALIDACAO E NORMALIZAÇÃO DE DOMÍNIO ──────────────────────────────────
    
    def validar_dados_item(self, dados: dict):
        obrigatorios = ["nome", "tipo", "modelo", "quantidade", "caixa", "localizacao"]
        for campo in obrigatorios:
            if campo not in dados or not str(dados[campo]).strip():
                raise ValueError(f"Campo '{campo}' obrigatório e não pode estar vazio.")

        qtd = dados["quantidade"]
        if not isinstance(qtd, int) or qtd < 0:
            raise ValueError("Quantidade deve ser um inteiro não negativo.")

        proibidos = [";", "--", "/*", "*/"]
        for campo in ["nome", "tipo", "modelo", "caixa", "localizacao", "slot"]:
            valor = str(dados.get(campo, ""))
            if len(valor) > 255:
                raise ValueError(f"Campo '{campo}' não pode exceder 255 caracteres.")
            for p in proibidos:
                if p in valor:
                    raise ValueError(f"Campo '{campo}' contém caractere proibido: {p}")

    def normalizar_dados(self, dados: dict) -> dict:
        return {
            "nome": dados.get("nome", "").strip().title(),
            "tipo": dados.get("tipo", "").strip().title(),
            "modelo": dados.get("modelo", "").strip().upper(),
            "quantidade": int(dados.get("quantidade", 0)),
            "caixa": dados.get("caixa", "").strip(),
            "localizacao": dados.get("localizacao", "Não informado").strip().title(),
            "slot": dados.get("slot", "").strip().upper()
        }

    # ── OPERAÇÕES CORE DE NEGÓCIO (Antigo CRUD) ──────────────────────────────

    def registrar_item(self, dados_crus: dict, usuario="sistema") -> dict:

        print("\n")
        print("="*60)
        print("DEBUG SERVICE - REGISTRAR ITEM")
        print("="*60)

        print("Dados recebidos pela tela:")
        print(dados_crus)

        try:

            print("\n[1] Validando dados...")
            self.validar_dados_item(dados_crus)

            print("OK validação")

            print("\n[2] Normalizando dados...")
            dados = self.normalizar_dados(dados_crus)

            print("Dados normalizados:")
            print(dados)


            print("\n[3] Aplicando regras ItemRules...")

            sugestao = ItemRules.aplicar_regras({
                "nome": dados["nome"]
            })

            print("Sugestão encontrada:")
            print(sugestao)


            obrigatorios = ["nome", "modelo", "quantidade"]

            for campo in obrigatorios:
                if not dados_crus.get(campo):
                    raise ValueError(
                        f"Campo '{campo}' é obrigatório"
                    )


            if not dados_crus.get("caixa") and sugestao.get("caixa"):
                dados["caixa"] = sugestao["caixa"]

            if not dados_crus.get("localizacao") and sugestao.get("localizacao"):
                dados["localizacao"] = sugestao["localizacao"]

            if not dados_crus.get("slot") and sugestao.get("slot"):
                dados["slot"] = sugestao["slot"]


            print("\n[4] Procurando item existente...")

            existente = self.item_repo.buscar_por_nome_e_modelo(
                dados["nome"],
                dados["modelo"]
            )

            print("Resultado busca:")
            print(existente)



            if existente:

                print("\n[5] ITEM EXISTE - atualizando quantidade")

                item_id, quantidade_atual = existente

                nova_qtd = quantidade_atual + dados["quantidade"]

                print(
                    f"Quantidade antiga: {quantidade_atual}"
                )
                print(
                    f"Nova quantidade: {nova_qtd}"
                )


                self.item_repo.atualizar_quantidade(
                    item_id,
                    nova_qtd
                )

                print("Quantidade atualizada")


                self.hist_repo.registrar(
                    item_id,
                    "quantidade",
                    str(quantidade_atual),
                    str(nova_qtd),
                    usuario,
                    "entrada_manual"
                )

                print("Histórico registrado")


                self.mov_repo.registrar(
                    item_id,
                    "entrada",
                    dados["quantidade"],
                    usuario
                )

                print("Movimentação registrada")


                acao = "atualizado"



            else:

                print("\n[5] ITEM NOVO - inserindo")

                item_id = self.item_repo.salvar(dados)

                print("ID criado:")
                print(item_id)


                self.hist_repo.registrar(
                    item_id,
                    "*",
                    None,
                    f"{dados['nome']} | {dados['modelo']}",
                    usuario,
                    "inserido"
                )

                print("Histórico registrado")


                self.mov_repo.registrar(
                    item_id,
                    "entrada",
                    dados["quantidade"],
                    usuario
                )

                print("Movimentação registrada")


                acao = "inserido"



            print("\n[6] Registrando LOG")

            registrar_log(
                usuario,
                "INSERIR_ITEM",
                f"{dados['nome']} | {dados['modelo']} | qtd={dados['quantidade']}"
            )


            print("\n[7] Commit")

            self.conn.commit()


            print("COMMIT OK")

            print("="*60)
            print("FIM REGISTRO ITEM")
            print("="*60)


            return {
                "status":"ok",
                "acao":acao,
                "item_id":item_id
            }


        except Exception as e:

            print("\n")
            print("="*60)
            print("ERRO NO SERVICE")
            print(type(e))
            print(e)
            print("="*60)


            self.conn.rollback()

            return {
                "status":"erro",
                "mensagem":str(e)
            }

    def atualizar_item(self, item_id: int, novos_dados: dict, usuario="sistema") -> dict:
        try:
            r = self.item_repo.buscar_por_id(item_id)
            if not r: raise ValueError("Item não encontrado")

            snapshot_antes = {"nome": r[0], "tipo": r[1], "modelo": r[2], "quantidade": r[3], "caixa": r[4], "localizacao": r[5], "slot": r[6]}
            item_dict = dict(snapshot_antes)
            item_dict.update(novos_dados)

            self.validar_dados_item(item_dict)
            item_dict = self.normalizar_dados(item_dict)

            self.item_repo.atualizar_item_completo(item_id, item_dict)

            changes = []
            for campo in ["nome", "tipo", "modelo", "quantidade", "caixa", "localizacao", "slot"]:
                antes, depois = str(snapshot_antes[campo]), str(item_dict[campo])
                if antes != depois:
                    self.hist_repo.registrar(item_id, campo, antes, depois, usuario, "editado")
                    changes.append(f"{campo}:{antes}->{depois}")

            if changes:
                registrar_log(usuario, "EDITAR_ITEM", f"{item_dict['nome']} | {item_dict['modelo']} | " + "; ".join(changes))

            diff = item_dict["quantidade"] - snapshot_antes["quantidade"]
            if diff != 0:
                self.mov_repo.registrar(item_id, "entrada" if diff > 0 else "saida", abs(diff), usuario)

            self.conn.commit()
            return {"status": "ok", "mensagem": "Item atualizado com sucesso", "item_id": item_id}
        except Exception as e:
            self.conn.rollback()
            return {"status": "erro", "mensagem": str(e)}

    def deletar_item(self, item_id: int, usuario="sistema") -> dict:
        try:
            r = self.item_repo.buscar_por_id(item_id)
            if not r: raise ValueError("Item não encontrado")
            nome, modelo, quantidade = r[0], r[2], r[3]

            if quantidade > 0:
                self.mov_repo.registrar(item_id, "saida", quantidade, usuario)

            self.hist_repo.registrar(item_id, "*", f"{nome} | {modelo} | qtd={quantidade}", None, usuario, "deletado")
            self.item_repo.deletar(item_id)
            
            registrar_log(usuario, "DELETAR_ITEM", f"{nome} | {modelo} | qtd={quantidade}")
            self.conn.commit()
            return {"status": "ok", "mensagem": "Item deletedo com sucesso", "item_id": item_id}
        except Exception as e:
            self.conn.rollback()
            return {"status": "erro", "mensagem": str(e)}

    # ── MÉTODOS DE CONSULTA PASSADOS AO COMPLETER / UI ───────────────────────

    def obter_sugestoes_por_termo(self, termo: str) -> list[str]:
        rows = self.item_repo.buscar_distinct_nomes(termo)
        return [str(r[0]) for r in rows]

    def prever_atributos_por_nome(self, nome: str) -> dict:
        return ItemRules.aplicar_regras({"nome": nome})

    def buscar_detalhes_por_nome(self, nome: str) -> dict | None:
        rows = self.item_repo.buscar_por_nome_like(nome)
        if not rows: return None
        r = rows[0]
        return {"nome": r[0], "tipo": r[1], "modelo": r[2], "caixa": r[3], "localizacao": r[4], "slot": r[5]}

    def listar_todos_itens(self) -> list[dict]:
        rows = self.item_repo.listar_todos()
        return [
            {"id": r[0], "nome": r[1], "tipo": r[2], "modelo": r[3],
             "quantidade": r[4], "caixa": r[5], "localizacao": r[6], "slot": r[7]}
            for r in rows
        ]
        
        
    def buscar_itens(self, texto):
        print("[EstoqueService] Entrou no service em buscar itens")
        
        rows = self.item_repo.buscar_por_termo(texto)
        
        print(f"[EstoqueService] {len(rows)} itens encontrados para termo='{texto}'")
       
        return [
            {
                "id": r[0],
                "nome": r[1],
                "tipo": r[2],
                "modelo": r[3],
                "quantidade": r[4],
                "caixa": r[5],
                "localizacao": r[6],
                "slot": r[7]
            }
            for r in rows
        ]
    
        # ── HISTÓRICO E MOVIMENTAÇÕES ──────────────────────────────────────────

    def listar_movimentacoes(self, item_id=None, tipo=None, usuario=None):
        rows = self.mov_repo.listar(
            item_id=item_id,
            tipo=tipo,
            usuario=usuario
        )
        print(f"[EstoqueService] {len(rows)} movimentações encontradas para item_id={item_id}, tipo={tipo}, usuario={usuario}")
        return [
            {
                "id": r[0],
                "item_id": r[1],
                "item_nome": r[2],
                "item_modelo": r[3],
                "tipo": r[4],
                "quantidade": r[5],
                "usuario": r[6],
                "data": r[7],
            }
            for r in rows
               
        ]


    def listar_historico(self, item_id=None, usuario=None):
        rows = self.hist_repo.listar(
            item_id=item_id,
            usuario=usuario
        )
        print(f"[EstoqueService] {len(rows)} registros de histórico encontrados para item_id={item_id}, usuario={usuario}")
        return [
            {
                "id": r[0],
                "item_id": r[1],
                "item_nome": r[2],
                "item_modelo": r[3],
                "campo": r[4],
                "valor_anterior": r[5],
                "valor_novo": r[6],
                "usuario": r[7],
                "acao": r[8],
                "data": r[9],
            }
            for r in rows
        ]