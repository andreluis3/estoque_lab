from PyQt6.QtWidgets import (
    QDialog,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QSpinBox
)

from PyQt6.QtCore import pyqtSignal


class EditarDialog(QDialog):

    item_editado = pyqtSignal(dict)


    def __init__(self, item, parent=None):

        super().__init__(parent)

        self.item = item

        self.setWindowTitle(
            "Editar item"
        )

        self.setFixedSize(
            350,
            350
        )

        self.criar_interface()


    def criar_interface(self):

        layout = QVBoxLayout(self)


        self.nome = QLineEdit(
            self.item.get("nome","")
        )


        self.quantidade = QSpinBox()

        self.quantidade.setValue(
            self.item.get(
                "quantidade",
                0
            )
        )


        self.botao_salvar = QPushButton(
            "Salvar alterações"
        )


        layout.addWidget(
            self.nome
        )

        layout.addWidget(
            self.quantidade
        )

        layout.addWidget(
            self.botao_salvar
        )


        self.botao_salvar.clicked.connect(
            self.salvar
        )


    def salvar(self):

        dados = {

            "id": self.item["id"],

            "nome": self.nome.text(),

            "quantidade":
                self.quantidade.value()

        }


        self.item_editado.emit(
            dados
        )

        self.accept()