"""
item_falta_card.py — Card individual de item em estoque crítico.

Usado dentro do ItensEmFaltaDialog. Não faz nenhuma consulta ao banco,
apenas recebe um dict já pronto e renderiza.
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


COR_CRITICO = "#ff4c4c"   # quantidade == 0
COR_ATENCAO = "#ffcc00"   # quantidade 1 ou 2


class ItemFaltaCard(QFrame):
    def __init__(self, item: dict, parent=None):
        super().__init__(parent)
        self.item = item
        self._setup_ui()

    def _setup_ui(self):
        qtd = self.item.get("quantidade", 0)
        cor_status = COR_CRITICO if qtd == 0 else COR_ATENCAO
        emoji_status = "🔴" if qtd == 0 else "🟡"

        self.setStyleSheet(f"""
            QFrame#cardFalta {{
                background-color: #1b1b1b;
                border: 1px solid {cor_status};
                border-left: 4px solid {cor_status};
                border-radius: 12px;
            }}
            QLabel {{
                color: white;
                background: transparent;
            }}
            QLabel#labelCampo {{
                color: #888888;
                font-size: 11px;
            }}
            QLabel#valorCampo {{
                color: white;
                font-size: 13px;
                font-weight: 500;
            }}
        """)
        self.setObjectName("cardFalta")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # ── Cabeçalho: bolinha + nome + quantidade em destaque ──
        header = QHBoxLayout()
        header.setSpacing(10)

        status_label = QLabel(emoji_status)
        status_label.setStyleSheet("font-size: 18px;")
        header.addWidget(status_label)

        nome_label = QLabel(self.item.get("nome", "—"))
        fonte_nome = QFont()
        fonte_nome.setPointSize(13)
        fonte_nome.setBold(True)
        nome_label.setFont(fonte_nome)
        header.addWidget(nome_label)

        header.addStretch()

        qtd_label = QLabel(f"Qtd: {qtd}")
        qtd_label.setStyleSheet(f"""
            color: {cor_status};
            font-size: 14px;
            font-weight: bold;
        """)
        header.addWidget(qtd_label)

        layout.addLayout(header)

        # ── Linha divisória sutil ──
        linha = QFrame()
        linha.setFixedHeight(1)
        linha.setStyleSheet("background-color: #2a2a2a; border: none;")
        layout.addWidget(linha)

        # ── Grid de detalhes ──
        grid = QGridLayout()
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(4)

        campos = [
            ("Modelo", self.item.get("modelo") or "—"),
            ("Tipo", self.item.get("tipo") or "—"),
            ("Caixa", self.item.get("caixa") or "—"),
            ("Localização", self.item.get("localizacao") or "—"),
        ]

        for col, (label, valor) in enumerate(campos):
            lbl_campo = QLabel(label)
            lbl_campo.setObjectName("labelCampo")
            lbl_valor = QLabel(str(valor))
            lbl_valor.setObjectName("valorCampo")

            grid.addWidget(lbl_campo, 0, col)
            grid.addWidget(lbl_valor, 1, col)

        layout.addLayout(grid)

    def corresponde_busca(self, termo: str) -> bool:
        """Usado pelo dialog para filtrar em tempo real."""
        termo = termo.lower().strip()
        if not termo:
            return True
        nome = str(self.item.get("nome", "")).lower()
        modelo = str(self.item.get("modelo", "")).lower()
        return termo in nome or termo in modelo