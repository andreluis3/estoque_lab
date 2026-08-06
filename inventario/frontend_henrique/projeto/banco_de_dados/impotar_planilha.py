# Impotar a planilha
# Ler e separar os dados por tipo
# criar uma arquivo para cada tipo

import pandas as pd
import os

"""Este módulo importa a planilha le os dados e separa em planilhas menores de acordo com o tipo do item."""

def dados():
    # Le a planilha e separa os dados peço tipo do item
    ...

# Lendo o arquivo principal
arquivo = r"C:\Users\Henrique\Documents\IPT\Projetos\Inventario\Meu projeto\planilhas\estoque_lab_completa.xlsx"   # Arquivo original
df = pd.read_excel(arquivo, header=1) # Le arquivo excel
# header=0  diz para o Pandas que a linha 0 é cabeçalho

df = df.dropna(how= "all")  # Remove as linhas vazias

print("Abrindo aquivo Excel")
print()

print(df.head())
print(df.columns)

print()
print("Planilha lida com sucesso.")

# Separando pelo tipo do item:
print("Separando itens.")
pasta_base = "Inventario_Organizado"

os.makedirs(pasta_base, exist_ok= True) # Cria a pasta

for tipo, grupo in df.grupby("Tipo"):  
     # Agrupa pelo tipo do item
    pasta_tipo = os.path.join(pasta_base, tipo) # Cria o nome pasta para cada tipo dentro de pasta_base
    os.makedirs(pasta_tipo, exist_ok= True)

    caminho_arquivo = os.path.join(pasta_tipo, f"{tipo}.xlsx")
    grupo.to_excel(caminho_arquivo, index=  False)
    print(f"Pasta {tipo} criada em: {caminho_arquivo}")

#print("Itens separados")