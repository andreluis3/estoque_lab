from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QAbstractItemView
)
from PyQt6.QtCore import Qt, QTimer

from ui.tabela_estoque import TabelaEstoque
from controllers.crud import Crud
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QLabel
from ui.dialogo_inserir import DialogoInserir
from PyQt6.QtWidgets import QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARMAZENAMENTO DE COMPONENTES - LABORATÓRIO DE EMC")
        self.resize(1000, 600)

        container = QWidget()
        layout = QVBoxLayout()  

        self.input_busca = QLineEdit()
        self.input_busca.textChanged.connect(self.filtrar_tabela)
        self.input_busca.setPlaceholderText("🔍 Buscar item...")

        layout.addWidget(self.input_busca)
        self.service = Crud()

        # tabela
        self.tabela = TabelaEstoque()
        layout.addWidget(self.tabela)

        container.setLayout(layout)
        self.setCentralWidget(container)
        self.botao_add = QPushButton("➕ Adicionar Equipamento")
        self.botao_add.clicked.connect(self.abrir_dialogo)
        layout.addWidget(self.botao_add)

    def on_item_changed(self, item): #funcao de clique
        try:
            self.tabela.blockSignals(True)

            row = item.row()
            col = item.column()

            # ID na coluna 0
            item_id = int(self.tabela.item(row, 0).text())

            colunas = ["id", "nome", "tipo", "modelo", "quantidade", "caixa", "localizacao", "slot"]

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
            
            
    def recarregar_tabela(self):
        itens = self.service.listar_itens()
        self.tabela.carregar_dados(itens)
    
    def abrir_dialogo(self):
        print("Botão clicado!")

        dialogo = DialogoInserir()

        if dialogo.exec():
            print("Dialog confirmado")

            dados = dialogo.get_dados()

            resultado = self.service.inserir_item(dados, usuario="andre")

            if resultado["status"] == "ok":
                self.recarregar_tabela()
            else:
                print("Erro:", resultado["mensagem"])