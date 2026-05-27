from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ui.tabela_estoque import TabelaEstoque


class TelaEstoque(QWidget):
    def __init__(self, service):
        super().__init__()

        self.service = service

        self.layout = QVBoxLayout(self)

        # SUA TABELA (widget que você já tem)
        self.tabela = TabelaEstoque()

        self.layout.addWidget(self.tabela)

        self.carregar_dados()

    def carregar_dados(self):
        itens = self.service.listar_itens()
        self.tabela.carregar_dados(itens)