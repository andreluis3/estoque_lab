from dataclasses import dataclass
from collections import Counter

def ordenar_por_importancia(itens):
    contagem = Counter(i["categoria"] for i in itens)

    return sorted(
        itens,
        key=lambda x: (-contagem[x["categoria"]], x["categoria"])
    )

@dataclass
class Item:
    id: int
    item: str
    modelo: str
    categoria: str
    quantidade: int
    local_caixa: str
    local_slot: str
    descricao: str
    status: str = ""