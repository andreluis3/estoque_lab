from PyQt6.QtWidgets import QWidget, QPushButton, QApplication
from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve, Qt
from inventario.ui.widgets.menu_lateral import MenuLateralWidget
from inventario.ui.widgets.barra_busca import BarraBuscaWidget
from inventario.ui.components.logo_widget import LogoWidget
from inventario.ui.widgets.tabela_estoque_widget import TabelaEstoqueWidget
from inventario.ui.widgets.popup_alerta import PopupAlertaWidget
from inventario.ui.dialogs.falta_dialog import DialogFalta

class TelaHenriquePage(QWidget):
    def __init__(self, estoque_service=None, parent=None):
        super().__init__(parent)
        self.estoque_service = estoque_service
        self.menu_aberto = True
        self.largura_menu = 400
        self.iniciar_ui()

    def iniciar_ui(self):
        # Resgata dimensões dinâmicas da tela igual ao original
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        self.largura_tela = geometry.width()
        self.altura_tela = geometry.height()

        self.resize(self.largura_tela, self.altura_tela)
        self.setStyleSheet("background-color: black; color: white;")

        # 1. Instanciação da Tabela Primeiro (Fica ao fundo do Menu Lateral)
        self.tabela = TabelaEstoqueWidget(self)

        # 2. Instanciação do Menu Lateral Animado
        self.menu = MenuLateralWidget(self)
        self.menu.setGeometry(0, 0, self.largura_menu, self.altura_tela)
        self.menu.raise_()

        # 3. Gatilho de Ativação do Menu (Botão Hambúrguer)
        self.botao_menu = QPushButton("☰", self)
        self.botao_menu.setGeometry(20, 20, 60, 60)
        self.botao_menu.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: white;
                font-size: 28px;
                border-radius: 18px;
                border: 2px solid #0078ff;
            }
            QPushButton:hover { background-color: #0078ff; }
            QPushButton:pressed { background-color: #005ed1; }
        """)
        self.botao_menu.clicked.connect(self.animar_menu)
        self.botao_menu.raise_()

        # 4. Componente de Busca (Centralizado Dinamicamente)
        self.barra_busca = BarraBuscaWidget(self)
        x_busca = int(self.largura_tela - 400) // 2 - 50
        self.barra_busca.move(x_busca, 50)

        # 5. Componente de Logo (Canto Superior Direito)
        self.logo = LogoWidget(self)
        self.logo.move(self.largura_tela - 175, 15)

        # Conexões de Sinais dos Componentes aos Métodos Locais / Pontes de Lógica
        self.barra_busca.buscar_clicado.connect(self.realizar_busca)
        self.menu.action_falta.connect(self.abrir_janela_falta)

        # Configura as proporções iniciais geométricas
        self.atualizar_layout()
        self.verificar_alertas_sistema()

    def animar_menu(self):
        self.animacao = QPropertyAnimation(self.menu, b"geometry")
        self.animacao.setDuration(300)
        self.animacao.setEasingCurve(QEasingCurve.Type.InOutQuart)

        if self.menu_aberto:
            self.animacao.setStartValue(QRect(0, 0, self.largura_menu, self.altura_tela))
            self.animacao.setEndValue(QRect(-self.largura_menu, 0, self.largura_menu, self.altura_tela))
            self.menu_aberto = False
        else:
            self.animacao.setStartValue(QRect(-self.largura_menu, 0, self.largura_menu, self.altura_tela))
            self.animacao.setEndValue(QRect(0, 0, self.largura_menu, self.altura_tela))
            self.menu_aberto = True

        self.animacao.valueChanged.connect(self.atualizar_layout)
        self.animacao.start()

    def atualizar_layout(self):
        margem_esquerda = (self.largura_menu + 50) if self.menu_aberto else 80
        self.tabela.setGeometry(
            margem_esquerda,
            150,
            self.width() - margem_esquerda - 50,
            self.height() - 250
        )

    def realizar_busca(self, texto):
        # Aqui você fará a chamada limpa ao seu Service no futuro. Exemplo visual mantido:
        print(f"Buscando no Service por: {texto}")

    def verificar_alertas_sistema(self):
        # Simulação ou leitura segura de dados vindos do seu Service principal
        self.alertas_dados = [] 
        if self.alertas_dados:
            self.popup = PopupAlertaWidget(len(self.alertas_dados), self)
            self.popup.saiba_mais_clicado.connect(self.abrir_janela_falta)
            
            # Posiciona no canto inferior direito de forma idêntica
            x = self.largura_tela - 340
            y = self.altura_tela - 180
            self.popup.move(x, y)
            self.popup.show()

    def abrir_janela_falta(self):
        self.janela_falta = DialogFalta(self.alertas_dados, self)
        self.janela_falta.show()