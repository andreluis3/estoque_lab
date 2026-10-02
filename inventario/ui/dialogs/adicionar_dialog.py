from PyQt6.QtWidgets import (
    QDialog,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QMessageBox
)

from PyQt6.QtCore import pyqtSignal

from inventario.ui.widgets.quantidade_spinbox import QuantidadeSpinBox
from inventario.ui.theme.dialog_style import ESTILO_DIALOG


class AdicionarDialog(QDialog):
    item_adicionado = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.configurar_janela()
        self.criar_interface()

    def configurar_janela(self):
        self.setWindowTitle("Adicionar item")
        self.setFixedSize(350, 450)

        self.setStyleSheet(ESTILO_DIALOG)

    def criar_interface(self):
        layout = QVBoxLayout(self)

        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Nome")

        self.tipo = QLineEdit()
        self.tipo.setPlaceholderText("Tipo")

        self.modelo = QLineEdit()
        self.modelo.setPlaceholderText("Modelo")

        self.quantidade = QuantidadeSpinBox(
            minimum=1,
            maximum=99,
            value=1
        )

        self.caixa = QLineEdit()
        self.caixa.setPlaceholderText("Caixa")

        self.localizacao = QLineEdit()
        self.localizacao.setPlaceholderText("Localização")

        self.slot = QLineEdit()
        self.slot.setPlaceholderText("Slot")

        self.botao_salvar = QPushButton("Salvar")

        campos = [
            self.nome,
            self.tipo,
            self.modelo,
            self.quantidade,
            self.caixa,
            self.localizacao,
            self.slot
        ]

        for campo in campos:
            layout.addWidget(campo)

        layout.addWidget(self.botao_salvar)

        self.botao_salvar.clicked.connect(self.salvar)

    def salvar(self):
        if not self.nome.text().strip():
            QMessageBox.warning(
                self,
                "Erro",
                "O campo 'Nome' é obrigatório."
            )
            return

        if not self.modelo.text().strip():
            QMessageBox.warning(
                self,
                "Erro",
                "O campo 'Modelo' é obrigatório."
            )
            return

        if self.quantidade.value() <= 0:
            QMessageBox.warning(
                self,
                "Erro",
                "A quantidade deve ser maior que zero."
            )
            return

        dados = {
            "nome": self.nome.text(),
            "tipo": self.tipo.text(),
            "modelo": self.modelo.text(),
            "quantidade": self.quantidade.value(),
            "caixa": self.caixa.text(),
            "localizacao": self.localizacao.text(),
            "slot": self.slot.text()
        }

        self.item_adicionado.emit(dados)
        self.accept()