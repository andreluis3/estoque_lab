
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView
)
from PyQt6.QtCore import Qt


class EscolherItemDialog(QDialog):

    def __init__(self, candidatos, parent=None):
        super().__init__(parent)

        self.candidatos = candidatos
        self.acao = None
        self.item_selecionado = None

        self.configurar_janela()
        self.criar_interface()
        self.carregar_candidatos()

    def configurar_janela(self):
        self.setWindowTitle("Item já cadastrado")
        self.setMinimumSize(950, 420)

        self.setStyleSheet("""
            QDialog {
                background-color: #111111;
                color: white;
            }

            QLabel {
                color: white;
                font-size: 13px;
            }

            QTableWidget {
                background-color: #0b0b0b;
                color: white;
                border: 1px solid #2e2e38;
                gridline-color: #2e2e38;
                selection-background-color: #0078ff;
                selection-color: white;
            }

            QHeaderView::section {
                background-color: #1e1e24;
                color: white;
                padding: 7px;
                border: 1px solid #2e2e38;
                font-weight: bold;
            }

            QPushButton {
                background-color: #0078ff;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 9px 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #005ed1;
            }

            QPushButton:disabled {
                background-color: #333333;
                color: #888888;
            }
        """)

    def criar_interface(self):
        layout = QVBoxLayout(self)

        titulo = QLabel(
            "Já existem itens com o mesmo nome e modelo."
        )
        titulo.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        descricao = QLabel(
            "Selecione um registro para adicionar a quantidade, "
            "cadastre um novo registro ou cancele a operação."
        )
        descricao.setWordWrap(True)

        layout.addWidget(titulo)
        layout.addWidget(descricao)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(8)
        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Nome",
            "Tipo",
            "Modelo",
            "Quantidade",
            "Caixa",
            "Localização",
            "Slot"
        ])

        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tabela.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.tabela.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.tabela)

        botoes = QHBoxLayout()

        self.botao_adicionar = QPushButton(
            "Adicionar ao ID selecionado"
        )
        self.botao_novo = QPushButton(
            "Cadastrar novo ID"
        )
        self.botao_cancelar = QPushButton(
            "Cancelar"
        )

        self.botao_adicionar.clicked.connect(
            self.selecionar_existente
        )
        self.botao_novo.clicked.connect(
            self.cadastrar_novo
        )
        self.botao_cancelar.clicked.connect(
            self.reject
        )

        botoes.addWidget(self.botao_adicionar)
        botoes.addWidget(self.botao_novo)
        botoes.addWidget(self.botao_cancelar)

        layout.addLayout(botoes)

    def carregar_candidatos(self):
        self.tabela.setRowCount(len(self.candidatos))

        campos = [
            "id",
            "nome",
            "tipo",
            "modelo",
            "quantidade",
            "caixa",
            "localizacao",
            "slot"
        ]

        for linha, item in enumerate(self.candidatos):
            for coluna, campo in enumerate(campos):
                valor = item.get(campo)

                celula = QTableWidgetItem(
                    "" if valor is None else str(valor)
                )

                if campo == "id":
                    celula.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                self.tabela.setItem(
                    linha,
                    coluna,
                    celula
                )

        self.tabela.resizeRowsToContents()

    def selecionar_existente(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            return

        self.item_selecionado = self.candidatos[linha]
        self.acao = "somar"
        self.accept()

    def cadastrar_novo(self):
        self.acao = "novo"
        self.item_selecionado = None
        self.accept()