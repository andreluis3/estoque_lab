from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout
)

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMessageBox

class AdicionarDialog(QDialog):

    item_adicionado = pyqtSignal(dict)


    def __init__(self, parent=None):
        super().__init__(parent)

        self.configurar_janela()
        self.criar_interface()


    def configurar_janela(self):

        self.setWindowTitle(
            "Adicionar item"
        )

        self.setFixedSize(
            350,
            450
        )


        self.setStyleSheet("""
            QDialog {
                background-color:#111111;
                color:white;
            }

            QLabel {
                color:white;
            }

            QLineEdit,
            QSpinBox {
                background:#222222;
                color:white;
                border:1px solid #0078ff;
                padding:5px;
            }

            QPushButton {
                background:#0078ff;
                color:white;
                border-radius:8px;
                padding:8px;
            }

            QPushButton:hover {
                background:#005ed1;
            }
        """)


    def criar_interface(self):

        layout = QVBoxLayout(self)


        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Nome")


        self.tipo = QLineEdit()
        self.tipo.setPlaceholderText("Tipo")


        self.modelo = QLineEdit()
        self.modelo.setPlaceholderText("Modelo")


        self.quantidade = QSpinBox()
        self.quantidade.setMinimum(1)


        self.caixa = QLineEdit()
        self.caixa.setPlaceholderText("Caixa")


        self.localizacao = QLineEdit()
        self.localizacao.setPlaceholderText("Localização")


        self.slot = QLineEdit()
        self.slot.setPlaceholderText("Slot")


        self.botao_salvar = QPushButton(
            "Salvar"
        )


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


        layout.addWidget(
            self.botao_salvar
        )


        self.botao_salvar.clicked.connect(
            self.salvar
        )


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
        
        if not self.quantidade.value() > 0:
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


        self.item_adicionado.emit(
            dados
        )

        self.accept()