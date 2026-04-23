from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
)


class DialogoInserir(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adicionar Equipamento")

        layout = QVBoxLayout()

        self.nome = QLineEdit()
        self.tipo = QLineEdit()
        self.modelo = QLineEdit()
        self.quantidade = QLineEdit()
        self.caixa = QLineEdit()
        self.localizacao = QLineEdit()
        self.slot = QLineEdit()

        self.botao_salvar = QPushButton("Salvar")

        self.botao_salvar.clicked.connect(self.accept)

        layout.addWidget(self.nome)
        layout.addWidget(self.tipo)
        layout.addWidget(self.modelo)
        layout.addWidget(self.quantidade)
        layout.addWidget(self.caixa)
        layout.addWidget(self.localizacao)
        layout.addWidget(self.slot)
        layout.addWidget(self.botao_salvar)

        self.setLayout(layout)

    def get_dados(self):
        return {
            "nome": self.nome.text(),
            "tipo": self.tipo.text(),
            "modelo": self.modelo.text(),
            "quantidade": int(self.quantidade.text() or 0),
            "caixa": self.caixa.text(),
            "localizacao": self.localizacao.text(),
            "slot": self.slot.text()
        }