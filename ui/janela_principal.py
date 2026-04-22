from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout
)

from ui.tabela_estoque import TabelaEstoque


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LABSTOCK")
        self.resize(1000, 600)

        container = QWidget()
        layout = QVBoxLayout()

        # 👇 sua tabela
        self.tabela = TabelaEstoque()

        layout.addWidget(self.tabela)

        container.setLayout(layout)
        self.setCentralWidget(container)