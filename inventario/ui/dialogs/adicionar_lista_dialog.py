"""
adicionar_lista_dialog.py — Formulário de cadastro de item na Lista de Compras.

Serve de base para o EditarListaDialog (que herda e sobrescreve os hooks
_titulo(), _texto_botao_salvar() e _salvar()), evitando duplicar o layout.
"""

from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QSpinBox, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import pyqtSignal

from inventario.ui.theme.dialog_style import ESTILO_DIALOG
from inventario.ui.components.mensagem import Mensagem


class AdicionarListaDialog(QDialog):
    """Emite `item_adicionado` com um dict pronto para o EstoqueService."""

    item_adicionado = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self._titulo())
        self.setFixedSize(360, 420)
        self.setStyleSheet(ESTILO_DIALOG)
        self._criar_interface()

    # ─── Interface ───────────────────────────────────────────────────────

    def _criar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        titulo = QLabel(self._titulo())
        titulo.setStyleSheet("color: #0078ff; font-size: 15px; font-weight: bold;")
        layout.addWidget(titulo)

        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Nome *")
        layout.addWidget(self.campo_nome)

        self.campo_tipo = QLineEdit()
        self.campo_tipo.setPlaceholderText("Tipo")
        layout.addWidget(self.campo_tipo)

        self.campo_modelo = QLineEdit()
        self.campo_modelo.setPlaceholderText("Modelo")
        layout.addWidget(self.campo_modelo)

        self.campo_quantidade = QSpinBox()
        self.campo_quantidade.setMinimum(1)
        self.campo_quantidade.setMaximum(999999)
        self.campo_quantidade.setValue(1)
        layout.addWidget(self.campo_quantidade)

        self.campo_observacao = QLineEdit()
        self.campo_observacao.setPlaceholderText("Observação (ex: comprar urgente)")
        layout.addWidget(self.campo_observacao)

        layout.addStretch()

        botoes = QHBoxLayout()
        self.botao_cancelar = QPushButton("Cancelar")
        self.botao_cancelar.clicked.connect(self.reject)
        self.botao_salvar = QPushButton(self._texto_botao_salvar())
        self.botao_salvar.clicked.connect(self._salvar)

        botoes.addWidget(self.botao_cancelar)
        botoes.addWidget(self.botao_salvar)
        layout.addLayout(botoes)

    # ─── Hooks sobrescritos pelo EditarListaDialog ─────────────────────

    def _titulo(self) -> str:
        return "Adicionar à Lista de Compras"

    def _texto_botao_salvar(self) -> str:
        return "Salvar"

    # ─── Ações ───────────────────────────────────────────────────────────

    def _coletar_dados(self) -> dict:
        return {
            "nome": self.campo_nome.text().strip(),
            "tipo": self.campo_tipo.text().strip(),
            "modelo": self.campo_modelo.text().strip(),
            "quantidade": self.campo_quantidade.value(),
            "observacao": self.campo_observacao.text().strip(),
        }

    def _salvar(self):
        dados = self._coletar_dados()

        if not dados["nome"]:
            Mensagem.erro(self, "O campo 'Nome' é obrigatório.")
            return

        self.item_adicionado.emit(dados)
        self.accept()