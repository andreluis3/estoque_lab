from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt


class TabelaEstoque(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(8)
        self.setHorizontalHeaderLabels([
            "ID", "Nome", "Tipo", "Modelo",
            "Quantidade", "Caixa", "Localização", "Slot"
        ])
        
        # Ajusta as colunas para preencherem o espaço da janela de forma elegante
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def carregar_dados(self, itens):
        self.blockSignals(True)  # 🔥 evita bugs ao carregar e editar inline simultaneamente

        # ORDENAÇÃO (Equivalente ao ORDER BY id ASC):
        # Ordena a lista de itens diretamente pelo valor da chave 'id' antes de desenhar a tabela
        itens.sort(key=lambda x: int(x["id"]))

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

                # 🔥 CENTRALIZAR TEXTO (Mantém o padrão estético em todas as células)
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # 🔒 trava a edição da célula se for a coluna do ID (Coluna 0)
                if col == 0:
                    cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsEditable)

                self.setItem(row, col, cell)

        self.blockSignals(False)   
        print(f"[tabela_estoque] {len(itens)} items carregados na tabela com sucesso.")

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

            # 🔒 Se por acaso for o ID, garante que nasce travado também
            if col == 0:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.setItem(row, col, item)
        print(f"[tabela_estoque] Item adicionado: {dados['nome']} ({dados['modelo']}) com ID {dados['id']}.")
        