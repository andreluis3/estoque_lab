"""
itens_em_falta_dialog.py — Painel de estoque crítico (itens com quantidade <= 2).

Uso:
    dialog = ItensEmFaltaDialog(self.estoque_service, self)
    dialog.exec()
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from inventario.ui.theme.dialog_style import ESTILO_DIALOG
from inventario.ui.theme.scrollbar import SCROLLBAR
from inventario.ui.widgets.item_falta_card import ItemFaltaCard


class ItensEmFaltaDialog(QDialog):
    def __init__(self, estoque_service, parent=None):
        super().__init__(parent)
        self.estoque_service = estoque_service
        self.cards: list[ItemFaltaCard] = []

        self.setWindowTitle("Estoque Crítico")
        self.resize(650, 700)
        self.setStyleSheet(ESTILO_DIALOG + SCROLLBAR)
        self._setup_ui()
        self.carregar_itens()

    # ─── Layout ──────────────────────────────────────────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        layout.addLayout(self._cabecalho())
        layout.addWidget(self._campo_busca())

        # Área de scroll com os cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")

        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.lista_layout = QVBoxLayout(self.container)
        self.lista_layout.setSpacing(10)
        self.lista_layout.setContentsMargins(2, 2, 2, 2)
        self.lista_layout.addStretch()

        self.scroll_area.setWidget(self.container)
        layout.addWidget(self.scroll_area, stretch=1)

        layout.addLayout(self._rodape())

    def _cabecalho(self) -> QVBoxLayout:
        v = QVBoxLayout()
        v.setSpacing(4)

        titulo = QLabel("⚠️ Estoque Crítico")
        fonte_titulo = QFont()
        fonte_titulo.setPointSize(16)
        fonte_titulo.setBold(True)
        titulo.setFont(fonte_titulo)
        titulo.setStyleSheet("color: #0078ff;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(titulo)

        subtitulo = QLabel("Componentes com estoque baixo (quantidade ≤ 2)")
        subtitulo.setStyleSheet("color: #888888; font-size: 12px;")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(subtitulo)

        return v

    def _campo_busca(self) -> QLineEdit:
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("🔍 Buscar por nome ou modelo...")
        self.campo_busca.textChanged.connect(self._filtrar)
        return self.campo_busca

    def _rodape(self) -> QHBoxLayout:
        h = QHBoxLayout()
        self.label_total = QLabel("Total de itens críticos: 0")
        self.label_total.setStyleSheet("color: #aaaaaa; font-size: 12px;")

        btn_fechar = QPushButton("Fechar")
        btn_fechar.setFixedWidth(120)
        btn_fechar.clicked.connect(self.close)

        h.addWidget(self.label_total)
        h.addStretch()
        h.addWidget(btn_fechar)
        return h

    # ─── Dados ───────────────────────────────────────────────────────────

    def carregar_itens(self):
        # Limpa cards antigos (mantém o addStretch no fim)
        for card in self.cards:
            self.lista_layout.removeWidget(card)
            card.deleteLater()
        self.cards.clear()

        itens = self.estoque_service.listar_itens_criticos()

        for item in itens:
            card = ItemFaltaCard(item)
            # insere antes do stretch (que fica sempre no último índice)
            self.lista_layout.insertWidget(self.lista_layout.count() - 1, card)
            self.cards.append(card)

        self._atualizar_total()

    def _filtrar(self, texto: str):
        visiveis = 0
        for card in self.cards:
            mostrar = card.corresponde_busca(texto)
            card.setVisible(mostrar)
            if mostrar:
                visiveis += 1
        self._atualizar_total(visiveis)

    def _atualizar_total(self, quantidade: int | None = None):
        total = quantidade if quantidade is not None else len(self.cards)
        self.label_total.setText(f"Total de itens críticos: {total}")