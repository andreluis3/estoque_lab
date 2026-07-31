

LINK_SERVIDOR = ('SERVIDOR = r"I:\LGE\operacao\Areas\CEM\software\EstoqueLab"')
link_local = ('LOCAL = r"C:\Users\Public\Documents\EstoqueLab"')

class ExportService:

    def exportar_estoque_excel(self):

        itens = self.item_repository.listar()

        gerar_excel(itens)

        return caminho_arquivo