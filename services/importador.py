import pandas as pd
from controllers.crud import Crud
from openpyxl import load_workbook
from openpyxl import load_workbook


# 🔥 MAPEAMENTO CORRETO (ALINHADO COM SEU BANCO)
COLUNAS_PLANILHA = {
    "Nome Item": "nome",
    "Tipo": "tipo",
    "Modelo": "modelo",
    "Quantidade": "quantidade",
    "Caixa": "caixa",
    "Localização": "localizacao",
    "Slot": "slot"
}


import os
import pandas as pd
from controllers.crud import Crud

def importar_excel(caminho: str) -> list[dict]:
    df = pd.read_excel(caminho)
    print("📂 CAMINHO REAL DO ARQUIVO:")
    print(os.path.abspath(caminho))
    print(caminho)
    print("PRIMEIRA LINHA DO DF:")
    print(df.iloc[0])

    print("COLUNAS BRUTAS DO EXCEL:")
    print(list(df.columns))
    
    print("VALORES DE QUANTIDADE DO EXCEL:")
    print(df["quantidade"].head(20))

    df.columns = df.columns.str.strip()

    # 🔁 RENOMEAR
    df = df.rename(columns=COLUNAS_PLANILHA)

    for col in COLUNAS_PLANILHA.values():
        if col not in df.columns:
            df[col] = None

    # 🔥 LIMPEZA DOS DADOS
    df["nome"] = df["nome"].fillna("").astype(str).str.strip()
    df["tipo"] = df["tipo"].fillna("Outros").astype(str).str.strip()
    df["modelo"] = df["modelo"].fillna("").astype(str).str.strip()

    df["quantidade"] = df["quantidade"].fillna(0).astype(int)

    df["caixa"] = df["caixa"].fillna("").astype(str).str.strip()


    df["localizacao"] = (
        df["localizacao"]
        .fillna("")
        .astype(str)
        .str.strip()
        .replace("", "Não informado")
    )

    df["slot"] = (
        df["slot"]
        .fillna("")
        .astype(str)
        .str.strip()
    )
    
    df["slot"] = df["slot"].replace("", "Não informado")

    print("COLUNAS RENOMEADAS:")
    print(list(df.columns))

    return df.to_dict(orient="records")



def gerar_relatorio_inconsistencias(erros, total):
    print("\n🔍 VALIDAÇÃO FINAL:")

    if not erros:
        print("✅ Banco 100% sincronizado com a planilha!")
        return

    print(f"❌ {len(erros)} inconsistências encontradas:\n")

    for erro in erros[:10]:  # limita saída
        print(
            f"⚠️ {erro['nome']} | {erro['modelo']} → Excel: {erro['excel']} | Banco: {erro['banco']}"
        )

    if len(erros) > 10:
        print(f"... e mais {len(erros) - 10} erros")

    print("\n📊 RESUMO:")
    print(f"Total de itens: {total}")

def importar_para_banco(caminho):

    crud = Crud()

    print("🧹 Limpando banco...")
    crud.cursor.execute("DELETE FROM itens")
    crud.conn.commit()

    print("📥 Importando dados da planilha...")
    dados = importar_excel(caminho)

    total = len(dados)

    for i, item in enumerate(dados):
        crud.inserir_item(item, usuario="importacao")

        if i % 50 == 0:
            print(f"📊 Progresso: {i}/{total}")

    print("✅ Importação concluída!")

    # 🔥 VALIDAÇÃO FINAL
    erros = validar_diferencas(caminho)

    print("\n🔍 VALIDAÇÃO FINAL:")

    if not erros:
        print("✅ Banco 100% sincronizado com a planilha!")
    else:
        print(f"❌ {len(erros)} inconsistências encontradas:\n")

        for erro in erros[:10]:  # limita pra não poluir
            print(
                f"⚠️ {erro['nome']} | {erro['modelo']} → Excel: {erro['excel']} | Banco: {erro['banco']}"
            )

        if len(erros) > 10:
            print(f"... e mais {len(erros) - 10} erros")

        print("\n📊 RESUMO DA IMPORTAÇÃO:")
        print(f"Total: {total}")
        print(f"Erros: {erros}")
        erros = validar_diferencas(caminho)
        gerar_relatorio_inconsistencias(erros, total)
    
def validar_diferencas(caminho_excel):
        crud = Crud()

        df_excel = pd.read_excel(caminho_excel)
        df_excel.columns = df_excel.columns.str.strip()

        df_excel = df_excel.rename(columns={
            "Nome Item": "nome",
            "Tipo": "tipo",
            "Modelo": "modelo",
            "Quantidade": "quantidade",
            "Caixa": "caixa",
            "Localização": "localizacao",
            "Slot": "slot"
        })

        banco = crud.listar_itens()

        mapa_banco = {
            (item["nome"].strip().lower(), item["modelo"].strip().lower()): item
            for item in banco
        }

        erros = []

        for _, row in df_excel.iterrows():
            chave = (
                str(row.get("nome", "")).strip().lower(),
                str(row.get("modelo", "")).strip().lower()
            )

            qtd_excel = int(row.get("quantidade", 0))

            if chave in mapa_banco:
                qtd_banco = mapa_banco[chave]["quantidade"]

                if qtd_excel != qtd_banco:
                    erros.append({
                        "nome": chave[0],
                        "modelo": chave[1],
                        "excel": qtd_excel,
                        "banco": qtd_banco
                    })
            else:
                erros.append({
                    "nome": chave[0],
                    "modelo": chave[1],
                    "excel": qtd_excel,
                    "banco": "NÃO EXISTE"
                })

        return erros
    

def salvar_com_template(dados, caminho_template, caminho_saida):
    wb = load_workbook(caminho_template)
    ws = wb.active

    if ws is None:
        raise ValueError("Planilha não encontrada no template")

    # limpa dados antigos (mantém formatação)
    ws.delete_rows(2, ws.max_row)

    for i, item in enumerate(dados, start=2):
        ws[f"A{i}"] = item.get("nome", "")
        ws[f"B{i}"] = item.get("tipo", "")
        ws[f"C{i}"] = item.get("modelo", "")
        ws[f"D{i}"] = item.get("quantidade", 0)
        ws[f"E{i}"] = item.get("caixa", "")
        ws[f"F{i}"] = item.get("localizacao", "")
        ws[f"G{i}"] = item.get("slot", "")

    wb.save(caminho_saida)
    
