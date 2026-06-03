from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from inventario.ui.pages.janela_itens_falta import JanelaItensFalta
from inventario.ui.pages.estoque import TelaEstoque
from inventario.ui.pages.historico import TelaHistorico

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from inventario.ui.pages.estoque import TelaEstoque
from inventario.ui.pages.historico import TelaHistorico
from inventario.ui.pages.janela_itens_falta import JanelaItensFalta 
from inventario.services.alerta_service import AlertService
from inventario.ui.pages.alertas_page import PageAlertas
from inventario.services.alerta_service import AlertService

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
        # STACK
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # REGISTRO DE PÁGINAS
        self.pages = {}

        # SERVICE ALERTAS
        self.alerta_service = AlertService(self.service)

        self.register_pages()

        # PAGE ALERTAS
        self.pages["alertas"] = PageAlertas(self.alerta_service)

        # ROTAS
        self.btn_estoque.clicked.connect(lambda: self.navigate("estoque"))
        self.btn_historico.clicked.connect(lambda: self.navigate("historico"))
       #self.btn_falta.clicked.connect(self.abrir_falta) popup do henrique
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
        alertas = self.alerta_service.get_alertas()

        janela = JanelaItensFalta(alertas)
        janela.show()