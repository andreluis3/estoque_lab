from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer

from ui.tabela_estoque import TabelaEstoque
from ui.dialogo_inserir import DialogoInserir
from ui.tela_historico import TelaHistorico
from controllers.crud import Crud


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARMAZENAMENTO DE COMPONENTES - LABORATÓRIO DE EMC")
        self.resize(1100, 650)

        self.crud = Crud()

        container = QWidget()
        layout = QVBoxLayout()

        # ── Busca ──────────────────────────────────────────────────────────
        self.input_busca = QLineEdit()
        self.input_busca.setPlaceholderText("🔍 Buscar por nome, tipo, modelo...")
        self.input_busca.textChanged.connect(self.filtrar_tabela)
        layout.addWidget(self.input_busca)

        # ── Tabela ─────────────────────────────────────────────────────────
        self.tabela = TabelaEstoque()
        self.tabela.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.tabela)

        # ── Botões ─────────────────────────────────────────────────────────
        botoes = QHBoxLayout()

        self.botao_add = QPushButton("➕ Adicionar Equipamento")
        self.botao_add.clicked.connect(self.abrir_dialogo)

        self.btn_recarregar = QPushButton("🔄 Recarregar Banco")
        self.btn_recarregar.clicked.connect(self.carregar_tabela)

        self.btn_historico = QPushButton("📋 Ver Histórico")
        self.btn_historico.clicked.connect(self.abrir_historico)

        botoes.addWidget(self.botao_add)
        botoes.addWidget(self.btn_recarregar)
        botoes.addWidget(self.btn_historico)
        layout.addLayout(botoes)

        # ── Status ─────────────────────────────────────────────────────────
        self.label_status = QLabel("")
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_status)

        container.setLayout(layout)
        self.setCentralWidget(container)

        self.carregar_tabela()

    # ── Tabela ─────────────────────────────────────────────────────────────

    def carregar_tabela(self):
        itens = self.crud.listar_itens()
        self.tabela.blockSignals(True)
        self.tabela.carregar_dados(itens)
        self.tabela.blockSignals(False)
        self.label_status.setText(f"{len(itens)} itens carregados")

    def filtrar_tabela(self, texto):
        """Filtra linhas da tabela conforme o texto digitado na busca."""
        texto = texto.strip().lower()
        for row in range(self.tabela.rowCount()):
            match = False
            for col in range(self.tabela.columnCount()):
                item = self.tabela.item(row, col)
                if item and texto in item.text().lower():
                    match = True
                    break
            self.tabela.setRowHidden(row, not match)

    def on_item_changed(self, item):
        """Edição inline de célula na tabela — salva direto no banco."""
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

            # ID não pode ser editado
            if campo == "id":
                return

            valor = item.text().strip()

            if not valor:
                self._mostrar_erro(f"O campo '{campo}' não pode estar vazio.")
                self.carregar_tabela()
                return

            if campo == "quantidade":
                if not valor.isdigit():
                    self._mostrar_erro("Quantidade deve ser um número inteiro positivo.")
                    self.carregar_tabela()
                    return
                valor = int(valor)

            resultado = self.crud.atualizar_item(item_id, {campo: valor}, usuario="andre")

            if resultado["status"] == "ok":
                item.setBackground(Qt.GlobalColor.green)
                QTimer.singleShot(800, self.carregar_tabela)
                self.label_status.setText(f"✅ Campo '{campo}' atualizado.")
            else:
                self._mostrar_erro(resultado["mensagem"])
                self.carregar_tabela()

        except Exception as e:
            self._mostrar_erro(str(e))
            self.carregar_tabela()
        finally:
            self.tabela.blockSignals(False)

    # ── Diálogo de inserção ────────────────────────────────────────────────

    def abrir_dialogo(self):
        """Abre o dialog para adicionar um novo item ao banco."""
        dialogo = DialogoInserir(self.crud)
        if dialogo.exec():
            self.carregar_tabela()
            self.label_status.setText("✅ Item adicionado com sucesso.")

    # ── Histórico ──────────────────────────────────────────────────────────

    def abrir_historico(self):
        tela = TelaHistorico(self.crud)
        tela.exec()

    # ── Mensagens ──────────────────────────────────────────────────────────

    def _mostrar_erro(self, mensagem: str):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erro")
        msg.setText(mensagem)
        msg.exec()

    def _mostrar_sucesso(self, mensagem: str):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Sucesso")
        msg.setText(mensagem)
        msg.exec()