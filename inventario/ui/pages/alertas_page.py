from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from ui.pages.janela_itens_falta import JanelaItensFalta

#trouxe do programa do henrique
class PageAlertas(QWidget):
    def __init__(self, alert_service):
        super().__init__()

        self.alert_service = alert_service

        layout = QVBoxLayout(self)

        self.btn_abrir = QPushButton("Ver Itens em Falta")
        self.btn_abrir.clicked.connect(self.abrir_alertas)

        layout.addWidget(self.btn_abrir)

    def abrir_alertas(self):
        alertas = self.alert_service.get_alertas()
        self.janela = JanelaItensFalta(alertas)
        self.janela.show()