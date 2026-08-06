from PyQt6.QtWidgets import QTableWidget, QHeaderView,QMenu, QAbstractItemView, QTableWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal
from inventario.ui.theme.styles import ESTILO_TABELA
from PyQt6.QtCore import Qt
from inventario.ui.theme.styles import ESTILO_TABELA
from PyQt6.QtGui import QAction

class TabelaEstoqueWidget(QTableWidget):
    """
    Tabela de estoque da Henrique Screen.

    Este widget é um COMPONENTE INTERNO (QTableWidget comum), não uma janela.
    Ele não sabe nada sobre banco de dados ou EstoqueService — apenas recebe
    uma lista de itens já prontos e os exibe. Toda a lógica de busca no banco
    fica na TelaHenriquePage / EstoqueService, mantendo a separação de
    responsabilidades (a tabela só cuida de "como mostrar", não de
    "de onde vêm os dados").
    """

    COLUNAS = [
        "ID",
        "NOME",
        "TIPO",
        "MODELO",
        "QUANTIDADE",
        "CAIXA",
        "LOCALIZAÇÃO",
        "SLOT",
    ]

    CAMPOS = [
        "id",
        "nome",
        "tipo",
        "modelo",
        "quantidade",
        "caixa",
        "localizacao",
        "slot",
    ]
    
    item_selecionado = pyqtSignal(dict)
    
       # Sinais disparados pelo menu de contexto / duplo clique
    editar_solicitado = pyqtSignal(dict)
    deletar_solicitado = pyqtSignal(dict)
    adicionar_solicitado = pyqtSignal()
    movimentar_solicitado = pyqtSignal(dict)
    historico_solicitado = pyqtSignal()
    lista_compras_solicitado = pyqtSignal(dict)
    
    

    def __init__(self, parent=None):
        super().__init__(parent)
        self.configurar_tabela()
        self.aplicar_estilo()
        self.itemSelectionChanged.connect(self.selecionar_item)
        self.itemDoubleClicked.connect(self._ao_dar_duplo_clique)
        # Menu de contexto (botão direito)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.abrir_menu_contexto)

    # ------------------------------------------------------------------
    # CONFIGURAÇÃO ESTRUTURAL (colunas, seleção, scroll, cabeçalho)
    # ------------------------------------------------------------------
    def configurar_tabela(self):
        self.setColumnCount(len(self.COLUNAS))
        self.setHorizontalHeaderLabels(self.COLUNAS)

        # Comportamento: tabela só de leitura, seleciona linha inteira
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Linhas alternadas (facilita leitura em 325 itens)
        self.setAlternatingRowColors(True)

        # Scroll suave, pixel a pixel (necessário para 325 registros)
        self.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)

        # Esconde numeração vertical padrão do Qt
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(36)

        # Cabeçalho horizontal
        header = self.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # ID e QUANTIDADE mais estreitas, ocupam só o necessário
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

    # ------------------------------------------------------------------
    # ESTILO (reaproveita ESTILO_TABELA do theme/styles.py)
    # ------------------------------------------------------------------
    def aplicar_estilo(self):
        # Adiciona o estilo das linhas alternadas em cima do ESTILO_TABELA
        # existente, sem duplicar nada que já está no theme.
        estilo_com_alternancia = ESTILO_TABELA + """
            QTableWidget::item:alternate {
                background-color: #161616;
            }
        """
        self.setStyleSheet(estilo_com_alternancia)

    # ------------------------------------------------------------------
    # DADOS
    # ------------------------------------------------------------------
    def carregar_dados(self, itens):
        """
        itens: lista retornada por estoque_service.listar_todos_itens()
        Aceita tanto dicts quanto objetos (ORM/dataclass) com os atributos
        definidos em self.CAMPOS.
        """
        self.limpar_tabela()
        self.setRowCount(len(itens))
        self.setSortingEnabled(False)  # evita bug de reordenar durante o preenchimento

        for linha, item in enumerate(itens):
            valores = self._extrair_valores(item)
            for coluna, valor in enumerate(valores):
                texto = "" if valor is None else str(valor)
                cell = QTableWidgetItem(texto)
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(linha, coluna, cell)

        self.setSortingEnabled(True)

    def limpar_tabela(self):
        self.setRowCount(0)

    def _extrair_valores(self, item):
        if isinstance(item, dict):
            return [item.get(campo, "") for campo in self.CAMPOS]
        return [getattr(item, campo, "") for campo in self.CAMPOS]
    
    def selecionar_item(self):
            linha = self.currentRow()
            if linha < 0:
                return

            item = self._item_da_linha(linha)
            if item is None:
                return

            print("[TabelaEstoqueWidget] Item selecionado:")
            print(item)
            self.item_selecionado.emit(item)
            
    def _item_da_linha(self, linha: int) -> dict | None:
        """Reconstrói o dict completo a partir das células da linha."""
        id_widget = self.item(linha, 0)
        if id_widget is None:
            return None

        try:
            return {
                "id": int(id_widget.text()),
                "nome": self.item(linha, 1).text(),
                "tipo": self.item(linha, 2).text(),
                "modelo": self.item(linha, 3).text(),
                "quantidade": int(self.item(linha, 4).text() or 0),
                "caixa": self.item(linha, 5).text(),
                "localizacao": self.item(linha, 6).text(),
                "slot": self.item(linha, 7).text(),
            }
        except (AttributeError, ValueError):
            return None

    # ------------------------------------------------------------------
    # MENU DE CONTEXTO (clique com botão direito)
    # ------------------------------------------------------------------
    def abrir_menu_contexto(self, posicao):
        linha = self.rowAt(posicao.y())

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #1b1b1b;
                color: white;
                border: 1px solid #0078ff;
                border-radius: 8px;
                padding: 6px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #0078ff;
            }
            QMenu::separator {
                height: 1px;
                background: #2a2a2a;
                margin: 6px 4px;
            }
        """)

        # "Adicionar item" sempre disponível, mesmo sem linha clicada
        acao_adicionar = QAction("➕ Adicionar item", self)
        acao_adicionar.triggered.connect(self.adicionar_solicitado.emit)
        menu.addAction(acao_adicionar)

        item = self._item_da_linha(linha) if linha >= 0 else None

        if item is not None:
            self.selectRow(linha)  # garante que a linha clicada fique selecionada

            menu.addSeparator()

            acao_editar = QAction("✏ Editar", self)
            acao_editar.triggered.connect(lambda: self.editar_solicitado.emit(item))
            menu.addAction(acao_editar)

            acao_deletar = QAction("🗑 Deletar item", self)
            acao_deletar.triggered.connect(lambda: self.deletar_solicitado.emit(item))
            menu.addAction(acao_deletar)

            acao_movimentar = QAction("🔁 Movimentar item", self)
            acao_movimentar.triggered.connect(lambda: self.movimentar_solicitado.emit(item))
            menu.addAction(acao_movimentar)

            menu.addSeparator()

            acao_historico = QAction("📋 Ver histórico", self)
            acao_historico.triggered.connect(self.historico_solicitado.emit)
            menu.addAction(acao_historico)

            acao_lista_compras = QAction("🛒 Adicionar à lista de compras", self)
            acao_lista_compras.triggered.connect(lambda: self.lista_compras_solicitado.emit(item))
            menu.addAction(acao_lista_compras)

        menu.exec(self.viewport().mapToGlobal(posicao))


    def _ao_dar_duplo_clique(self, cell: QTableWidgetItem):
        item = self._item_da_linha(cell.row())
        if item is not None:
            self.editar_solicitado.emit(item)
                
        