from inventario.ui.pages.henrique_screen import TelaHenriquePage

class AppUI:

    def __init__(self, service):

        print("="*60)
        print("[APPUI] Inicializando AppUI")
        print("="*60)

        self.service = service

        print("[APPUI] Criando TelaHenriquePage...")

        self.window = TelaHenriquePage(
            estoque_service=self.service
        )
        print("[DEBUG APP] Importou TelaHenriquePage")
        print("[APPUI] TelaHenriquePage criada.")

    def show(self):

        print("[APPUI] Exibindo janela maximizada.")

        self.window.showMaximized()