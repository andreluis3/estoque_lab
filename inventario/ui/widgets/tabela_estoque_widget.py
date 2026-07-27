from PyQt6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal
from inventario.ui.theme.styles import ESTILO_TABELA
from PyQt6.QtCore import Qt
from inventario.ui.theme.styles import ESTILO_TABELA


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

    # Nomes dos atributos/keys esperados em cada item vindo do service.
    # Se seus objetos/dicts usarem outros nomes, ajuste apenas esta lista.
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

    def __init__(self, parent=None):
        super().__init__(parent)
        self.configurar_tabela()
        self.aplicar_estilo()
        self.itemSelectionChanged.connect(self.selecionar_item)

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

        item = {
            "id": int(self.item(linha, 0).text()),
            "nome": self.item(linha, 1).text(),
            "tipo": self.item(linha, 2).text(),
            "modelo": self.item(linha, 3).text(),
            "quantidade": int(self.item(linha, 4).text()),
            "caixa": self.item(linha, 5).text(),
            "localizacao": self.item(linha, 6).text(),
            "slot": self.item(linha, 7).text(),
        }

        print("[TabelaEstoqueWidget] Printando item selecionado:")
        print(item)
        self.item_selecionado.emit(item)
            
        