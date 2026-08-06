from PyQt6.QtWidgets import QDialog, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

class PopupAlertaWidget(QDialog):
    saiba_mais_clicado = pyqtSignal()

    def __init__(self, quantidade_alertas, parent=None):
        super().__init__(parent)
        self.quantidade_alertas = quantidade_alertas
        self.iniciar_ui()

    def iniciar_ui(self):
        self.setFixedSize(350, 160)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setStyleSheet("""
            background-color: #1e1e1e;
            border-radius: 15px;
            color: white;
        """)

        self.label = QLabel(f"⚠ {self.quantidade_alertas} itens com estoque baixo", self)
        self.label.setGeometry(15, 35, 320, 40) # Ajustado margem esquerda interna para não cortar texto
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")

        self.botao = QPushButton("Saiba mais", self)
        self.botao.setGeometry(100, 90, 150, 45)
        self.botao.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)
        print("[PopupAlertaWidget] Construindo interface...")
        self.botao.clicked.connect(self.acao_saiba_mais)
        QTimer.singleShot(10000, self.close)

    def acao_saiba_mais(self):
        self.close()
        self.saiba_mais_clicado.emit()