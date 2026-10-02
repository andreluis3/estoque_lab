from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt, QTimer

from inventario.ui.legacy.tabela_estoque import TabelaEstoque
from inventario.ui.legacy.dialogo_inserir import DialogoInserir
from inventario.ui.legacy.tela_historico import TelaHistorico
from inventario.services.authenticator import autenticar
from inventario.services.log_service import registrar_log


class MainWindow(QMainWindow):
    def __init__(self, estoque_service):  # <- Agora recebe corretamente o serviço injetado pelo main.py
        super().__init__()

        self.usuario_logado = None
        # ENGENHARIA ARQUITETURAL: Salvamos o centralizador de serviços na janela principal
        self.estoque_service = estoque_service

        # Inicia com tela de login
        self.criar_tela_login()

    # ── Tabela (Usando as regras e métodos do Service) ──────────────────────

    def carregar_tabela(self):
        self.itens_completos = self.estoque_service.listar_todos_itens()
        
        self.tabela.blockSignals(True)
        self.tabela.carregar_dados(self.itens_completos)
        self.tabela.blockSignals(False)
        self.label_status.setText(f"{len(self.itens_completos)} itens carregados")

    def filtrar_tabela(self, texto):
        texto = texto.strip().lower()
        
        # Se o campo de busca for limpo, recarrega todos os itens originais
        if not texto:
            self.tabela.blockSignals(True)
            self.tabela.carregar_dados(self.itens_completos)
            self.tabela.blockSignals(False)
            self.label_status.setText(f"{len(self.itens_completos)} itens carregados")
            return

        # Filtra a lista de dicionários na memória de forma ultra rápida e segura
        itens_filtrados = []
        for item in self.itens_completos:
            nome = str(item.get("nome", "")).lower()
            tipo = str(item.get("tipo", "")).lower()
            modelo = str(item.get("modelo", "")).lower()
            caixa = str(item.get("caixa", "")).lower()
            localizacao = str(item.get("localizacao", "")).lower()

            # Se o texto coincidir com qualquer um destes campos, mantém o item
            if (texto in nome) or (texto in tipo) or (texto in modelo) or (texto in caixa) or (texto in localizacao):
                itens_filtrados.append(item)

        # Atualiza a tabela apenas com os resultados correspondentes
        self.tabela.blockSignals(True)
        self.tabela.carregar_dados(itens_filtrados)
        self.tabela.blockSignals(False)
        self.label_status.setText(f"{len(itens_filtrados)} itens encontrados para a busca")

    def on_item_changed(self, item):
        """Edição inline de célula na tabela — envia para validação e persistência do Service."""
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

            # Deixamos a validação de tipo e consistência básica no fluxo rápido da UI,
            # mas o EstoqueService também revalida tudo por baixo dos panos.
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
            print(f"[janela_principal], item clicado: id={item_id}, campo={campo}, valor={valor}")

            # Chama a inteligência enterprise do EstoqueService em vez do CRUD direto
            usuario = self.usuario_logado or "sistema"
            resultado = self.estoque_service.atualizar_item(item_id, {campo: valor}, usuario=usuario)

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
        """Abre o dialog para adicionar um novo item passando o orquestrador de serviço."""
        # Passa o estoque_service que está na janela principal direto para o diálogo
        dialogo = DialogoInserir(estoque_service=self.estoque_service)
        print("[janela_principal] Abrindo diálogo de inserção com EstoqueService injetado.")
        
        # Fazemos um pequeno ajuste dinâmico: injetamos o usuário ativo no diálogo antes de abrir
        # para que o log registre quem realmente salvou o componente no lab
        if self.usuario_logado:
            def _salvar_com_usuario_real():
                dados_item = dialogo._coletar_dados()
                try:
                    resultado = dialogo.estoque_service.registrar_item(dados_item, usuario=self.usuario_logado)
                    if resultado.get("acao") == "atualizado":
                        msg = "Quantidade acumulada e atualizada no item existente!"
                    else:
                        msg = "Novo item inserido com sucesso no estoque!"
                    QMessageBox.information(dialogo, "Sucesso", msg)
                    dialogo.accept()
                except ValueError as e:
                    QMessageBox.warning(dialogo, "Aviso de Validação", str(e))
                except Exception as e:
                    QMessageBox.critical(dialogo, "Erro Operacional", f"Falha ao salvar: {str(e)}")
            dialogo.botao_salvar.disconnect()
            dialogo.botao_salvar.clicked.connect(_salvar_com_usuario_real)

        if dialogo.exec():
            self.carregar_tabela()
            self.label_status.setText("✅ Item adicionado com sucesso.")

    # ── Histórico ──────────────────────────────────────────────────────────

    def abrir_historico(self):
        # Caso sua TelaHistorico precise se adaptar depois, ela também usará a conexão/service.
        # Temporariamente passamos o service adaptado se necessário.
        tela = TelaHistorico(self.estoque_service)
        tela.exec()

    # ── Mensagens ──────────────────────────────────────────────────────────

    def _mostrar_erro(self, mensagem: str):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erro")
        msg.setText(mensagem)
        msg.exec()
        print(f"[janela_principal] Erro: {mensagem}")

    def _mostrar_sucesso(self, mensagem: str):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Sucesso")
        msg.setText(mensagem)
        msg.exec()
        print(f"[janela_principal] Sucesso: {mensagem}")

    # ── Construção de Telas e Fluxos ───────────────────────────────────────

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
        print("[janela_principal] TabelaEstoque criada e conectada ao on_item_changed.")

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
        print(f"[janela_principal] Tela de login criada. Usuário logado: {self.usuario_logado}")

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

        # REGRA REVOLUCIONADA: Em vez de acessar o arquivo bruto de CRUD, o estoque_service 
        # intercepta, verifica a quantidade restante e debita usando a transação isolada!
        try:
            # Como ainda não havíamos migrado o 'retirar_item' para o service na resposta anterior,
            # adicionei dinamicamente um fallback seguro para você não perder a funcionalidade.
            if hasattr(self.estoque_service, 'retirar_item'):
                resultado = self.estoque_service.retirar_item(item_id, qtd, usuario, motivo)
            else:
                # Caso o seu service queira ler direto do repo_item:
                # Buscamos a quantidade atual usando a conexão ativa
                r = self.estoque_service.item_repo.buscar_por_id(item_id)
                if not r:
                    resultado = {"status": "erro", "mensagem": "Item não encontrado"}
                elif qtd > r[3]: # r[3] é a quantidade atual no banco
                    resultado = {"status": "erro", "mensagem": "Quantidade insuficiente"}
                else:
                    nova_qtd = r[3] - qtd
                    self.estoque_service.item_repo.atualizar_quantidade(item_id, nova_qtd)
                    self.estoque_service.mov_repo.registrar(item_id, "saida", qtd, usuario)
                    self.estoque_service.hist_repo.registrar(item_id, "quantidade", str(r[3]), str(nova_qtd), usuario, "retirada")
                    registrar_log(usuario, "RETIRADA", f"{usuario} retirou {qtd}x {r[0]} | Motivo: {motivo}")
                    self.estoque_service.conn.commit()
                    resultado = {"status": "ok"}
        except Exception as e:
            resultado = {"status": "erro", "mensagem": str(e)}

        if resultado["status"] == "ok":
            self.carregar_tabela()
            self.label_status.setText("✅ Item retirado com sucesso")
        else:
            self._mostrar_erro(resultado["mensagem"])