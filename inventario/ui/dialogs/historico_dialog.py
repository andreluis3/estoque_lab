"""
historico_dialog.py — Dialog de histórico de movimentações e alterações.

Segue o padrão visual dos outros dialogs (ESTILO_DIALOG) e as tabelas
usam o mesmo estilo da tabela principal do sistema (ESTILO_TABELA).

Uso (dentro do henrique_screen.py):
    from inventario.ui.dialogs.historico_dialog import HistoricoDialog
    dialog = HistoricoDialog(self.estoque_service, self)
    dialog.exec()
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
    QPushButton, QComboBox, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

from inventario.ui.theme.styles import ESTILO_TABELA
from inventario.ui.theme.dialog_style import ESTILO_DIALOG

ESTILO_TABS = """
    QTabWidget::pane {
        border: 1px solid #0078ff;
        border-radius: 10px;
        background-color: #111111;
        top: -1px;
    }
    QTabBar::tab {
        background: #1b1b1b;
        color: white;
        padding: 10px 18px;
        margin-right: 4px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-size: 13px;
        font-weight: 500;
    }
    QTabBar::tab:selected {
        background: #0078ff;
        color: white;
    }
    QTabBar::tab:hover {
        background: #005ed1;
    }
"""

ESTILO_COMBO = """
    QComboBox {
        background: #222222;
        color: white;
        border: 1px solid #0078ff;
        border-radius: 6px;
        padding: 6px;
    }
    QComboBox QAbstractItemView {
        background: #1b1b1b;
        color: white;
        selection-background-color: #0078ff;
    }
"""


class HistoricoDialog(QDialog):
    def __init__(self, estoque_service, parent=None):
        super().__init__(parent)
        self.estoque_service = estoque_service
        self.setWindowTitle("Histórico")
        self.resize(1150, 680)
        self.setStyleSheet(ESTILO_DIALOG + ESTILO_TABS + ESTILO_COMBO)
        self._setup_ui()
        self.carregar_historico()

    # ─── Layout ──────────────────────────────────────────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        titulo = QLabel("Histórico de Movimentações e Alterações")
        fonte = QFont()
        fonte.setPointSize(15)
        fonte.setBold(True)
        titulo.setFont(fonte)
        titulo.setStyleSheet("color: #0078ff;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        layout.addWidget(self._barra_filtros())

        self.abas = QTabWidget()
        self.abas.addTab(self._aba_movimentacoes(), "📦 Entradas / Saídas")
        self.abas.addTab(self._aba_alteracoes(), "🔍 Alterações de Campos")
        layout.addWidget(self.abas)

        rodape = QHBoxLayout()
        self.label_total = QLabel("Total: 0 registros")
        self.label_total.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        btn_fechar = QPushButton("Fechar")
        btn_fechar.setFixedWidth(120)
        btn_fechar.clicked.connect(self.close)
        rodape.addWidget(self.label_total)
        rodape.addStretch()
        rodape.addWidget(btn_fechar)
        layout.addLayout(rodape)

    def _barra_filtros(self) -> QWidget:
        frame = QWidget()
        h = QHBoxLayout(frame)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(10)

        h.addWidget(QLabel("Usuário:"))
        self.filtro_usuario = QLineEdit()
        self.filtro_usuario.setPlaceholderText("ex: andre")
        self.filtro_usuario.setFixedWidth(150)
        h.addWidget(self.filtro_usuario)

        h.addWidget(QLabel("Item ID:"))
        self.filtro_item_id = QLineEdit()
        self.filtro_item_id.setPlaceholderText("ex: 42")
        self.filtro_item_id.setFixedWidth(90)
        h.addWidget(self.filtro_item_id)

        h.addWidget(QLabel("Tipo:"))
        self.filtro_tipo = QComboBox()
        self.filtro_tipo.addItems(["Todos", "entrada", "saida"])
        self.filtro_tipo.setFixedWidth(120)
        h.addWidget(self.filtro_tipo)

        btn_filtrar = QPushButton("🔍 Filtrar")
        btn_filtrar.setFixedWidth(110)
        btn_filtrar.clicked.connect(self.carregar_historico)
        h.addWidget(btn_filtrar)

        btn_limpar = QPushButton("✖ Limpar")
        btn_limpar.setFixedWidth(100)
        btn_limpar.clicked.connect(self._limpar_filtros)
        h.addWidget(btn_limpar)

        h.addStretch()
        return frame

    def _aba_movimentacoes(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(10, 10, 10, 10)

        self.tabela_mov = QTableWidget()
        self.tabela_mov.setColumnCount(8)
        self.tabela_mov.setHorizontalHeaderLabels(
            ["ID", "Item ID", "Nome", "Modelo", "Tipo", "Qtd", "Usuário", "Data/Hora"]
        )
        self._estilizar_tabela(self.tabela_mov)
        layout.addWidget(self.tabela_mov)
        return w

    def _aba_alteracoes(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(10, 10, 10, 10)

        self.tabela_hist = QTableWidget()
        self.tabela_hist.setColumnCount(9)
        self.tabela_hist.setHorizontalHeaderLabels(
            ["ID", "Item ID", "Nome", "Modelo", "Campo", "Antes", "Depois", "Usuário", "Data/Hora"]
        )
        self._estilizar_tabela(self.tabela_hist)
        layout.addWidget(self.tabela_hist)
        return w

    def _estilizar_tabela(self, tabela: QTableWidget):
        tabela.setStyleSheet(ESTILO_TABELA)
        tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tabela.setAlternatingRowColors(False)
        vh = tabela.verticalHeader()
        if vh is not None:
            vh.setVisible(False)
        h = tabela.horizontalHeader()
        if h is not None:
            h.setStretchLastSection(True)
            h.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    # ─── Dados ───────────────────────────────────────────────────────────

    def carregar_historico(self):
        usuario = self.filtro_usuario.text().strip() or None
        tipo = self.filtro_tipo.currentText()
        tipo = None if tipo == "Todos" else tipo

        item_id_txt = self.filtro_item_id.text().strip()
        item_id = int(item_id_txt) if item_id_txt.isdigit() else None

        movs = self.estoque_service.listar_movimentacoes(item_id=item_id, tipo=tipo, usuario=usuario)
        hists = self.estoque_service.listar_historico(item_id=item_id, usuario=usuario)

        self._preencher_movimentacoes(movs)
        self._preencher_alteracoes(hists)

        self.label_total.setText(f"Total: {len(movs)} movimentações  |  {len(hists)} alterações")

    def _preencher_movimentacoes(self, dados: list[dict]):
        t = self.tabela_mov
        t.setRowCount(0)
        for row_idx, d in enumerate(dados):
            t.insertRow(row_idx)
            valores = [
                d["id"], d["item_id"], d["item_nome"], d["item_modelo"],
                d["tipo"], d["quantidade"], d["usuario"], d["data"]
            ]
            for col, val in enumerate(valores):
                cell = QTableWidgetItem(str(val) if val is not None else "—")
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 4:
                    if val == "entrada":
                        cell.setForeground(QColor("#2ecc71"))
                        cell.setFont(self._fonte_negrito())
                    elif val == "saida":
                        cell.setForeground(QColor("#ff4c4c"))
                        cell.setFont(self._fonte_negrito())
                t.setItem(row_idx, col, cell)

    def _preencher_alteracoes(self, dados: list[dict]):
        t = self.tabela_hist
        t.setRowCount(0)
        for row_idx, d in enumerate(dados):
            t.insertRow(row_idx)
            valores = [
                d["id"], d["item_id"], d["item_nome"], d["item_modelo"],
                d["campo"], d["valor_anterior"], d["valor_novo"],
                d["usuario"], d["data"]
            ]
            for col, val in enumerate(valores):
                cell = QTableWidgetItem(str(val) if val is not None else "—")
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if d.get("acao") == "deletado":
                    cell.setForeground(QColor("#ff4c4c"))
                t.setItem(row_idx, col, cell)

    def _limpar_filtros(self):
        self.filtro_usuario.clear()
        self.filtro_item_id.clear()
        self.filtro_tipo.setCurrentIndex(0)
        self.carregar_historico()

    def _fonte_negrito(self) -> QFont:
        f = QFont()
        f.setBold(True)
        return f