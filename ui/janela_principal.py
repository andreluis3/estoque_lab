

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QAbstractItemView
)
from PyQt6.QtCore import Qt, QTimer

from ui.tabela_estoque import TabelaEstoque
from controllers.crud import Crud
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QLabel
from ui.dialogo_inserir import DialogoInserir
from PyQt6.QtWidgets import QPushButton
from services.importador import importar_para_banco


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 

        self.setWindowTitle("ARMAZENAMENTO DE COMPONENTES - LABORATÓRIO DE EMC")
        self.resize(1000, 600)

        # ✅ ORDEM CORRETA
        self.crud = Crud()


        container = QWidget()
        layout = QVBoxLayout()

        # 🔍 BUSCA
        self.input_busca = QLineEdit()
        self.input_busca.setPlaceholderText("🔍 Buscar item...")
        self.input_busca.textChanged.connect(self.filtrar_tabela)
        layout.addWidget(self.input_busca)

        # 📦 TABELA
        self.tabela = TabelaEstoque()
        layout.addWidget(self.tabela)

        # ➕ BOTÃO ADD
        self.botao_add = QPushButton("➕ Adicionar Equipamento")
        self.botao_add.clicked.connect(self.abrir_dialogo)
        layout.addWidget(self.botao_add)

        # 🔄 RELOAD
        self.btn_recarregar = QPushButton("🔄 Recarregar Planilha")
        self.btn_recarregar.clicked.connect(self.recarregar_dados)
        layout.addWidget(self.btn_recarregar)

        container.setLayout(layout)
        self.setCentralWidget(container)

        self.carregar_tabela()
        
 
        
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

            resultado = self.crud.atualizar_item(item_id, dados, usuario="andre")

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
        for row in range(self.tabela.rowCount()):
            match = False

            for col in range(self.tabela.columnCount()):
                item = self.tabela.item(row, col)

                if item and texto.lower() in item.text().lower():
                    match = True
                    break
                    
            self.tabela.setRowHidden(row, not match)
            
    
    def abrir_dialogo(self):
        print("Botão clicado!")

        dialogo = DialogoInserir(self.service)

        if dialogo.exec():
            self.carregar_tabela()
            
    def carregar_tabela(self):
        itens = self.crud.listar_itens()
        self.tabela.carregar_dados(itens)   
        
    def recarregar_dados(self):
        caminho = "planilhas/estoque_lab_completa.xlsx"
        importar_para_banco(caminho)
        self.carregar_tabela() 