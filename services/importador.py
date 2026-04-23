import pandas as pd
from controllers.crud import Crud


# 🔥 MAPEAMENTO CORRETO (ALINHADO COM SEU BANCO)
COLUNAS_PLANILHA = {
    "Nome Item": "nome",
    "Tipo": "tipo",
    "Modelo": "modelo",
    "Quantidade": "quantidade",
    "Caixa": "caixa",
    "Localização": "localizacao"
    # "Slot" ignorado por enquanto
}


def importar_excel(caminho: str) -> list[dict]:
    df = pd.read_excel(caminho)

    print("PRIMEIRA LINHA DO DF:")
    print(df.iloc[0])

    print("COLUNAS BRUTAS DO EXCEL:")
    print(list(df.columns))

    # limpar nomes
    df.columns = df.columns.str.strip()

    # renomear
    df = df.rename(columns=COLUNAS_PLANILHA)

    # garantir colunas obrigatórias
    for col in COLUNAS_PLANILHA.values():
        if col not in df.columns:
            df[col] = None

    # 🔥 LIMPEZA E PADRONIZAÇÃO
    df["nome"] = df["nome"].fillna("").astype(str).str.strip()
    df["tipo"] = df["tipo"].fillna("Outros").astype(str).str.strip()
    df["modelo"] = df["modelo"].fillna("").astype(str).str.strip()
    df["quantidade"] = df["quantidade"].fillna(0).astype(int)
    df["caixa"] = df["caixa"].fillna("").astype(str).str.strip()
    df["localizacao"] = df["localizacao"].fillna("").astype(str).str.strip()

    # ordem final
    ordem = ["nome", "tipo", "modelo", "quantidade", "caixa", "localizacao"]
    df = df[ordem]

    print("COLUNAS RENOMEADAS:")
    print(list(df.columns))

    return df.to_dict(orient="records")


# 🔥 AGORA USANDO SEU CRUD (CORRETO)
def importar_para_banco(caminho):
    crud = Crud()

    dados = importar_excel(caminho)

    for item in dados:
        resultado = crud.inserir_item(item)

        if resultado["status"] != "ok":
            print("Erro ao inserir:", resultado["mensagem"])

    print("Importação concluída!")