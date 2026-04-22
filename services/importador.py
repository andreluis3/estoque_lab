import pandas as pd

COLUNAS_PLANILHA = {
    "Nome Equipamento": "item",
    "Tipo": "categoria",
    "Modelo": "modelo",
    "Quantidade": "quantidade",
    "Caixa": "local_caixa",
    "Localização": "descricao",
    "Slot": "local_slot"
}

def importar_excel(caminho: str) -> list[dict]:
    df = pd.read_excel(caminho)
    df = df.rename(columns=COLUNAS_PLANILHA)
    return df.to_dict(orient="records")