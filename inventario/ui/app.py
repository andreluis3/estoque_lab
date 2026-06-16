from inventario.ui.pages.henrique_screen import TelaHenriquePage

class AppUI:
    def __init__(self, service):
        self.service = service

        self.window = TelaHenriquePage(
            estoque_service=self.service
        )

    def show(self):
        self.window.showMaximized()