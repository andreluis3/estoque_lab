from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtCore import Qt


class TabelaEstoque(QTableWidget):
    def __init__(self):
        super().__init__()

        self.colunas = ["ID", "Nome", "Tipo", "Modelo", "Quantidade", "Caixa", "Localização"]

        self.setColumnCount(len(self.colunas))
        self.setHorizontalHeaderLabels(self.colunas)

        # 🔥 esconder ID (mas ele existe!)
        self.setColumnHidden(0, True)

        # estética
        self.horizontalHeader().setStretchLastSection(True)
        #ajustar colunas para tabela
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)          # Nome
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents) # Tipo
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # Modelo
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # Quantidade
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # Caixa
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)          # Localização
        self.setAlternatingRowColors(True)
        
    def carregar_dados(self, itens):
        self.setRowCount(0)

        for item in itens:
            row = self.rowCount()
            self.insertRow(row)

            valores = [
                item["id"],
                item["nome"],
                item["tipo"],
                item["modelo"],
                item["quantidade"],
                item["caixa"],
                item["localizacao"]
            ]

            for col, valor in enumerate(valores):
                cell = QTableWidgetItem(str(valor))
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(row, col, cell)

    def adicionar_item(self, dados):
        row = self.rowCount()
        self.insertRow(row)

        valores = [
            dados["id"],
            dados["nome"],
            dados["tipo"],
            dados["modelo"],
            dados["quantidade"],
            dados["caixa"],
            dados["localizacao"]
        ]

        for col, valor in enumerate(valores):
            item = QTableWidgetItem(str(valor))

            # 🔥 CENTRALIZAR TEXTO
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.setItem(row, col, item)
            