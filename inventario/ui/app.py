from inventario.ui.pages.henrique_screen import TelaHenriquePage

class AppUI:
    def __init__(self, service):
        self.service = service
        # Instancia a interface limpa e decomposta passando o motor de dados (Service)
        self.window = TelaHenriquePage(estoque_service=self.service)

    def show(self):
        self.window.showMaximized() # Garante abertura ocupando a tela de forma profissional