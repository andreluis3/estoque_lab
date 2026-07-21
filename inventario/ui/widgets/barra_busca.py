from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal

class BarraBuscaWidget(QWidget):
    # Sinal emitido para que a Controller/Page capture o termo pesquisado sem acoplar a lógica aqui
    buscar_clicado = pyqtSignal(str)
    texto_alterado = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.iniciar_ui()

    def iniciar_ui(self):
        self.setFixedSize(650, 60) # Largura do input (400) + espaço + largura do botão (200)
        print("[BarraBuscaWidget] Construindo interface...")
        # Input de texto
        self.input_busca = QLineEdit(self)
        self.input_busca.setGeometry(0, 0, 400, 60)
        #self.input_busca.textChanged.connect(self.emitir_texto_alterado)
        self.input_busca.setPlaceholderText("Digite o nome do componente")
        self.input_busca.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                font-size: 18px;
                border-radius: 15px;
                padding-left: 18px;
                border: 2px solid #2d2d2d;
            }
            QLineEdit:focus {
                border: 2px solid #0078ff;
            }
        """)
   

        # Botão Buscar
        self.botao_busca = QPushButton("Buscar", self)
        self.botao_busca.setGeometry(450, 0, 200, 60)
        self.botao_busca.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                font-size: 20px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)
        self.botao_busca.clicked.connect(self.emitir_busca)

    def emitir_busca(self):

        texto = self.input_busca.text()

        print("="*50)
        print("[BarraBusca]")
        print(f"Texto pesquisado: {texto}")
        print("="*50)

        self.buscar_clicado.emit(texto)