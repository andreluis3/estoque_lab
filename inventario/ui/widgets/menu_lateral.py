from PyQt6.QtWidgets import QFrame, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, pyqtSignal, Qt
from inventario.utils.paths import IMAGES_DIR
from inventario.ui.theme.styles import ESTILO_BOTAO_MENU, ESTILO_BOTAO_MENU_COLAPSADO


class MenuLateralWidget(QFrame):
    # Sinais para comunicação com a página pai externa (inalterados)
    action_editar = pyqtSignal()
    action_adicionar = pyqtSignal()
    action_remover = pyqtSignal()
    action_historico = pyqtSignal()
    action_falta = pyqtSignal()
    action_itens_lista_desejos = pyqtSignal()
    action_exportacao = pyqtSignal()

    # Constantes visuais do menu
    LARGURA_ABERTA = 310
    LARGURA_FECHADA = 72
    ALTURA_BOTAO = 50
    ESPACAMENTO = 10
    TOPO_BOTOES = 120
    TAMANHO_ICONE = 30
    MARGEM_ABERTA = 17
    MARGEM_FECHADA = 15

    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_aberto = True
        self.iniciar_menu_lateral()

    def iniciar_menu_lateral(self):
        # IMPORTANTE: setFixedWidth() estava travando minimumWidth ==
        # maximumWidth == 260. Isso fazia o Qt "clampar" qualquer
        # setGeometry() de volta para 260px -- o menu nunca encolhia
        # de verdade, só os botões por dentro mudavam de estilo.
        # Por isso o efeito sanfona quebrou. Removendo a trava:
        self.setMinimumWidth(0)
        self.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
        self.resize(self.LARGURA_ABERTA, self.height())

        self.setStyleSheet("""
            QFrame {
                background-color: #111111;
                border-right: 2px solid #0078ff;
            }
        """)
        print("[MenuLateral] Construindo interface...")

        self.botao_editar = QPushButton(self)
        self.botao_adicionar = QPushButton(self)
        self.botao_remover = QPushButton(self)
        self.botao_historico = QPushButton(self)
        self.botao_falta = QPushButton(self)
        self.botao_lista_desejos = QPushButton(self)

        # (widget, texto, ícone, sinal)
        self._botoes_config = [
            (self.botao_editar, "Editar item", "icone_editar_item_transparente_final.png", self.action_editar),
            (self.botao_adicionar, "Adicionar item", "icone_adicionar_item_transparente_final.png", self.action_adicionar),
            (self.botao_remover, "Remover item", "icone_remover_item_transparente_final.png", self.action_remover),
            (self.botao_historico, "Histórico", "icone_historico_transparente_final.png", self.action_historico),
            (self.botao_falta, "Itens em falta", "icone_itens_em_falta_transparente_final.png", self.action_falta),
            (self.botao_lista_desejos, "Lista de desejos", "icone_itens_utilizados_transparente_final.png", self.action_itens_lista_desejos),
        ]

        for btn, texto, icone_nome, sinal in self._botoes_config:
            btn.setIcon(QIcon(str(IMAGES_DIR / icone_nome)))
            btn.setIconSize(QSize(self.TAMANHO_ICONE, self.TAMANHO_ICONE))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(sinal.emit)

        self._posicionar_botoes(self.LARGURA_ABERTA)
        self._aplicar_estilo_botoes(expandido=True)

        print("[MenuLateral] Menu criado com", len(self._botoes_config), "botões.")

    def _posicionar_botoes(self, largura_menu):
        """Reposiciona e redimensiona os botões conforme a largura atual do menu.
        Chamado tanto na criação quanto a cada frame da animação de abrir/fechar."""
        margem = self.MARGEM_FECHADA if largura_menu <= self.LARGURA_FECHADA + 10 else self.MARGEM_ABERTA
        largura_botao = max(largura_menu - (margem * 2), self.TAMANHO_ICONE)
        y = self.TOPO_BOTOES
        for btn, *_ in self._botoes_config:
            btn.setGeometry(margem, y, largura_botao, self.ALTURA_BOTAO)
            y += self.ALTURA_BOTAO + self.ESPACAMENTO

    def _aplicar_estilo_botoes(self, expandido: bool):
        """Alterna entre 'ícone + texto' e 'somente ícone'. Só deve ser chamado
        no início (ao fechar) ou no fim (ao abrir) da animação — nunca durante,
        para não cortar texto no meio da transição."""
        for btn, texto, *_ in self._botoes_config:
            btn.setText(texto if expandido else "")
            btn.setToolTip("" if expandido else texto)
            btn.setStyleSheet(ESTILO_BOTAO_MENU if expandido else ESTILO_BOTAO_MENU_COLAPSADO)
        self.menu_aberto = expandido