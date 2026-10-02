# Adicionar valor
# Remover valor
# Editar valor 

def verificar_estoque(df):
    minimo_componentes = {
        "display": 2,
        "capacitor": 2,
        "baterias": 2,

        "ci": 5,
        "microcontrolador": 5,
        "transistor": 5,
        "fusivel": 5,
        "diodo": 5,
        "sd card": 5,
        "rele": 5,
        "varistor": 5,
        "led": 5,

        "resistor": 20,
    }

    itens_em_falta = []

    for _, linha in df.iterrows():
        # Pegando valores do planilha:
        nome = str(linha["Nome Item"]).lower()
        item = str(linha["Tipo"]).lower
        quantidade = int(linha["Quantidade"])
        # OBS: Verificar os valores na tabela

        minimo = None

        #print("Procurando itens:")
        
        # Primeiro procurar pelo tipo do item:
        for chave in minimo_componentes:    # Pegando a chave do dicionário
            minimo = minimo_componentes[chave]
            break

        # Caso não sejá encontrado pelo tipo, procurar pelo nome
        if minimo is None:
            for chave in minimo_componentes:
                if chave in nome:   # Verifica se a chave do dicionário está presente no nome do item
                    minimo = minimo_componentes[chave]
                    break
        
        # Verificando a quantidade:
        if minimo is not None:
            if quantidade <= minimo:
                itens_em_falta.append(
                    f"{linha['Nome Item']} está com apenas {quantidade} unidades."
                )

    print()
    print(itens_em_falta)
    return itens_em_falta