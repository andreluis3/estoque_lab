import os
from inventario.ui.theme.scrollbar import SCROLLBAR

# Estilo unificado dos botões do menu lateral
ESTILO_BOTAO_MENU = """
    QPushButton {
        background-color: #1b1b1b;
        color: white;
        border: 1px solid #2d2d2d;
        border-radius: 14px;
        font-size: 35px;
        text-align: left;
        padding-left: 20px;
    }
    QPushButton:hover {
        background-color: #0078ff;
        border: 1px solid #3399ff;
    }
    QPushButton:pressed {
        background-color: #005ed1;
    }
"""

# Estilo da Tabela Principal
ESTILO_TABELA = f"""
    QTableWidget {{
        background-color: #111111;
        color: white;
        border: 1px solid #0078ff;
        border-radius: 14px;
        font-size: 16px;
        gridline-color: transparent;
        padding: 6px;
    }}
    QTableWidget::item {{
        padding: 10px;
        border-bottom: 1px solid #1a1a1a;
    }}
    QTableWidget::item:selected {{
        background-color: #0078ff;
        color: white;
        border-radius: 6px;
    }}
    QHeaderView::section {{
        background-color: #151515;
        color: #0078ff;
        padding: 14px;
        border: none;
        font-weight: bold;
        font-size: 15px;
    }}
    QCornerButton::section {{
        background-color: #151515;
        border: none;
    }}
    {SCROLLBAR}
"""