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

        self.setWindowTitle("ARMAZENAMENTO DE COMPONENTES - LABORATÓRIO DE EMC")
        self.resize(1000, 600)

        container = QWidget()
        layout = QVBoxLayout()  

        self.input_busca = QLineEdit()
        self.service = Crud()
        self.input_busca.textChanged.connect(self.filtrar_tabela)
        self.input_busca.setPlaceholderText("🔍 Buscar item...")

        layout.addWidget(self.input_busca)

        # tabela
        self.tabela = TabelaEstoque()
        layout.addWidget(self.tabela)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_item_changed(self, item): #funcao de clique
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
            
    def filtrar_tabela(self, texto):
        texto = texto.lower()

        for row in range(self.tabela.rowCount()):
            mostrar = False

            for col in range(self.tabela.columnCount()):
                item = self.tabela.item(row, col)

                if item and texto in item.text().lower():
                    mostrar = True
                    break

            self.tabela.setRowHidden(row, not mostrar)