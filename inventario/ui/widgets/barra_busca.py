from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal


class BarraBuscaWidget(QWidget):

    buscar_clicado = pyqtSignal(str)
    texto_alterado = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.iniciar_ui()


    def iniciar_ui(self):

        self.setFixedSize(650, 60)

        print("[BarraBuscaWidget] Construindo interface...")


        self.input_busca = QLineEdit(self)

        self.input_busca.setGeometry(
            0,
            0,
            400,
            60
        )


        # quando digitar já dispara busca
        self.input_busca.textChanged.connect(
            self.emitir_texto_alterado
        )


        self.input_busca.setPlaceholderText(
            "Digite o nome do componente"
        )


        self.botao_busca = QPushButton(
            "Buscar",
            self
        )

        self.botao_busca.setGeometry(
            450,
            0,
            200,
            60
        )


        self.botao_busca.clicked.connect(
            self.emitir_busca
        )



    def emitir_busca(self):

        texto = self.input_busca.text()

        self.buscar_clicado.emit(texto)



    def emitir_texto_alterado(self, texto):

        print("[BarraBusca] Digitando:", texto)

        self.texto_alterado.emit(texto)