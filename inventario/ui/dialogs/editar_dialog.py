"""
editar_dialog.py — Formulário completo de edição de item do estoque.

Segue o mesmo padrão visual do AdicionarDialog. Recebe o item já selecionado
na tabela e pré-preenche todos os campos.
"""

from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QSpinBox, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import pyqtSignal


class EditarDialog(QDialog):

    item_editado = pyqtSignal(dict)

    def __init__(self, item: dict, parent=None):
        super().__init__(parent)
        self.item = item

        self.configurar_janela()
        self.criar_interface()

    # ─── Janela ──────────────────────────────────────────────────────────

    def configurar_janela(self):
        self.setWindowTitle(f"Editar item — {self.item.get('nome', '')}")
        self.setFixedSize(350, 480)

        self.setStyleSheet("""
            QDialog {
                background-color:#111111;
                color:white;
            }
            QLabel {
                color:white;
                font-size: 12px;
            }
            QLineEdit,
            QSpinBox {
                background:#222222;
                color:white;
                border:1px solid #0078ff;
                border-radius: 4px;
                padding:6px;
            }
            QPushButton {
                background:#0078ff;
                color:white;
                border-radius:8px;
                padding:8px;
                font-weight: 500;
            }
            QPushButton:hover {
                background:#005ed1;
            }
        """)

    # ─── Interface ───────────────────────────────────────────────────────

    def criar_interface(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        self.nome = self._campo_texto(layout, "Nome", self.item.get("nome", ""))
        self.tipo = self._campo_texto(layout, "Tipo", self.item.get("tipo", ""))
        self.modelo = self._campo_texto(layout, "Modelo", self.item.get("modelo", ""))

        layout.addWidget(QLabel("Quantidade"))
        self.quantidade = QSpinBox()
        self.quantidade.setMinimum(0)
        self.quantidade.setMaximum(999999)
        self.quantidade.setValue(int(self.item.get("quantidade", 0)))
        layout.addWidget(self.quantidade)

        self.caixa = self._campo_texto(layout, "Caixa", self.item.get("caixa", ""))
        self.localizacao = self._campo_texto(layout, "Localização", self.item.get("localizacao", ""))
        self.slot = self._campo_texto(layout, "Slot", self.item.get("slot", ""))

        self.botao_salvar = QPushButton("💾 Salvar alterações")
        self.botao_salvar.clicked.connect(self.salvar)
        layout.addWidget(self.botao_salvar)

    def _campo_texto(self, layout, label: str, valor_atual: str) -> QLineEdit:
        layout.addWidget(QLabel(label))
        campo = QLineEdit(str(valor_atual) if valor_atual is not None else "")
        layout.addWidget(campo)
        return campo

    # ─── Ações ───────────────────────────────────────────────────────────

    def salvar(self):
        if not self.nome.text().strip():
            QMessageBox.warning(self, "Erro", "O campo 'Nome' é obrigatório.")
            return

        if not self.modelo.text().strip():
            QMessageBox.warning(self, "Erro", "O campo 'Modelo' é obrigatório.")
            return

        dados = {
            "id": self.item["id"],
            "nome": self.nome.text().strip(),
            "tipo": self.tipo.text().strip(),
            "modelo": self.modelo.text().strip(),
            "quantidade": self.quantidade.value(),
            "caixa": self.caixa.text().strip(),
            "localizacao": self.localizacao.text().strip(),
            "slot": self.slot.text().strip(),
        }

        self.item_editado.emit(dados)
        self.accept()