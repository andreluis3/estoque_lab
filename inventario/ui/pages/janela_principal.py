from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from ui.pages.janela_itens_falta import JanelaItensFalta
from ui.pages.estoque import TelaEstoque
from ui.pages.historico import TelaHistorico

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from ui.pages.estoque import TelaEstoque
from ui.pages.historico import TelaHistorico
from ui.pages.janela_itens_falta import JanelaItensFalta
class JanelaPrincipal(QMainWindow):
    def __init__(self, service):
        super().__init__()

        self.service = service

        self.setWindowTitle("Sistema Estoque - HUB")
        self.resize(1200, 800)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout(self.central)

        # BOTÕES
        self.btn_falta = QPushButton("Itens em Falta")
        self.btn_estoque = QPushButton("Estoque")
        self.btn_historico = QPushButton("Histórico")

        self.layout.addWidget(self.btn_falta)
        self.layout.addWidget(self.btn_estoque)
        self.layout.addWidget(self.btn_historico)

        # STACK PRINCIPAL
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # PAGES (tudo usa service)
        self.page_estoque = TelaEstoque(self.service)
        self.page_historico = TelaHistorico(self.service)

        self.stack.addWidget(self.page_estoque)
        self.stack.addWidget(self.page_historico)

        # CONEXÕES
        self.btn_estoque.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_estoque)
        )

        self.btn_historico.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_historico)
        )

        self.btn_falta.clicked.connect(self.abrir_falta)

    def abrir_falta(self):
        alertas = self.service.get_alertas()
        janela = JanelaItensFalta(alertas)
        janela.exec()  # melhor que show()