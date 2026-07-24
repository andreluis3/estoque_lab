from PyQt6.QtWidgets import QWidget, QPushButton, QApplication
from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve, Qt
from inventario.ui.widgets.menu_lateral import MenuLateralWidget
from inventario.ui.widgets.barra_busca import BarraBuscaWidget
from inventario.ui.components.logo_widget import LogoWidget
from inventario.ui.widgets.tabela_estoque_widget import TabelaEstoqueWidget
from inventario.ui.widgets.popup_alerta import PopupAlertaWidget
from inventario.ui.dialogs.falta_dialog import DialogFalta
from inventario.services.estoque_service import EstoqueService
import traceback


class TelaHenriquePage(QWidget):
    def __init__(self, estoque_service=None, parent=None):
        super().__init__(parent)
        
        print("="*60)
        print("[DEBUG] Entrou na TelaHenriquePage")
        print("[DEBUG] estoque_service:", estoque_service)
        print("[DEBUG] parent:", parent)
        print("="*60)
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
        # 1. Tabela oficial do sistema
        self.tabela = TabelaEstoqueWidget(self)
        print("[TelaHenriquePage] TabelaEstoqueWidget criada.")
        print(f"[TelaHenriquePage] Dimensões da tela: {self.largura_tela}x{self.altura_tela}")

        self.tabela.show()

        print("[TelaHenriquePage] Tabela criada.")
        self.tabela.show()
        print("[TelaHenriquePage] Tabela criada.")
        print("Tabela criada")

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
        print("[TelaHenriquePage] Menu criado.")

        # 4. Componente de Busca (Centralizado Dinamicamente)
        self.barra_busca = BarraBuscaWidget(self)
        x_busca = int(self.largura_tela - 400) // 2 - 50
        self.barra_busca.move(x_busca, 50)

        # 5. Componente de Logo (Canto Supeself.input_busca = QLineEdit(self)rior Direito)
        self.logo = LogoWidget(self)
        self.logo.move(self.largura_tela - 175, 15)
        print("[TelaHenriquePage] Logo criada.")

        # Conexões de Sinais dos Componentes aos Métodos Locais / Pontes de Lógica
        self.barra_busca.texto_alterado.connect(
            self.realizar_busca
        )
        self.menu.action_falta.connect(self.abrir_janela_falta)
        print("[TelaHenriquePage] Conectando sinais...")

        # Configura as proporções iniciais geométricas
        self.atualizar_layout()
        print(self.tabela.geometry())
        self.verificar_alertas_sistema()
        self.carregar_dados_tabela_naui()
        print("[TelaHenriquePage] Interface OK.")

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
        print("[TelaHenriquePage] Animação do menu iniciada.")

    def atualizar_layout(self):
        margem_esquerda = (self.largura_menu + 50) if self.menu_aberto else 80
        self.tabela.setGeometry(
            margem_esquerda,
            150,
            self.width() - margem_esquerda - 50,
            self.height() - 250
        )


    def realizar_busca(self, termo):
        try:
            
            termo = termo.strip()
            print("==============================")
            print("[BUSCA HENRIQUE em realizar_busca] Termo recebido:", termo)
            print("Termo:", termo)

            if termo:

                itens = self.estoque_service.buscar_itens(termo)

            else:

                itens = self.estoque_service.listar_todos_itens()


            print("Itens encontrados:", len(itens))


            self.tabela.carregar_dados(itens)

            print("Tabela atualizada")


        except Exception:

            import traceback
            traceback.print_exc()

#DEF COMENTADA PARA TESTAR O REALIZAR BUSCA ACIMA
    """def realizar_busca(self):
        
        try:
            termo = self.input_busca.text().strip()

            print(f"[BUSCA Henrique_screen] Termo: {termo}")

            print("[BUSCA Henrique_screen] Chamando service...")
            itens = self.estoque_service.buscar_itens(termo)

            print("[BUSCA Henrique_screen] Service retornou")
            print(itens)

            print(f"[BUSCA Henrique_screen] Quantidade: {len(itens)}")

            print("[BUSCA Henrique_screen] Atualizando tabela...")
            self.tabela.carregar_dados(itens)

            print("[BUSCA Henrique_screen] Tabela atualizada.")

        except Exception:
            import traceback
            traceback.print_exc()"""

    def emitir_texto_alterado(self, texto):

        print("="*50)
        print("[BarraBusca] Texto digitado:")
        print(texto)
        print("="*50)

        self.texto_alterado.emit(texto)

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
        
    def carregar_dados_tabela_naui(self):
        print ("Carregando dados na tabela a partir do EstoqueService...")
        if not self.estoque_service:
            print ("Erro : Estoque service não fornecido. Verifique a inicialização.")
            return
        itens = self.estoque_service.listar_todos_itens()
        self.tabela.carregar_dados(itens)
        print("Dados carregados na tabela com sucesso.")
        