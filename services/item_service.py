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