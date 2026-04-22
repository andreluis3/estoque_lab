from PyQt6.QtWidgets import QTableView
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor

from themes import cor_por_categoria, status_por_quantidade


class TabelaEstoque(QTableView):
    def __init__(self):
        super().__init__()

        self.model = QStandardItemModel()
        self.setModel(self.model)

        self.configurar_tabela()

    def configurar_tabela(self):
        headers = ["Tipo", "Item", "Modelo", "Qtd", "Caixa", "Slot", "Status"]
        self.model.setHorizontalHeaderLabels(headers)

    def carregar_dados(self, itens):
        self.model.removeRows(0, self.model.rowCount())

        for item in itens:
            tipo = item["categoria"]
            qtd = item["quantidade"]

            cor = cor_por_categoria(tipo)
            status, cor_status = status_por_quantidade(qtd)

            linha = [
                QStandardItem(tipo),
                QStandardItem(item["item"]),
                QStandardItem(item["modelo"]),
                QStandardItem(str(qtd)),
                QStandardItem(item["local_caixa"]),
                QStandardItem(item["local_slot"]),
                QStandardItem(status)
            ]

            # 🎨 cor por tipo
            for col in linha:
                col.setBackground(QColor(cor))

            # ⚠️ prioridade: status
            if status != "OK":
                for col in linha:
                    col.setBackground(QColor(cor_status))

            self.model.appendRow(linha)