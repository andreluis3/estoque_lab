from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QTableView


class TabelaEstoque(QTableView):
    def __init__(self):
        super().__init__()

        self.model = QStandardItemModel()
        self.setModel(self.model)

        self.model.setHorizontalHeaderLabels([
            "Tipo", "Item", "Modelo", "Qtd", "Caixa", "Slot"
        ])

    def carregar_dados(self, itens):
        print("CARREGANDO NA TABELA:", len(itens))  # DEBUG

        self.model.setRowCount(0)  # limpa

        for item in itens:
            linha = [
                QStandardItem(str(item["categoria"])),
                QStandardItem(str(item["item"])),
                QStandardItem(str(item["modelo"])),
                QStandardItem(str(item["quantidade"])),
                QStandardItem(str(item["local_caixa"])),
                QStandardItem(str(item["local_slot"])),
            ]

            self.model.appendRow(linha)

        self.resizeColumnsToContents()