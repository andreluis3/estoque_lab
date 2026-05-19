from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer

from ui.tabela_estoque import TabelaEstoque
from ui.dialogo_inserir import DialogoInserir
from ui.tela_historico import TelaHistorico
from controllers.crud import Crud
from services.authenticator import autenticar
from services.log_service import registrar_log
from PyQt6.QtWidgets import QInputDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.usuario_logado = None
        self.crud = Crud()

        # Inicia com tela de login
        self.criar_tela_login()

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

            resultado = self.crud.atualizar_item(item_id, {campo: valor}, usuario=self.usuario_logado or "sistema")

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

    def mostrar_sistema_principal(self):
        """Cria e mostra a interface principal do sistema após login."""
        self.setWindowTitle("ARMAZENAMENTO DE COMPONENTES - LABORATÓRIO DE EMC")
        self.resize(1100, 650)

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
        
        self.btn_retirar = QPushButton("➖ Retirar Item")
        self.btn_retirar.clicked.connect(self.retirar_item)

        botoes.addWidget(self.btn_retirar)

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
        
    def criar_tela_login(self):
        self.widget_login = QWidget()
        layout = QVBoxLayout()

        # Título
        titulo = QLabel("🔐 Login do Sistema")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        # Campo usuário
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Usuário (ex: andre)")
        layout.addWidget(self.input_usuario)

        # Campo senha
        self.input_senha = QLineEdit()
        self.input_senha.setPlaceholderText("Senha (DD/MM/AA)")
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_senha)

        # Botão login
        botao_login = QPushButton("Entrar")
        layout.addWidget(botao_login)

        # Status
        self.label_login_status = QLabel("")
        self.label_login_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_login_status)

        # Ação do login
        def fazer_login():
            usuario = self.input_usuario.text().strip().lower()
            senha = self.input_senha.text().strip()

            if autenticar(usuario, senha):
                self.usuario_logado = usuario
                self.label_login_status.setText("✅ Login realizado com sucesso")
                registrar_log(usuario, "LOGIN", "Usuário entrou no sistema")
                self.mostrar_sistema_principal()
            else:
                self.label_login_status.setText("❌ Usuário ou senha inválidos")

        # Clique do botão
        botao_login.clicked.connect(fazer_login)

        # ENTER nos campos
        self.input_usuario.returnPressed.connect(fazer_login)
        self.input_senha.returnPressed.connect(fazer_login)

        self.widget_login.setLayout(layout)
        self.setCentralWidget(self.widget_login)
        
    def retirar_item(self):
        row = self.tabela.currentRow()

        if row < 0:
            self._mostrar_erro("Selecione um item primeiro")
            return

        item_id_widget = self.tabela.item(row, 0)
        nome_widget = self.tabela.item(row, 1)

        if item_id_widget is None or nome_widget is None:
            self._mostrar_erro("Erro ao acessar item da tabela")
            return

        item_id = int(item_id_widget.text())
        nome = nome_widget.text()

        qtd, ok = QInputDialog.getInt(self, "Quantidade", f"Quantidade para retirar de {nome}:")

        if not ok or qtd <= 0:
            return

        motivo, ok = QInputDialog.getText(self, "Motivo", "Descreva o motivo da retirada:")

        if not ok or not motivo.strip():
            self._mostrar_erro("Motivo é obrigatório")
            return

        if not self.usuario_logado:
            self._mostrar_erro("Usuário não identificado. Faça login novamente.")
            return

        usuario = self.usuario_logado

        resultado = self.crud.retirar_item(
            item_id,
            qtd,
            usuario,
            motivo)


        if resultado["status"] == "ok":
            self.carregar_tabela()
            self.label_status.setText("✅ Item retirado com sucesso")
        else:
            self._mostrar_erro(resultado["mensagem"])
            
        