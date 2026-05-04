

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QAbstractItemView
)
from PyQt6.QtCore import Qt, QTimer

from PyQt6.QtWidgets import QMessageBox

from ui.tabela_estoque import TabelaEstoque
from controllers.crud import Crud
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QLabel
from ui.dialogo_inserir import DialogoInserir
from PyQt6.QtWidgets import QPushButton
from services.importador import importar_para_banco
from services.importador import gerar_relatorio_inconsistencias

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
        
    def tratar_erro(self, erro):
        print("ERRO:", erro)
        self.mostrar_erro(str(erro))
        
    def on_item_changed(self, item):
        try:
            self.tabela.blockSignals(True)

            if item is None:
                return

            row = item.row()
            col = item.column()

            item_id_widget = self.tabela.item(row, 0)
            if item_id_widget is None:
                return

            item_id = int(item_id_widget.text())

            colunas = ["id", "nome", "tipo", "modelo", "quantidade", "caixa", "localizacao", "slot"]

            campo = colunas[col]
            valor = item.text().strip()

            # ❌ não permitir vazio
            if not valor:
                self.mostrar_erro(f"O campo '{campo}' não pode ser vazio")
                self.carregar_tabela()
                return

            # 🔢 valida quantidade
            if campo == "quantidade":
                if not valor.isdigit():
                    self.mostrar_erro("Quantidade deve ser número inteiro positivo")
                    self.carregar_tabela()
                    return

                valor = int(valor)

                if valor < 0:
                    self.mostrar_erro("Quantidade não pode ser negativa")
                    self.carregar_tabela()
                    return

            dados = {campo: valor}

            resultado = self.crud.atualizar_item(item_id, dados, usuario="andre")

            if resultado["status"] != "ok":
                raise ValueError(resultado["mensagem"])

            item.setBackground(Qt.GlobalColor.green)
            print(f"✅ Item {item_id} atualizado: {campo} = {valor}")  # DEBUG

            # 🔄 Recarregar tabela para refletir mudanças
            self.carregar_tabela()

        except Exception as e:
            if item:
                item.setBackground(Qt.GlobalColor.red)
            self.tratar_erro(e)

        finally:
            self.tabela.blockSignals(False)
            
    def filtrar_tabela(self, texto):
        for row in range(self.tabela.rowCount()):
            match = False

            for col in range(self.tabela.columnCount()):
                item = self.tabela.item(row, col)

                if item:
                    valor = item.text()
                    match = True
                    break
                    
            self.tabela.setRowHidden(row, not match)
            
    
    def abrir_dialogo(self):
        print("Botão clicado!")

        dialogo = DialogoInserir(self.crud)

        if dialogo.exec():
            self.carregar_tabela()
            
    def carregar_tabela(self):
        itens = self.crud.listar_itens()
        self.tabela.carregar_dados(itens)   
        
    def recarregar_dados(self):
        caminho = "planilhas/estoque_lab_completa.xlsx"

        self.btn_recarregar.setEnabled(False)
        self.btn_recarregar.setText("⏳ Sincronizando...")

        from services.sincronizador import sincronizar_planilha_banco
        sincronizar_planilha_banco(caminho)

        self.carregar_tabela()

        from services.importador import validar_diferencas
        erros = validar_diferencas(caminho)

        self.mostrar_inconsistencias(erros)

        self.btn_recarregar.setEnabled(True)
        self.btn_recarregar.setText("🔄 Sincronizar Planilha")
        
    def mostrar_erro(self, mensagem):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erro")
        msg.setText("Ocorreu um erro no sistema")
        msg.setInformativeText(mensagem)
        msg.exec()
        
    def mostrar_sucesso(self, mensagem):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Sucesso")
        msg.setText(mensagem)
        msg.exec()
        
    def mostrar_inconsistencias(self, erros):
        if not erros:
            self.mostrar_sucesso("✅ Banco sincronizado com a planilha!")
            return

        texto = ""

        for erro in erros[:15]:
            texto += (
                f"Item: {erro['nome']}\n"
                f"Modelo: {erro['modelo']}\n"
                f"Excel: {erro['excel']} | Banco: {erro['banco']}\n"
                "------------------------\n"
            )

        if len(erros) > 15:
            texto += f"\n... e mais {len(erros) - 15} inconsistências"

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Inconsistências encontradas")
        msg.setText("⚠️ Diferenças entre planilha e banco")
        msg.setDetailedText(texto)
        msg.exec()