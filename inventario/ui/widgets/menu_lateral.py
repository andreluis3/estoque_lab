from PyQt6.QtWidgets import QFrame, QPushButton, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, pyqtSignal
from inventario.utils.paths import IMAGES_DIR
from inventario.ui.theme.styles import ESTILO_BOTAO_MENU

class MenuLateralWidget(QFrame):
    # Sinais para comunicação com a página pai externa
    action_editar = pyqtSignal()
    action_adicionar = pyqtSignal()
    action_remover = pyqtSignal()
    action_historico = pyqtSignal()
    action_falta = pyqtSignal()
    action_itens_lista_desejos = pyqtSignal()

    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.iniciar_menu_lateral()


    def iniciar_menu_lateral(self):
        self.setFixedWidth(350)
        self.setStyleSheet("""
            QFrame {
                background-color: #111111;
                border-right: 2px solid #0078ff;
            }
        """)
        print("[MenuLateral] Construindo interface...")
        
        # Instanciar Botões com exata nomenclatura visual
        self.botao_editar = QPushButton("Editar item", self)
        self.botao_adicionar = QPushButton("Adicionar item", self)
        self.botao_remover = QPushButton("Remover item", self)
        self.botao_historico = QPushButton("Histórico", self)
        self.botao_falta = QPushButton("Itens em falta", self)
        self.botao_lista_desejos = QPushButton("Lista de desejos", self)

        botoes = [
            (self.botao_editar, 140, "icone_editar_item_transparente_final.png", self.action_editar),
            (self.botao_adicionar, 215, "icone_adicionar_item_transparente_final.png", self.action_adicionar),
            (self.botao_remover, 290, "icone_remover_item_transparente_final.png", self.action_remover),
            (self.botao_historico, 365, "icone_historico_transparente_final.png", self.action_historico),
            (self.botao_falta, 440, "icone_itens_em_falta_transparente_final.png", self.action_falta),
            (self.botao_lista_desejos, 515, "icone_itens_utilizados_transparente_final.png", self.action_itens_lista_desejos),
        ]

        for btn, pos_y, icone_nome, sinal in botoes:
            btn.setGeometry(20, pos_y, 340, 55)
            btn.setStyleSheet(ESTILO_BOTAO_MENU)
            btn.setIcon(QIcon(str(IMAGES_DIR / icone_nome)))
            btn.setIconSize(QSize(80, 80))
            btn.clicked.connect(sinal.emit)
            
        print("[MenuLateral] Menu criado.")
        print("[MenuLateral] Botões:")
        print("   Editar")
        print("   Adicionar")
        print("   Remover")
        print("   Histórico")
        print("   Itens em falta")
        print("   Lista de desejos")
        print("   Itens utilizados")