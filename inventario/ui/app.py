from ui.pages.janela_principal import JanelaPrincipal


class AppUI:
    def __init__(self, service):
        self.service = service
        self.window = JanelaPrincipal(service)

    def show(self):
        self.window.show()