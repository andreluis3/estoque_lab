from PyQt6.QtWidgets import QTableWidget, QHeaderView
from PyQt6.QtCore import Qt
from inventario.ui.theme.styles import ESTILO_TABELA

class TabelaEstoqueWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.iniciar_ui()

    def iniciar_ui(self):
        self.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.setStyleSheet(ESTILO_TABELA)
        
        # Configuração de cabeçalhos e alinhamentos originais
        self.verticalHeader().setDefaultSectionSize(38)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)