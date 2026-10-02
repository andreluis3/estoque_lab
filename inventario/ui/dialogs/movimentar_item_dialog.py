from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

from PyQt6.QtCore import pyqtSignal

from inventario.ui.widgets.quantidade_spinbox import QuantidadeSpinBox
from inventario.ui.theme.dialog_style import ESTILO_DIALOG


class MovimentarItemDialog(QDialog):
    """
    Dialog responsável pela movimentação de estoque.

    Recebe um item selecionado da tabela e permite:
    - adicionar quantidade
    - remover quantidade

    Não acessa banco diretamente.
    A comunicação será feita pela TelaHenriquePage/Service.
    """

    adicionar_quantidade = pyqtSignal(int, int)
    remover_quantidade = pyqtSignal(int, int)

    def __init__(self, item, parent=None):
        super().__init__(parent)

        self.item = item

        self.configurar_janela()
        self.criar_interface()

    def configurar_janela(self):
        self.setWindowTitle("Movimentar item")
        self.setFixedSize(350, 250)

        self.setStyleSheet(ESTILO_DIALOG)

    def criar_interface(self):
        layout = QVBoxLayout(self)

        nome = self.item.get(
            "nome",
            "Sem nome"
        )

        quantidade = self.item.get(
            "quantidade",
            0
        )

        self.label_item = QLabel(
            f"Item: {nome}"
        )

        self.label_quantidade = QLabel(
            f"Quantidade atual: {quantidade}"
        )

        self.quantidade_input = QuantidadeSpinBox(
            minimum=1,
            maximum=99999,
            value=1
        )

        botoes = QHBoxLayout()

        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_remover = QPushButton("Remover")

        botoes.addWidget(self.botao_adicionar)
        botoes.addWidget(self.botao_remover)

        layout.addWidget(self.label_item)
        layout.addWidget(self.label_quantidade)
        layout.addWidget(QLabel("Quantidade:"))
        layout.addWidget(self.quantidade_input)
        layout.addLayout(botoes)

        self.botao_adicionar.clicked.connect(
            self.adicionar
        )

        self.botao_remover.clicked.connect(
            self.remover
        )

    def adicionar(self):
        quantidade = self.quantidade_input.value()

        item_id = int(
            self.item["id"]
        )

        self.adicionar_quantidade.emit(
            item_id,
            quantidade
        )

        self.accept()

    def remover(self):
        quantidade = self.quantidade_input.value()

        item_id = int(
            self.item["id"]
        )

        self.remover_quantidade.emit(
            item_id,
            quantidade
        )

        self.accept()