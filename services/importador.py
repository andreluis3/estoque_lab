import pandas as pd
from controllers.crud import Crud
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


def importar_excel(caminho: str) -> list[dict]:
    df = pd.read_excel(caminho)

    print("PRIMEIRA LINHA DO DF:")
    print(df.iloc[0])

    print("COLUNAS BRUTAS DO EXCEL:")
    print(list(df.columns))

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


def importar_para_banco(caminho):
    crud = Crud()

    dados = importar_excel(caminho)

    for item in dados:
        resultado = crud.inserir_item(item)

        if resultado["status"] != "ok":
            print("Erro ao inserir:", resultado["mensagem"])

    print("Importação concluída!")
    
def recarregar_dados(self):
    caminho = "planilhas/estoque_lab_completa.xlsx"

    importar_para_banco(caminho)

    crud = Crud()
    itens = crud.listar_itens()

    self.tabela.carregar_dados(itens)
    
from openpyxl import load_workbook

def salvar_com_template(dados, caminho_template, caminho_saida):
    wb = load_workbook(caminho_template)
    ws = wb.active

    # limpa dados antigos (mantém formatação)
    ws.delete_rows(2, ws.max_row)

    for i, item in enumerate(dados, start=2):
        ws[f"A{i}"] = item["nome"]
        ws[f"B{i}"] = item["tipo"]
        ws[f"C{i}"] = item["modelo"]
        ws[f"D{i}"] = item["quantidade"]
        ws[f"E{i}"] = item["caixa"]
        ws[f"F{i}"] = item["localizacao"]
        ws[f"G{i}"] = item["slot"]

    wb.save(caminho_saida)