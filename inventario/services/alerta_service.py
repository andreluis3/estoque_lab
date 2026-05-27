import pandas as pd
from inventario.frontend_henrique.projeto.alerta import verificar_estoque


class AlertService:
    def __init__(self, estoque_service):
        self.estoque_service = estoque_service

    def get_alertas(self) -> list[str]:
        """
        Converte dados do banco em alertas de estoque baixo
        """
        itens = self.estoque_service.listar_todos_itens()

        # converter para DataFrame (compatível com lógica antiga do Henrique)
        df = pd.DataFrame(itens)

        # padronizar nomes igual ao código antigo
        df = df.rename(columns={
            "nome": "Nome Item",
            "tipo": "Tipo",
            "quantidade": "Quantidade"
        })

        return verificar_estoque(df)