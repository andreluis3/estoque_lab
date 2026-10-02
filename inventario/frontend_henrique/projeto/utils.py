# Eduarda IGBRAS - Ligou para o Marcelo

import pandas as pd
import os
import re

def limpar_nome(nome):  # Apenas limapa os dados
    nome = str(nome).strip()    # Remove espaços
    nome = re.sub(r'[\\/*?:"<>|]', "", nome)    # Remoce caracteres indesejados
    nome = nome.replace(" ", "_")
    return nome

def separar_por_tipo(df, pasta_base="Inventario_Organizado"):
    # Gera uma pasta e uma planilha para cada tipo de item

    #caminho_nova_pasta = e
    os.makedirs(pasta_base, exist_ok=True)  # Cria a pasta

    for tipo, grupo in df.groupby("Tipo"):  # Agrupa pelo tipo do item
        tipo_limpo = limpar_nome(tipo)

        pasta_tipo = os.path.join(pasta_base, tipo_limpo)   # Cria o caminho
        os.makedirs(pasta_tipo, exist_ok=True)  # Cria una pasta para cada tipo de dado

        # Gerando novas planilhas:
        caminho_arquivo = os.path.join(
            pasta_tipo,             # Caminho
            f"{tipo_limpo}.xlsx"    # Arquivo
        )

        grupo.to_excel(caminho_arquivo, index=False)

        print(f"Arquivo criado: {caminho_arquivo}")

def buscar_item(df, nome):
    return df[df["Nome Item"].str.contains(nome, case=False, na=False)]

def estoque_baixo(df, minimo=5):
    # Para caso tenha poucas unidades
    return df[df["Quantidade"] < minimo]