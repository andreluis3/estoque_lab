from repositories.item_repository import inserir_item, listar_itens
from utils.excel_utils import exportar_para_excel


class ItemService:
    def __init__(self, crud):
        self.crud = crud

    def inserir_item(self, item, usuario=None):
        resultado = self.crud.inserir_item(item)

        if resultado["status"] == "ok":
            exportar_para_excel()

        return resultado

    def listar_itens(self):
        return self.crud.listar_itens()
    
    def buscar_item(self, texto, filtro):
        return self.crud.buscar_item(texto, filtro)
    
    def buscar_por_nome(self, nome):
        return self.crud.buscar_por_nome(nome)
    
    def buscar_por_modelo(self, modelo):
        return self.crud.buscar_por_modelo(modelo)
    
    def atualizar_item(self, item_id, dados, usuario=None):
        resultado = self.crud.atualizar_item(item_id, dados)

        if resultado["status"] == "ok":
            exportar_para_excel()

        return resultado

    def buscar_padrao_mais_comum(self, texto):
        return self.crud.buscar_padrao_mais_comum(texto)