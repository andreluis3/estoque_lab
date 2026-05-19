from controllers.crud import Crud
from services.importador import importar_excel
from utils.normalizador import normalizar


def sincronizar_planilha_banco(caminho_excel):
    crud = Crud()

    print("🔄 Auto sync iniciando...")

    excel = importar_excel(caminho_excel)

    # 🔥 REMOVE DUPLICADOS DO EXCEL PRIMEIRO
    vistos = set()
    excel_limpo = []

    for i in excel:
        chave = (
            normalizar(i["nome"]),
            normalizar(i["modelo"]),
            normalizar(i.get("tipo", ""))
        )

        if chave not in vistos:
            vistos.add(chave)
            excel_limpo.append(i)

    banco = crud.listar_itens()

    mapa_excel = {
        (
            normalizar(i["nome"]),
            normalizar(i["modelo"]),
            normalizar(i.get("tipo", ""))
        ): i
        for i in excel_limpo
    }

    mapa_banco = {
        (
            normalizar(i["nome"]),
            normalizar(i["modelo"]),
            normalizar(i.get("tipo", ""))
        ): i
        for i in banco
    }

    # 📥 Excel → Banco
    for chave, item_excel in mapa_excel.items():

        if chave in mapa_banco:
            item_banco = mapa_banco[chave]

            # 🔥 só atualiza se realmente mudou
            if item_excel["quantidade"] != item_banco["quantidade"]:
               crud.atualizar_quantidade(
                item_banco["id"],
                item_excel["quantidade"]
            )

        else:
            crud.inserir_item(item_excel, usuario="auto_sync")

    print("✅ Sync finalizado sem duplicação")
    
