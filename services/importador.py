import pandas as pd

COLUNAS_PLANILHA = {
    "Tipo": "categoria",
    "Nome Equipamento": "item",
    "Modelo": "modelo",
    "Quantidade": "quantidade",
    "Caixa": "local_caixa",
    "Slot": "local_slot",
    "Localização": "descricao"
}

def importar_excel(caminho: str) -> list[dict]:
    df = pd.read_excel(caminho)

    # Renomeia colunas
    df = df.rename(columns=COLUNAS_PLANILHA)

    # Garante que todas existam
    for col in COLUNAS_PLANILHA.values():
        if col not in df.columns:
            df[col] = None

    # Limpeza básica
    df["categoria"] = df["categoria"].fillna("Outros")
    df["item"] = df["item"].fillna("").str.strip()
    df["modelo"] = df["modelo"].fillna("").str.strip()
    df["quantidade"] = df["quantidade"].fillna(0).astype(int)

    # Ordem final das colunas
    ordem = [
        "categoria",
        "item",
        "modelo",
        "quantidade",
        "local_caixa",
        "local_slot",
        "descricao"
    ]

    df = df[ordem]

    return df.to_dict(orient="records")