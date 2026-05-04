from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtCore import Qt


class TabelaEstoque(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(8)
        self.setHorizontalHeaderLabels([
            "ID", "Nome", "Tipo", "Modelo",
            "Quantidade", "Caixa", "Localização", "Slot"
        ])

    def carregar_dados(self, itens):
        self.blockSignals(True)  # 🔥 evita bug ao carregar

        self.setRowCount(len(itens))

        for row, item in enumerate(itens):
            valores = [
                item["id"],
                item["nome"],
                item["tipo"],
                item["modelo"],
                item["quantidade"],
                item["caixa"],
                item["localizacao"],
                item["slot"],
            ]

            for col, valor in enumerate(valores):
                cell = QTableWidgetItem(str(valor))

                # 🔒 trava ID
                if col == 0:
                    cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsEditable)

                self.setItem(row, col, cell)

        self.blockSignals(False)   

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
            dados["localizacao"],
            dados["slot"]
        ]

        for col, valor in enumerate(valores):
            item = QTableWidgetItem(str(valor))

            # 🔥 CENTRALIZAR TEXTO
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.setItem(row, col, item)
            