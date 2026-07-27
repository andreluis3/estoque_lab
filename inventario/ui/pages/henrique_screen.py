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
from inventario.ui.dialogs.adicionar_dialog import AdicionarDialog
from inventario.ui.dialogs.editar_dialog import EditarDialog
from inventario.ui.dialogs.remover_dialog import RemoverDialog
from inventario.ui.dialogs.movimentar_item_dialog import MovimentarItemDialog
from inventario.ui.components.mensagem import Mensagem
from inventario.ui.dialogs.remover_dialog import RemoverDialog


class TelaHenriquePage(QWidget):
    def __init__(self, estoque_service=None, parent=None):
        super().__init__(parent)
        self.estoque_service = EstoqueService()
        
        print("="*60)
        print("[DEBUG] Entrou na TelaHenriquePage")
        print("[DEBUG] estoque_service:", estoque_service)
        print("[DEBUG] parent:", parent)
        print("="*60)
        self.estoque_service = estoque_service
        self.item_selecionado = None
        self.menu_aberto = True
        self.iniciar_ui()
        self.conectar_sinais()

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
        self.largura_menu = self.menu.LARGURA_ABERTA
        self.largura_menu_fechado = self.menu.LARGURA_FECHADA
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
        
        # Conexão do sinal de item selecionado da tabela ao método item_clicado
        self.tabela.item_selecionado.connect(
            self.salvar_item_selecionado
        )
        
        self.menu.action_falta.connect(self.abrir_movimentacao)
        print("[TelaHenriquePage] Conectando sinais...")

        # Configura as proporções iniciais geométricas
        self.atualizar_layout()
        print(self.tabela.geometry())
        self.verificar_alertas_sistema()
        self.carregar_dados_tabela_naui()
        print("[TelaHenriquePage] Interface OK.")

        #guardando itens selecionados
        self.item_selecionado = None
    
    def animar_menu(self):
        largura_atual = self.menu.width()

        self.animacao = QPropertyAnimation(self.menu, b"geometry")
        self.animacao.setDuration(280)
        self.animacao.setEasingCurve(QEasingCurve.Type.InOutQuart)

        if self.menu_aberto:
            # Vai recolher: esconde o texto ANTES de animar, pra não vazar
            self.menu._aplicar_estilo_botoes(expandido=False)
            self.animacao.setStartValue(QRect(0, 0, largura_atual, self.altura_tela))
            self.animacao.setEndValue(QRect(0, 0, self.largura_menu_fechado, self.altura_tela))
            self.menu_aberto = False
        else:
            # Vai expandir: só mostra o texto quando a animação terminar
            self.animacao.setStartValue(QRect(0, 0, largura_atual, self.altura_tela))
            self.animacao.setEndValue(QRect(0, 0, self.largura_menu, self.altura_tela))
            self.animacao.finished.connect(lambda: self.menu._aplicar_estilo_botoes(expandido=True))
            self.menu_aberto = True

        self.animacao.valueChanged.connect(self._sincronizar_menu)
        self.animacao.start()
        print("[TelaHenriquePage] Animação do menu iniciada.")

    def _sincronizar_menu(self, valor: QRect):
        """Chamado a cada frame da animação: mantém os botões e a tabela
        acompanhando a largura atual do menu."""
        largura = valor.width()
        self.menu._posicionar_botoes(largura)
        self.atualizar_layout(largura_menu_atual=largura)

    def atualizar_layout(self, largura_menu_atual=None):
        if largura_menu_atual is None:
            largura_menu_atual = self.largura_menu if self.menu_aberto else self.largura_menu_fechado
        margem_esquerda = largura_menu_atual + 50
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
        
    def editar_item(self, dados):

        print("[EDITAR] em [HenriqueScreen] foi editado o seguinte ->", dados)

        self.estoque_service.editar_item(
            dados
        )

        self.carregar_tabela()

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
        
      
    def salvar_item_selecionado(self, item):

        print("[TelaHenriquePage] Item selecionado:")
        print(item)

        self.item_selecionado = item  
        
    #essa janela que decide se vai abrir a movimentação ou a janela de falta
    def conectar_sinais(self):
            # tabela
    
            self.menu.action_adicionar.connect(
                self.abrir_adicionar
            )
    
            self.menu.action_editar.connect(
                self.abrir_editar
            )
            
            self.menu.action_remover.connect(
                self.abrir_remover
            )
    

    def abrir_adicionar(self):
        dialog = AdicionarDialog(self)
        dialog.item_adicionado.connect(
            self.adicionar_item
        )
        dialog.exec()   
        
    def adicionar_item(self, dados):
        print("=" * 60)
        print("[TelaHenriquePage]")
        print("Recebido do Dialog:")
        print(dados)
        print("=" * 60)
        resultado = self.estoque_service.registrar_item(dados)
        print(resultado)

        if resultado["status"] == "ok":
            self.carregar_dados_tabela_naui()
            Mensagem.sucesso(
                self,
                resultado["mensagem"]
            )

        else:
            Mensagem.erro(
                self,
                resultado["mensagem"]
            )
                
    def abrir_remover(self):
        if not self.item_selecionado:
            Mensagem.erro(
                self,
                "Selecione um item para remover."
            )
            return


        dialog = RemoverDialog(
            self.item_selecionado,
            self
        )


        dialog.item_removido.connect(
            self.remover_item
        )


        dialog.exec()
        
    def remover_item(self, item_id):

        print("=" * 60)
        print("[TelaHenriquePage]")
        print("Removendo item:")
        print(item_id)
        print("=" * 60)

#chama o service para decidir deletar o item e retorna o resultado para a tela, que decide se mostra sucesso ou erro
        resultado = self.estoque_service.deletar_item(
            item_id
        )


        print("Resultado:")
        print(resultado)


        if resultado["status"] == "ok":

            self.carregar_dados_tabela_naui()

            Mensagem.sucesso(
                self,
                resultado["mensagem"]
            )


        else:

            Mensagem.erro(
                self,
                resultado["mensagem"]
            )
        
    def abrir_editar(self):

        if self.item_selecionado is None:
            print("Nenhum item selecionado para editar")
            return


        dialog = EditarDialog(
            self.item_selecionado,
            self
        )


        dialog.item_editado.connect(
            self.editar_item
        )
        dialog.exec()
        
    def abrir_movimentacao(self):

        print("ABRIR MOVIMENTAÇÃO")

        if not self.item_selecionado:
            Mensagem.erro(
                self,
                "Selecione um item para movimentar."
            )
            return

        if self.item_selecionado is None:
            print("Nenhum item selecionado")
            return

        print(self.item_selecionado)

        dialog = MovimentarItemDialog(
            self.item_selecionado,
            self
        )

        dialog.exec()
        
    """def item_clicado(self, item):
        print("====================")
        print("ITEM SELECIONADO")
        print(item)
        print("====================")
        
        self.item_clicado(item)"""
    
    def item_clicado(self, item):
        self.dialog = MovimentarItemDialog(
            item,
            self
        )

        self.dialog.adicionar_quantidade.connect(
            self.adicionar_estoque
        )

        self.dialog.remover_quantidade.connect(
            self.remover_estoque
        )
        self.dialog.exec()
        
    def adicionar_quantidade(self, item_id, quantidade):
        self.estoque_service.adicionar_quantidade(item_id, quantidade)
        self.carregar_dados_tabela_naui()
        
        print(f"[TelaHenriquePage] Adicionou {quantidade} ao item ID {item_id}.")
        self.carregar_tabela()
        
    def remover_quantidade(self, item_id, quantidade):
        self.estoque_service.remover_quantidade(item_id, quantidade)
        self.carregar_dados_tabela_naui()
        
        print(f"[TelaHenriquePage] Removeu {quantidade} do item ID {item_id}.")
        self.carregar_tabela()
        
    
        
    def carregar_dados_tabela_naui(self):
        print ("Carregando dados na tabela a partir do EstoqueService...")
        if not self.estoque_service:
            print ("Erro : Estoque service não fornecido. Verifique a inicialização.")
            return
        itens = self.estoque_service.listar_todos_itens()
        self.tabela.carregar_dados(itens)
        print("Dados carregados na tabela com sucesso.")
        