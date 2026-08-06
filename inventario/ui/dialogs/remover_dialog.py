from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

from PyQt6.QtCore import pyqtSignal


class RemoverDialog(QDialog):

    item_removido = pyqtSignal(int)


    def __init__(self, item, parent=None):

        super().__init__(parent)

        self.item = item

        self.setWindowTitle(
            "Remover item"
        )

        self.setFixedSize(
            350,
            200
        )

        self.criar_interface()


    def criar_interface(self):

        layout = QVBoxLayout(self)


        texto = QLabel(
            f"Tem certeza que deseja deletar este item?\n\n"
            f"Nome: {self.item.get('nome')}\n"
            f"Modelo: {self.item.get('modelo')}\n"
            f"Quantidade: {self.item.get('quantidade')}\n\n"
            f"Essa ação não pode ser desfeita."
        )


        botoes = QHBoxLayout()


        self.confirmar = QPushButton(
            "Sim, deletar"
        )


        self.cancelar = QPushButton(
            "Cancelar"
        )


        botoes.addWidget(
            self.confirmar
        )

        botoes.addWidget(
            self.cancelar
        )


        layout.addWidget(
            texto
        )

        layout.addLayout(
            botoes
        )


        self.confirmar.clicked.connect(
            self.remover
        )


        self.cancelar.clicked.connect(
            self.reject
        )


    def remover(self):

        self.item_removido.emit(
            int(self.item["id"])
        )

        self.accept()