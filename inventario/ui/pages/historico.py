"""
tela_historico.py — Tela de histórico de movimentações e auditoria.

Como usar no janela_principal.py:
    from inventario.ui.tela_historico import TelaHistorico
    # num botão:
    tela = TelaHistorico(self.service)
    tela.show()
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
    QPushButton, QComboBox, QHeaderView, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont


class TelaHistorico(QWidget):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.setWindowTitle("📋 Histórico")
        self._setup_ui()
        self._carregar_tudo()

    # ─── Layout ──────────────────────────────────────────────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # Título
        titulo = QLabel("Histórico de Movimentações e Alterações")
        fonte = QFont()
        fonte.setPointSize(13)
        fonte.setBold(True)
        titulo.setFont(fonte)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Filtros
        layout.addWidget(self._barra_filtros())

        # Abas
        self.abas = QTabWidget()
        self.abas.addTab(self._aba_movimentacoes(), "📦 Entradas / Saídas")
        self.abas.addTab(self._aba_historico(),     "🔍 Alterações de Campos")
        layout.addWidget(self.abas)

        # Rodapé
        rodape = QHBoxLayout()
        self.label_total = QLabel("Total: 0 registros")
        btn_fechar = QPushButton("Fechar")
        btn_fechar.clicked.connect(self.close)
        rodape.addWidget(self.label_total)
        rodape.addStretch()
        rodape.addWidget(btn_fechar)
        layout.addLayout(rodape)

    def _barra_filtros(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        h = QHBoxLayout(frame)
        h.setContentsMargins(8, 6, 8, 6)

        h.addWidget(QLabel("Usuário:"))
        self.filtro_usuario = QLineEdit()
        self.filtro_usuario.setPlaceholderText("ex: andre")
        self.filtro_usuario.setFixedWidth(140)
        h.addWidget(self.filtro_usuario)

        h.addWidget(QLabel("Item ID:"))
        self.filtro_item_id = QLineEdit()
        self.filtro_item_id.setPlaceholderText("ex: 42")
        self.filtro_item_id.setFixedWidth(80)
        h.addWidget(self.filtro_item_id)

        h.addWidget(QLabel("Tipo:"))
        self.filtro_tipo = QComboBox()
        self.filtro_tipo.addItems(["Todos", "entrada", "saida"])
        self.filtro_tipo.setFixedWidth(110)
        h.addWidget(self.filtro_tipo)

        btn_filtrar = QPushButton("🔍 Filtrar")
        btn_filtrar.clicked.connect(self._carregar_tudo)
        h.addWidget(btn_filtrar)

        btn_limpar = QPushButton("✖ Limpar")
        btn_limpar.clicked.connect(self._limpar_filtros)
        h.addWidget(btn_limpar)

        h.addStretch()
        return frame

    def _aba_movimentacoes(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)

        self.tabela_mov = QTableWidget()
        self.tabela_mov.setColumnCount(7)
        self.tabela_mov.setHorizontalHeaderLabels([
            "ID", "Item ID", "Nome", "Modelo", "Tipo", "Quantidade", "Usuário", 
        ])
        # A coluna data fica fora da lista acima — adiciona separado
        self.tabela_mov.setColumnCount(8)
        self.tabela_mov.setHorizontalHeaderLabels([
            "ID", "Item ID", "Nome", "Modelo", "Tipo", "Qtd", "Usuário", "Data/Hora"
        ])
        self._estilizar_tabela(self.tabela_mov)
        layout.addWidget(self.tabela_mov)
        return w

    def _aba_historico(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)

        self.tabela_hist = QTableWidget()
        self.tabela_hist.setColumnCount(9)
        self.tabela_hist.setHorizontalHeaderLabels([
            "ID", "Item ID", "Nome", "Modelo",
            "Campo Alterado", "Antes", "Depois", "Usuário", "Data/Hora"
        ])
        self._estilizar_tabela(self.tabela_hist)
        layout.addWidget(self.tabela_hist)
        return w

    def _estilizar_tabela(self, tabela: QTableWidget):
        tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tabela.setAlternatingRowColors(True)
        vh = tabela.verticalHeader()
        if vh is not None:
            vh.setVisible(False)
        h = tabela.horizontalHeader()
        if h is not None:
            h.setStretchLastSection(True)
            h.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    # ─── Dados ───────────────────────────────────────────────────────────────

    def _carregar_tudo(self):
        usuario = self.filtro_usuario.text().strip() or None
        tipo    = self.filtro_tipo.currentText()
        tipo    = None if tipo == "Todos" else tipo

        item_id_txt = self.filtro_item_id.text().strip()
        item_id = int(item_id_txt) if item_id_txt.isdigit() else None

        movs  = self.service.listar_movimentacoes(item_id=item_id, tipo=tipo, usuario=usuario)
        hists = self.service.listar_historico(item_id=item_id, usuario=usuario)

        self._preencher_movimentacoes(movs)
        self._preencher_historico(hists)

        total = len(movs) + len(hists)
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

                # Colorir entrada (verde) e saída (vermelho)
                if col == 4:
                    if val == "entrada":
                        cell.setForeground(QColor("#2e7d32"))
                        cell.setFont(self._fonte_negrito())
                    elif val == "saida":
                        cell.setForeground(QColor("#c62828"))
                        cell.setFont(self._fonte_negrito())

                t.setItem(row_idx, col, cell)

    def _preencher_historico(self, dados: list[dict]):
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

                # Destacar ação de deletar
                if d.get("acao") == "deletado":
                    cell.setForeground(QColor("#b71c1c"))

                t.setItem(row_idx, col, cell)

    def _limpar_filtros(self):
        self.filtro_usuario.clear()
        self.filtro_item_id.clear()
        self.filtro_tipo.setCurrentIndex(0)
        self._carregar_tudo()

    def _fonte_negrito(self) -> QFont:
        f = QFont()
        f.setBold(True)
        return f