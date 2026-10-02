"""
lista_compras_dialog.py — Tela principal do módulo Lista de Compras.

Controla itens pendentes de compra.
Utiliza a tabela lista_compras do banco.
"""


from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QCheckBox, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from inventario.ui.theme.dialog_style import ESTILO_DIALOG
from inventario.ui.theme.styles import ESTILO_TABELA
from inventario.ui.dialogs.adicionar_lista_dialog import AdicionarListaDialog
from inventario.ui.dialogs.editar_lista_dialog import EditarListaDialog
from inventario.ui.dialogs.remover_lista_dialog import RemoverListaDialog
from inventario.ui.components.mensagem import Mensagem

COLUNAS = [
    "✔",
    "ID",
    "Nome",
    "Modelo",
    "Quantidade",
    "Status",
    "Observação",
    "Usuário",
    "Criado em"
]




class ListaComprasDialog(QDialog):
    def __init__(self, estoque_service, parent=None):
        super().__init__(parent)
        self.estoque_service = estoque_service
        self.item_selecionado: dict | None = None
        # trava para não disparar o toggle do checkbox ao repopular a tabela
        self._atualizando_tabela = False

        self.setWindowTitle("Lista de Compras")
        self.resize(1050, 600)
        self.setStyleSheet(ESTILO_DIALOG)
        self._setup_ui()
        self.carregar_lista()

    # ─── Layout ──────────────────────────────────────────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        titulo = QLabel("🛒 Lista de Compras")
        fonte = QFont()
        fonte.setPointSize(15)
        fonte.setBold(True)
        titulo.setFont(fonte)
        titulo.setStyleSheet("color: #0078ff;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("🔍 Pesquisar por nome ou modelo...")
        self.campo_busca.textChanged.connect(self._pesquisar)
        layout.addWidget(self.campo_busca)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(len(COLUNAS))
        self.tabela.setHorizontalHeaderLabels(COLUNAS)
        self.tabela.setStyleSheet(ESTILO_TABELA)
        self.tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        vh = self.tabela.verticalHeader()
        if vh is not None:
            vh.setVisible(False)
        h = self.tabela.horizontalHeader()
        if h is not None:
            h.setStretchLastSection(True)
            h.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tabela.itemSelectionChanged.connect(self._selecionar_linha)
        layout.addWidget(self.tabela)

        rodape = QHBoxLayout()
        self.label_total = QLabel("Total: 0 itens")
        self.label_total.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        rodape.addWidget(self.label_total)
        rodape.addStretch()

        self.botao_adicionar = QPushButton("+ Adicionar")
        self.botao_adicionar.clicked.connect(self._abrir_adicionar)
        rodape.addWidget(self.botao_adicionar)

        self.botao_editar = QPushButton("✏ Editar")
        self.botao_editar.clicked.connect(self._abrir_editar)
        rodape.addWidget(self.botao_editar)

        self.botao_remover = QPushButton("🗑 Remover")
        self.botao_remover.clicked.connect(self._abrir_remover)
        rodape.addWidget(self.botao_remover)

        self.botao_fechar = QPushButton("Fechar")
        self.botao_fechar.clicked.connect(self.close)
        rodape.addWidget(self.botao_fechar)

        layout.addLayout(rodape)

    # ─── Dados ───────────────────────────────────────────────────────────

    def carregar_lista(self):
        itens = self.estoque_service.listar_lista_compras()
        self._preencher_tabela(itens)

    def _pesquisar(self, termo: str):
        itens = self.estoque_service.pesquisar_lista_compras(termo)
        self._preencher_tabela(itens)

    def _preencher_tabela(self, itens: list[dict]):
        self._atualizando_tabela = True
        self.tabela.setRowCount(0)
        self.item_selecionado = None

        for row_idx, item in enumerate(itens):
            self.tabela.insertRow(row_idx)
            status = item.get("status", "PENDENTE")
            comprado = status == "COMPRADO"

            # Coluna 0 — checkbox "comprado", centralizado
            checkbox = QCheckBox()
            checkbox.setChecked(comprado)
            checkbox.stateChanged.connect(
                lambda estado, item_id=item["id"]: self._alternar_comprado(item_id, estado)
            )
            container = QWidget()
            wrap = QHBoxLayout(container)
            wrap.addWidget(checkbox)
            wrap.setAlignment(Qt.AlignmentFlag.AlignCenter)
            wrap.setContentsMargins(0, 0, 0, 0)
            self.tabela.setCellWidget(row_idx, 0, container)

            valores = [
                item["id"],
                item["nome"],
                item.get("modelo") or "—",
                item.get("quantidade") or 0,
                item.get("status") or "PENDENTE",
                item.get("observacao") or "—",
                item.get("usuario") or "—",
                item.get("criado_em") or "—" ]
            

            for col, val in enumerate(valores, start=1):
                cell = QTableWidgetItem(str(val))
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setData(Qt.ItemDataRole.UserRole, item)  # guarda o dict completo p/ seleção

                if comprado:
                    cell.setForeground(QColor("#666666"))
                    fonte_riscada = cell.font()
                    fonte_riscada.setStrikeOut(True)
                    cell.setFont(fonte_riscada)

                self.tabela.setItem(row_idx, col, cell)

        self.label_total.setText(f"Total: {len(itens)} itens")
        self._atualizando_tabela = False

    # ─── Seleção ─────────────────────────────────────────────────────────

    def _selecionar_linha(self):
        modelo_selecao = self.tabela.selectionModel()
        linhas = modelo_selecao.selectedRows() if modelo_selecao else []
        if not linhas:
            self.item_selecionado = None
            return

        row = linhas[0].row()
        cell = self.tabela.item(row, 1)  # coluna ID guarda o dict completo via UserRole
        if cell:
            self.item_selecionado = cell.data(Qt.ItemDataRole.UserRole)

    # ─── Ações: checkbox "comprado" ──────────────────────────────────────

    def _alternar_comprado(self, item_id: int, estado: int):
        if self._atualizando_tabela:
            return  # evita disparo em cascata durante o repopulamento

        marcado = estado == Qt.CheckState.Checked.value
        if marcado:
            resultado = self.estoque_service.marcar_item_comprado(item_id)
        else:
            resultado = self.estoque_service.desmarcar_item_comprado(item_id)

        if resultado["status"] != "ok":
            Mensagem.erro(self, resultado.get("mensagem", "Erro ao atualizar status."))

        self.carregar_lista()

    # ─── Ações: CRUD ─────────────────────────────────────────────────────

    def _abrir_adicionar(self):
        dialog = AdicionarListaDialog(self)
        dialog.item_adicionado.connect(self._adicionar_item)
        dialog.exec()

    def _adicionar_item(self, dados: dict):
        resultado = self.estoque_service.adicionar_lista_compras(dados)
        if resultado["status"] == "ok":
            self.carregar_lista()
            Mensagem.sucesso(self, resultado["mensagem"])
        else:
            Mensagem.erro(self, resultado["mensagem"])

    def _abrir_editar(self):
        if not self.item_selecionado:
            Mensagem.erro(self, "Selecione um item para editar.")
            return

        dialog = EditarListaDialog(self.item_selecionado, self)
        dialog.item_editado.connect(self._editar_item)
        dialog.exec()

    def _editar_item(self, item_id: int, dados: dict):
        resultado = self.estoque_service.editar_lista_compras(item_id, dados)
        if resultado["status"] == "ok":
            self.carregar_lista()
            Mensagem.sucesso(self, resultado["mensagem"])
        else:
            Mensagem.erro(self, resultado["mensagem"])

    def _abrir_remover(self):
        if not self.item_selecionado:
            Mensagem.erro(self, "Selecione um item para remover.")
            return

        dialog = RemoverListaDialog(self.item_selecionado, self)
        dialog.item_removido.connect(self._remover_item)
        dialog.exec()

    def _remover_item(self, item_id: int):
        resultado = self.estoque_service.remover_lista_compras(item_id)
        if resultado["status"] == "ok":
            self.carregar_lista()
            Mensagem.sucesso(self, resultado["mensagem"])
        else:
            Mensagem.erro(self, resultado["mensagem"])