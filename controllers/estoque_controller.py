from controllers.crud import Crud
from services.importador import importar_para_banco, validar_diferencas


class EstoqueController:
    def __init__(self):
        self.crud = Crud()

    def importar_planilha(self, caminho):
        sucesso = importar_para_banco(caminho)

        if not sucesso:
            return {"status": "erro", "mensagem": "Erro na importação"}

        erros = validar_diferencas(caminho)

        return {
            "status": "ok",
            "erros": erros
        }