


def comparar_planilha_banco(caminho_excel):
    from inventario.services.importador import importar_excel
    from inventario.controllers.crud import Crud

    crud = Crud()

    print("🔍 Comparando planilha com banco...\n")

    dados_planilha = importar_excel(caminho_excel)
    dados_banco = crud.listar_itens()

    # 🔧 normalização (mesma lógica do CRUD)
    def normalizar(item):
        return (
            str(item["nome"]).strip().lower(),
            str(item["modelo"]).strip().lower()
        )

    # 🔁 transformar em dict para comparação
    mapa_planilha = {
        normalizar(item): item for item in dados_planilha
    }

    mapa_banco = {
        normalizar(item): item for item in dados_banco
    }

    divergencias = []

    # 🔍 verificar itens diferentes
    for chave in mapa_planilha:
        item_planilha = mapa_planilha[chave]
        item_banco = mapa_banco.get(chave)

        if not item_banco:
            divergencias.append({
                "tipo": "❌ NÃO EXISTE NO BANCO",
                "item": item_planilha
            })
            continue

        if item_planilha["quantidade"] != item_banco["quantidade"]:
            divergencias.append({
                "tipo": "⚠️ QUANTIDADE DIFERENTE",
                "nome": item_planilha["nome"],
                "modelo": item_planilha["modelo"],
                "planilha": item_planilha["quantidade"],
                "banco": item_banco["quantidade"]
            })

    # 🔍 verificar itens que só existem no banco
    for chave in mapa_banco:
        if chave not in mapa_planilha:
            divergencias.append({
                "tipo": "❌ SÓ EXISTE NO BANCO",
                "item": mapa_banco[chave]
            })

    # 📊 RESULTADO
    if not divergencias:
        print("✅ Banco e planilha estão 100% sincronizados!")
    else:
        print(f"⚠️ Foram encontradas {len(divergencias)} divergências:\n")

        for d in divergencias[:20]:  # limita pra não poluir
            print(d)

        if len(divergencias) > 20:
            print(f"\n... e mais {len(divergencias) - 20} divergências")

    return divergencias