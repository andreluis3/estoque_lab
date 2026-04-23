from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QAbstractItemView
)
from PyQt6.QtCore import Qt, QTimer

from ui.tabela_estoque import TabelaEstoque
from controllers.crud import Crud
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LABSTOCK")
        self.resize(1000, 600)

        # 🔥 backend
        self.service = Crud()
        self.input_busca = QLineEdit()
        #buscar dados na tabela
        self.input_busca.setPlaceholderText("🔍 Buscar item...")
        layout.addWidget(self.input_busca)

        container = QWidget()
        layout = QVBoxLayout()

        # 👇 tabela
        self.tabela = TabelaEstoque()

        # 🔥 configurar tabela
        self.tabela.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.tabela.itemChanged.connect(self.on_item_changed)

        layout.addWidget(self.tabela)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_item_changed(self, item):
        try:
            self.tabela.blockSignals(True)

            row = item.row()
            col = item.column()

            # ID na coluna 0
            item_id = int(self.tabela.item(row, 0).text())

            colunas = ["id", "nome", "tipo", "modelo", "quantidade", "caixa", "localizacao"]

            campo = colunas[col]
            valor = item.text()

            if campo == "quantidade":
                valor = int(valor)

            dados = {campo: valor}

            resultado = self.service.atualizar_item(item_id, dados, usuario="andre")

            if resultado["status"] != "ok":
                raise ValueError(resultado["mensagem"])

            # feedback visual
            item.setBackground(Qt.GlobalColor.green)

            QTimer.singleShot(800, lambda: item.setBackground(Qt.GlobalColor.white))

        except Exception as e:
            item.setBackground(Qt.GlobalColor.red)
            print("Erro:", e)

        finally:
            self.tabela.blockSignals(False)