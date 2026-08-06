"""
remover_lista_dialog.py — Confirmação de remoção de item da Lista de Compras.

Mesmo padrão visual e estrutural do RemoverDialog usado no módulo de estoque.
"""

from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import pyqtSignal

from inventario.ui.theme.dialog_style import ESTILO_DIALOG


class RemoverListaDialog(QDialog):

    item_removido = pyqtSignal(int)

    def __init__(self, item: dict, parent=None):
        super().__init__(parent)
        self.item = item

        self.setWindowTitle("Remover da Lista de Compras")
        self.setFixedSize(350, 200)
        self.setStyleSheet(ESTILO_DIALOG)
        self._criar_interface()

    def _criar_interface(self):
        layout = QVBoxLayout(self)

        texto = QLabel(
            f"Deseja realmente remover este item da Lista de Compras?\n\n"
            f"Nome: {self.item.get('nome')}\n"
            f"Modelo: {self.item.get('modelo') or '—'}\n"
            f"Quantidade: {self.item.get('quantidade')}"
        )
        texto.setWordWrap(True)

        botoes = QHBoxLayout()
        self.botao_confirmar = QPushButton("Remover")
        self.botao_cancelar = QPushButton("Cancelar")

        botoes.addWidget(self.botao_cancelar)
        botoes.addWidget(self.botao_confirmar)

        layout.addWidget(texto)
        layout.addLayout(botoes)

        self.botao_confirmar.clicked.connect(self._remover)
        self.botao_cancelar.clicked.connect(self.reject)

    def _remover(self):
        self.item_removido.emit(int(self.item["id"]))
        self.accept()