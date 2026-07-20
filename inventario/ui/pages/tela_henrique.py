# PARA FAZER:
    # removaer barra preta 
    # retirar popup de pesquisa

    # Converter imagens para padrao da bibliote os - para poder abrir em outras maquinas

from inventario.services.estoque_service import EstoqueService
from inventario.services.backup_service import criar_backup
from inventario.frontend_henrique.projeto.utils import *
from inventario.frontend_henrique.projeto.alerta import verificar_estoque
from inventario.frontend_henrique.projeto.utils import *
from inventario.ui.theme.scrollbar import SCROLLBAR
from inventario.frontend_henrique.projeto.JanelasSegundarias.janela_falta import JanelaItensFalta
from inventario.frontend_henrique.projeto.utils import *
import sys
import os
from docx import Document
from datetime import datetime

from PyQt6.QtGui import QIcon   # Para adicionar imagens
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from inventario.utils.paths import IMAGES_DIR
# Importando componentes gráficos da biblioteca PyQt6:
from PyQt6.QtGui import QPixmap

from PyQt6.QtGui import QIcon   # Para popup
from PyQt6.QtCore import (
    QPropertyAnimation,
    QRect,
    QEasingCurve,
    Qt,
    QTimer
)

from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtWidgets import (
    QApplication,       # Motor gráfico
    QWidget,            # Janela
    QLabel,             # Texto
    QPushButton,        # Botões
    QVBoxLayout,        # Organiza os elementos verticalmente
    QLineEdit,          # Campo para digitar texto
    QTableWidget,       # Tabelas
    QTableWidgetItem,   # Elementos da tabela
    QMessageBox,         # Caixa de mensagem

    # Bibliotecas para aba lateral:
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QFrame,  

    # Para o popup:
    QSystemTrayIcon,
    QDialog,
) # FIM from PyQt6.QtWidgets import

from PyQt6.QtCore import (
    QPropertyAnimation,
    QRect,
    QEasingCurve,
    Qt,  )

class PopupAlerta(QDialog):
    def __init__(self, quantidade_alertas, lista_alertas, parent=None):
        super().__init__(parent)

        
        self.parent = parent
        self.lista_alertas = lista_alertas

        self.setFixedSize(350, 160)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setStyleSheet("""
            background-color: #1e1e1e;
            border-radius: 15px;
            color: white;
        """)
        print("="*60)
        print("[TelaHenriquePage] __init__")
        print("="*60)
        # TEXTO
        self.label = QLabel(
            f"⚠ {quantidade_alertas} itens com estoque baixo",
            self
        )
        
        self.label.setGeometry(
            150,
            55,
            700,
            40
        )
        
        self.label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        # BOTÃO SAIBA MAIS
        self.botao = QPushButton("Saiba mais", self)
        self.botao.setGeometry(100, 90, 150, 45)

        self.botao.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border-radius: 10px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #505050;
            }
        """)

        # conecta ao mesmo método do sistema principal
        self.botao.clicked.connect(self.acao_saiba_mais)

        QTimer.singleShot(10000, self.close)

    def acao_saiba_mais(self):
        self.close()

        # CHAMA A MESMA JANELA DO BOTÃO "Itens em falta"
        if self.parent is not None:
            self.parent.abrir_janela_falta()

class SistemaInventarioV2(QWidget):
    # Funções principais:
    def __init__(self, estoque_service=None):
        super().__init__()  # Inicializa a classe e a jenaela
        self.estoque_service = estoque_service
        
        self.alertas = []
        if self.alertas:
            self.popup = PopupAlerta(
                len(self.alertas),
                self.alertas
            )

            # Popup:
            if self.alertas:
                self.popup = PopupAlerta(
                    len(self.alertas),
                    self.alertas,
                    parent=self   # <-- ESSENCIAL
                )

                self.mostrar_popup()


        self.menu_aberto = True # Cria objeto para aba lateral
       
        self.iniciar_ui()   # Chama a interface gráfica

    def iniciar_ui(self):
        # Pegando medidas da tela:
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        
        self.largura_tela = geometry.width()
        self.altura_tela = geometry.height()

        self.largura_menu = 320

        print(self.largura_tela, self.altura_tela)    
         # Janela:
        self.setWindowTitle("Inventário")   # Nome da janela
        
        self.resize(self.largura_tela, self.altura_tela)
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: white;
            }
        """)
        
        # Aba/Menu lateral:
        self.menu = QFrame(self)
        self.menu.setGeometry(0, 0, 500, self.altura_tela)

        self.menu.setStyleSheet("""
            QFrame {
                background-color: #111111;
                border-right: 2px solid #0078ff;
            }
        """)
        
        self.menu.raise_()

        # Área principal do menu: 
        self.titulo = QLabel(
        #    "Sistema de Inventário",
            self
        )

        self.titulo.setGeometry(350, 50, 500, 60)

        self.titulo.setStyleSheet("""
            color: white;
            font-size: 32px;
            font-weight: bold;
        """)

        # Campo de busca
        self.input_busca = QLineEdit(self)
        
        x_campo_de_busca = int (self.largura_tela - 400) // 2
        self.input_busca.setGeometry(
            x_campo_de_busca,   # posição X
            50,    # posição Y
            400,   # largura
            60     # self.altura_tela
        )

        self.input_busca.setPlaceholderText(    # Texto dentro do campo de busca
            "Digite o nome do componente"   )

        self.input_busca.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                font-size: 18px;

                border-radius: 15px;
                padding-left: 18px;

                border: 2px solid #2d2d2d;
            }

            QLineEdit:focus {
                border: 2px solid #0078ff;
            }
        """)    

        # Botão Menu:
        self.botao_menu = QPushButton(
            "☰",
            self
        )

        self.botao_menu.setGeometry(
            20,
            20,
            60,
            60
        )

        self.botao_menu.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: white;
                font-size: 28px;
                border-radius: 18px;
                border: 2px solid #0078ff;
            }

            QPushButton:hover {
                background-color: #0078ff;
            }

            QPushButton:pressed {
                background-color: #005ed1;
            }
        """)

        self.botao_menu.clicked.connect(
            self.animar_menu
        )

        # Botões dentro do Menu:
        # ESTILO PADRÃO DOS BOTÕES
        estilo_botao = """
            QPushButton {
                background-color: #1b1b1b;
                color: white;
                border: 1px solid #2d2d2d;
                border-radius: 14px;
                font-size: 35px;
                text-align: left;
                padding-left: 20px;
            }

            QPushButton:hover {
                background-color: #0078ff;
                border: 1px solid #3399ff;
            }

            QPushButton:pressed {
                background-color: #005ed1;
            }
        """

        # BOTÃO EDITAR
        self.botao_editar = QPushButton(
            "Editar item",
            self.menu
        )

        self.botao_editar.setStyleSheet(
            estilo_botao
        )

        # BOTÃO ADICIONAR
        self.botao_adicionar = QPushButton(
            "Adicionar item",
            self.menu
        )

        self.botao_adicionar.setStyleSheet(
            estilo_botao
        )

        # BOTÃO REMOVER
        self.botao_remover = QPushButton(
            "Remover item",
            self.menu
        )

        self.botao_remover.setStyleSheet(
            estilo_botao
        )

        # BOTÃO HISTÓRICO
        self.botao_historico = QPushButton(
            "Histórico",
            self.menu
        )

        self.botao_historico.setStyleSheet(
            estilo_botao
        )

        # BOTÃO ITENS EM FALTA
        self.botao_falta = QPushButton(
            "Itens em falta",
            self.menu
        )
        self.botao_falta.clicked.connect(self.abrir_janela_falta)   # O que o botão deve fazer ao ser precionado

        self.botao_falta.setStyleSheet(
            estilo_botao
        )

        # BOTÃO ITENS UTILIZADOS
        self.botao_itensUsados = QPushButton(
            "Itens utilizados",
            self.menu
        )

        self.botao_itensUsados.setStyleSheet(
            estilo_botao
        )

        # POSIÇÃO DOS BOTÕES     
        self.botao_editar.setGeometry(
            20,
            140,
            340,
            55
        )

        self.botao_adicionar.setGeometry(
            20,
            215,
            340,
            55
        )

        self.botao_remover.setGeometry(
            20,
            290,
            340,
            55
        )

        self.botao_historico.setGeometry(
            20,
            365,
            340,
            55
        )

        self.botao_falta.setGeometry(
            20,
            440,
            340,
            55
        )

        self.botao_itensUsados.setGeometry(
            20,
            515,
            340,
            55
        )

        # Botão de busca
        self.botao_busca = QPushButton(
            "Buscar",
            self    )

        self.botao_busca.setGeometry(
            x_campo_de_busca + 450,   # X
            50,    # Y
            200,   # largura
            60     # self.altura_tela
        )

        self.botao_busca.setStyleSheet("""
            QPushButton {
                background-color: #0078ff;
                color: white;

                font-size: 18px;
                font-weight: bold;

                border-radius: 15px;
            }

            QPushButton:hover {
                background-color: #3399ff;
            }

            QPushButton:pressed {
                background-color: #005ed1;
            }
        """)
        
        self.botao_busca.clicked.connect(
            self.realizar_busca )

        self.botao_busca.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                font-size: 20px;
                border-radius: 15px;
            }

            QPushButton:hover {
                background-color: #505050;
            }
        """)

        # TABELA
        self.tabela = QTableWidget(self)

        # SCROLL MODERNO
        self.tabela.setVerticalScrollMode(
            QTableWidget.ScrollMode.ScrollPerPixel
        )

        self.tabela.setHorizontalScrollMode(
            QTableWidget.ScrollMode.ScrollPerPixel
        )

        # POSIÇÃO E TAMANHO
        self.tabela.setGeometry(
            430,                          # começa depois do menu
            150,
            self.largura_tela // 2,       # metade da tela
            self.altura_tela - 220
        )

        # ESTILO
        self.tabela.setStyleSheet(f"""
            QTableWidget {{
                background-color: #111111;
                color: white;

                border: 1px solid #0078ff;
                border-radius: 14px;

                font-size: 16px;

                gridline-color: transparent;

                padding: 6px;
            }}

            QTableWidget::item {{
                padding: 10px;
                border-bottom: 1px solid #1a1a1a;
            }}

            QTableWidget::item:selected {{
                background-color: #0078ff;
                color: white;
                border-radius: 6px;
            }}

            QHeaderView::section {{
                background-color: #151515;
                color: #0078ff;

                padding: 14px;

                border: none;

                font-weight: bold;
                font-size: 15px;
            }}

            QCornerButton::section {{
                background-color: #151515;
                border: none;
            }}

            {SCROLLBAR}
        """)
        
        # ALTURA DAS LINHAS
        self.tabela.verticalHeader().setDefaultSectionSize(38)

        # ESCONDE NUMERAÇÃO DA ESQUERDA
        self.tabela.verticalHeader().setVisible(False)

        # CENTRALIZA CABEÇALHO
        self.tabela.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # COLUNAS AUTOMÁTICAS
        header = self.tabela.horizontalHeader()
        header.setStretchLastSection(True)

        # DISTRIBUI AS COLUNAS
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # Imagens: 
        caminho_logo = str(IMAGES_DIR / "Logo_IPT.png")

        caminho_editarItem = str(
            IMAGES_DIR / "icone_editar_item_transparente_final.png"
        )

        caminho_removerItem = str(
            IMAGES_DIR / "icone_remover_item_transparente_final.png"
        )

        caminho_adicionarItem = str(
            IMAGES_DIR / "icone_adicionar_item_transparente_final.png"
        )

        caminho_itensUtilizados = str(
            IMAGES_DIR / "icone_itens_utilizados_transparente_final.png"
        )

        caminho_historico = str(
            IMAGES_DIR / "icone_historico_transparente_final.png"
        )

        caminho_itensFalta = str(
            IMAGES_DIR / "icone_itens_em_falta_transparente_final.png"
)

        # LOGO IPT
        self.logo = QLabel(self)
        pixmap_logo = QPixmap(caminho_logo)

        # REDIMENSIONA A IMAGEM
        pixmap_logo = pixmap_logo.scaled(
            120,
            120,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.logo.setPixmap(pixmap_logo)

        # POSIÇÃO NO CANTO SUPERIOR DIREITO
        self.logo.setGeometry(
            self.width() - 175,
            15,
            120,
            120
        )

        # Adicionando icones nos botões:
        self.botao_editar.setIcon(QIcon(caminho_editarItem))
        self.botao_adicionar.setIcon(QIcon(caminho_adicionarItem))
        self.botao_remover.setIcon(QIcon(caminho_removerItem))
        self.botao_historico.setIcon(QIcon(caminho_historico))
        self.botao_falta.setIcon(QIcon(caminho_itensFalta))
        self.botao_itensUsados.setIcon(QIcon(caminho_itensUtilizados))

        for botao in [
            self.botao_editar,
            self.botao_adicionar,
            self.botao_remover,
            self.botao_historico,
            self.botao_falta,
            self.botao_itensUsados
        ]:
            botao.setIconSize(QSize(80, 80))

        self.atualizar_layout()     # ATUALIZA O LAYOUT AO INICIAR

    # Funções de apoio: 
    def animar_menu(self):  # Função para animação do menu
        self.largura_menu = 400    
        
        self.animacao = QPropertyAnimation(
            self.menu,
            b"geometry"
        )

        self.animacao.setDuration(300)
        self.animacao.setEasingCurve(
            QEasingCurve.Type.InOutQuart
        )

        if self.menu_aberto:
            self.animacao.setStartValue(
                QRect(0, 0,self.largura_menu, self.altura_tela)
            )             
            self.animacao.setEndValue(
                QRect(-self.largura_menu, 0, self.largura_menu, self.altura_tela)
            )

            self.menu_aberto = False

        else:
            self.animacao.setStartValue(
                QRect(-self.largura_menu, 0, self.largura_menu, self.altura_tela)
            )

            self.animacao.setEndValue(
                QRect(0, 0, self.largura_menu, self.altura_tela)
            )

            self.menu_aberto = True

        self.animacao.valueChanged.connect(
            lambda: self.atualizar_layout()
        )
        print("[Tela_Henrique] Construindo interface...")
        self.animacao.start()
                                                                                      
    def realizar_busca(self):   # Busca o item nas planilhas
        nome = self.input_busca.text()

        print(f"Buscando: {nome}")

        QMessageBox.information(
            self,
            "Busca",
            f"Busca integrada futuramente:\n{nome}"
        )
        return
       

    def atualizar_layout(self):
        # Função para tabela acompanhar o menu
        if self.menu_aberto:
            margem_esquerda = self.largura_menu + 50
        else:
            margem_esquerda = 80

        self.tabela.setGeometry(
            margem_esquerda,
            150,
            self.width() - margem_esquerda - 50,
            self.height() - 250
        )

    def mostrar_popup(self):    # `Para parte de popup`

        screen = QApplication.primaryScreen()

        geometry = screen.availableGeometry()

        x = geometry.width() - 340
        y = geometry.height() - 180

        self.popup.move(x, y)

        self.popup.show()

    def abrir_janela_falta(self):   # Para o botao_falta
        self.janela_falta = JanelaItensFalta(
            self.alertas
        )

        self.janela_falta.show()

    def abrir_janela_falta(self):
        self.janela_falta = JanelaItensFalta(
            self.alertas
        )

        self.janela_falta.show()

#comentado para rodar no meu main  

# Inicialização
#app = QApplication(sys.argv)    # Cria o motor da interfaca gráfica
#janela = SistemaInventario()    # Instancia a classe  
#janela.show()   # Exibe a janela

#sys.exit(app.exec())    # Executa o código novamente (loopFe)