from dataclasses import dataclass

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