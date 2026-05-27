from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from ui.pages.janela_itens_falta import JanelaItensFalta
from ui.pages.estoque import TelaEstoque
from ui.pages.historico import TelaHistorico

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from ui.pages.estoque import TelaEstoque
from ui.pages.historico import TelaHistorico
from ui.pages.janela_itens_falta import JanelaItensFalta 
from inventario.services.alerta_service import AlertService
from ui.pages.alertas_page import PageAlertas


class JanelaPrincipal(QMainWindow):
    def __init__(self, service):
        super().__init__()

        self.service = service

        self.setWindowTitle("Sistema Estoque - HUB")
        self.resize(1200, 800)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout(self.central)

        # NAVBAR
        self.btn_falta = QPushButton("Itens em Falta")
        self.btn_estoque = QPushButton("Estoque")
        self.btn_historico = QPushButton("Histórico")

        self.layout.addWidget(self.btn_falta)
        self.layout.addWidget(self.btn_estoque)
        self.layout.addWidget(self.btn_historico)
        #alerta henrique
        self.self.alert_service = AlertService(self.service)
       

        # STACK (router real)
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # REGISTRO DE PÁGINAS (IMPORTANTE)
        self.pages = {}

        self.register_pages()

        # ROTAS
        self.btn_estoque.clicked.connect(lambda: self.navigate("estoque"))
        self.btn_historico.clicked.connect(lambda: self.navigate("historico"))
        self.btn_falta.clicked.connect(self.abrir_falta)
        self.pages["alertas"] = PageAlertas(self.alert_service)
        self.stack.addWidget(self.pages["alertas"])
        
        #btn
        self.btn_falta.clicked.connect(
        lambda: self.navigate("alertas")
            )
        
    def register_pages(self):
        self.pages["estoque"] = TelaEstoque(self.service)
        self.pages["historico"] = TelaHistorico(self.service)

        for page in self.pages.values():
            self.stack.addWidget(page)


    def navigate(self, name: str):
        page = self.pages.get(name)
        if page:
            self.stack.setCurrentWidget(page)

    def abrir_falta(self):
        alertas = self.service.get_alertas()
        janela = JanelaItensFalta(alertas)
        janela.exec()  # melhor que show()